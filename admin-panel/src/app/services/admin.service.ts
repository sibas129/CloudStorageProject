import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Admin } from '../models/admin.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AdminService {
  private apiUrl: string = '/api/admin';

  constructor(private http: HttpClient) {}

  public getAdmins(): Observable<Admin[]> {
    return this.http.get<Admin[]>(this.apiUrl);
  }

  public addAdmin(admin: Admin): Observable<any> {
    return this.http.post<Admin>(this.apiUrl, admin);
  }

  public deleteAdmin(id: number): Observable<{success: boolean}> {
    return this.http.delete<{success: boolean}>(`${this.apiUrl}/${id}`);
  }
}