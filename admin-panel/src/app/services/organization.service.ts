import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User, Folder } from '../models/user.model';
import { Observable, map } from 'rxjs';
import { Organization } from '../models/organization.mosel';

@Injectable({
  providedIn: 'root',
})
export class OrganizationService {
  private apiUrl: string = '/api/organization';

  constructor(private http: HttpClient) {}

  public getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>(this.apiUrl)
  }

  public getOrganizationById(id: number): Observable<Organization> {
    return this.http.get<Organization>(`${this.apiUrl}/${id}`)
    .pipe(
        map(response => ({...response,
          folder: this.mapToFolder(response.folder)
        }))
      );
  }

  public deleteOrganization(id: number): Observable<{success: boolean}> {
    return this.http.delete<{success: boolean}>(`${this.apiUrl}/${id}`);
  }

  private mapToFolder(folder: any): Folder[] {
    const result = [{...folder,
      root: true,
    }]
    return result;
  }
}