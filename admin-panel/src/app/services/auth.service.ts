import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, tap, throwError, BehaviorSubject } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import jwt_decode, { JwtPayload } from 'jwt-decode';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface DecodedToken extends JwtPayload {
  sub: string;
  isa: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private tokenKey: string = 'authToken';
  private authStatus = new BehaviorSubject<boolean>(this.hasValidToken());

  constructor(private http: HttpClient) {}

  private hasValidToken(): boolean {
    const token = this.getToken();
    if (token) {
      const decoded = this.getDecodedToken();
      if (decoded && decoded.exp) {
        const expirationDate = new Date(decoded.exp * 1000);
        return expirationDate > new Date();
      }
    }
    return false;
  }

  public getAuthStatus(): Observable<boolean> {
    return this.authStatus.asObservable();
  }

  public login(username: string, password: string): Observable<void> {
    const body = new HttpParams()
      .set('username', username)
      .set('password', password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
    });

    return this.http
      .post<LoginResponse>('/api/login', body.toString(), { headers })
      .pipe(
        tap((response) => {
          const token = response.access_token;
          localStorage.setItem(this.tokenKey, token);
          this.authStatus.next(true);
        }),
        map(() => {}),
        catchError(this.handleError)
      );
  }

  public logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.authStatus.next(false);
  }

  public isAuthenticatedUser(): boolean {
    return this.hasValidToken();
  }

  public getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  public getDecodedToken(): DecodedToken | null {
    const token = this.getToken();
    if (token) {
      try {
        return jwt_decode<DecodedToken>(token);
      } catch (error) {
        console.error('Ошибка декодирования токена:', error);
        return null;
      }
    }
    return null;
  }

  public isSuperAdmin(): boolean {
    const decodedToken = this.getDecodedToken();
    return decodedToken ? decodedToken.isa : false;
  }

  public getCurrentAdmin(): string {
    const decodedToken = this.getDecodedToken();
    const username = decodedToken?.sub;
    console.log('username: ', username);
    return username ? username : '';
  }

  private handleError(error: HttpErrorResponse) {
    let errorMsg = 'Произошла неизвестная ошибка!';
    if (error.error instanceof ErrorEvent) {
     
      errorMsg = `Ошибка: ${error.error.message}`;
    } else {
     
      if (error.status === 401) {
        errorMsg = 'Неправильные учетные данные.';
      } else {
        errorMsg = `Ошибка сервера: ${error.status}, сообщение: ${error.message}`;
      }
    }
    return throwError(() => errorMsg);
  }
}