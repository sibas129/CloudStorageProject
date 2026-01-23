import { Component, OnInit } from '@angular/core';
import { AdminService } from '../services/admin.service';
import { Admin } from '../models/admin.model';
import { FormBuilder, Validators, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';
import { switchMap } from 'rxjs';

@Component({
  selector: 'app-admin-list',
  templateUrl: './admin-list.component.html',
  styleUrls: ['./admin-list.component.scss'],
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
})
export class AdminListComponent implements OnInit {
  public admins: Admin[] = [];
  public adminForm!: FormGroup;
  public isSuperAdmin: boolean = false;
  constructor(
    private adminService: AdminService,
    private authService: AuthService,
    private fb: FormBuilder) {
  }

  public ngOnInit(): void {
    this.adminForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      //isSupreme: [false, Validators.required],
    });
    this.isSuperAdmin = this.authService.isSuperAdmin();
    if (!this.isSuperAdmin) {
      this.adminForm.disable();
    }
    this.adminService.getAdmins().subscribe((admins) => (this.admins = admins));
  }

  public addAdmin(): void {
    if (this.adminForm.valid) {
      const admin: Admin = this.adminForm.value;
      this.adminService.addAdmin(admin)
      .pipe(
        switchMap(() => this.adminService.getAdmins())
      )
      .subscribe((response) => {
        this.admins = response;
        this.adminForm.reset();
      });
    }
  }

  public deleteAdmin(admin: Admin): void {
    if (confirm(`Удалить администратора ${admin.username}?`)) {
      this.adminService.deleteAdmin(admin.id).subscribe((response) => {
        if (response.success) {
        this.admins = this.admins.filter((a) => a.id !== admin.id);
        }
      });
    }
  }
}