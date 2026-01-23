import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User, Folder, File } from '../models/user.model';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl: string = '/api/users';

  constructor(private http: HttpClient) {}

  public getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl)
  }

  public getUserById(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`)
    .pipe(
      map(response => ({...response,
        folder: this.mapToFolder(response.folder)
      }))
    );
  }

  public deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  public deleteFile(fileId: number): Observable<void> {
    return this.http.delete<void>(`api/files/${fileId}`);
  }

  public deleteFolder(folderId: number): Observable<void> {
    return this.http.delete<void>(`api/folders/${folderId}`);
  }

  private mapToFolder(folder: any): Folder[] {
    const result = [{...folder,
      root: true,
    }]
    return result;
  }
}