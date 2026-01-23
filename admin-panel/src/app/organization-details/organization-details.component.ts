import { Component, OnInit } from '@angular/core';
import { Organization } from '../models/organization.mosel';
import { OrganizationService } from '../services/organization.service';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FolderComponent } from '../folder/folder.component';
import { UserService } from '../services/user.service';
import { Folder } from '../models/user.model';

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrl: './organization-details.component.scss',
  standalone: true,
  imports: [RouterModule, CommonModule, FolderComponent]
})
export class OrganizationDetailsComponent implements OnInit{
  public org!: Organization;
  public isPopupVisible: boolean = false; 

  constructor(
    private orgService: OrganizationService,
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router
  ) {
  }

  public ngOnInit(): void {
    const id: number = Number(this.route.snapshot.paramMap.get('id'));
    this.orgService.getOrganizationById(id).subscribe((org: Organization) => {(this.org = org);
      console.log('org: ', this.org);
    });
  }

  public goBack(): void {
    this.router.navigate(['/admin/organization']);
  }

  public onFileDeleted(fileId: number): void {
    if (confirm('Удалить файл?')) {
      this.userService.deleteFile(fileId).subscribe(() => {
        this.removeFileFromFolderTree(this.org.folder, fileId);
      });
    }
  }

  public onFolderDeleted(folderId: number): void {
    if (confirm('Удалить папку?')) {
      this.userService.deleteFolder(folderId).subscribe(() => {
        this.removeFolderFromFolderTree(this.org.folder, folderId);
      });
    }
  }

  public togglePopup(): void {
    this.isPopupVisible = !this.isPopupVisible;
  }

  private removeFileFromFolderTree(folders: Folder[], fileId: number): boolean {
    for (let folder of folders) {
      const fileIndex = folder.files.findIndex((f) => f.id === fileId);
      if (fileIndex !== -1) {
        folder.files.splice(fileIndex, 1);
        return true;
      }
      if (this.removeFileFromFolderTree(folder.folders, fileId)) {
        return true;
      }
    }
    return false;
  }

  private removeFolderFromFolderTree(folders: Folder[], folderId: number): boolean {
    const folderIndex = folders.findIndex((f) => f.id === folderId);
    if (folderIndex !== -1) {
      folders.splice(folderIndex, 1);
      return true;
    }
    for (let folder of folders) {
      if (this.removeFolderFromFolderTree(folder.folders, folderId)) {
        return true;
      }
    }
    return false;
  }
  
}
