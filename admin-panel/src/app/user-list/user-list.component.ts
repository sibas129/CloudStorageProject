import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { User } from '../models/user.model';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss'],
  standalone: true,
  imports: [RouterModule, CommonModule],
})
export class UserListComponent implements OnInit {
  public users: User[] = [];

  constructor(private userService: UserService, private router: Router) {}

  public ngOnInit(): void {
    this.userService.getUsers().subscribe((users) => (this.users = users));
  }

  public viewDetails(user: User): void {
    this.router.navigate(['/admin/users', user.id]);
  }
}