import { Component, OnInit } from '@angular/core';
import { User, Folder } from '../models/user.model';
import { UserService } from '../services/user.service';
import { ActivatedRoute, RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FolderComponent } from '../folder/folder.component';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.scss'],
  standalone: true,
  imports: [RouterModule, CommonModule, FolderComponent],
})
export class UserDetailsComponent implements OnInit {
  public user!: User;

  constructor(
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  public ngOnInit(): void {
    const id: number = Number(this.route.snapshot.paramMap.get('id'));
    this.userService.getUserById(id).subscribe((user: User) => {(this.user = user);
    });
 
  }

  public goBack(): void {
    this.router.navigate(['/admin/users']);
  }

  public onFileDeleted(fileId: number): void {
    if (confirm('Удалить файл?')) {
      this.userService.deleteFile(fileId).subscribe(() => {
        this.removeFileFromFolderTree(this.user.folder, fileId);
      });
    }
  }

  public onFolderDeleted(folderId: number): void {
    if (confirm('Удалить папку?')) {
      this.userService.deleteFolder(folderId).subscribe(() => {
        this.removeFolderFromFolderTree(this.user.folder, folderId);
      });
    }
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