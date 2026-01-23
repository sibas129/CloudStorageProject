import { Component } from '@angular/core';
import { RouterModule, Router, RouterOutlet } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.scss'],
  standalone: true,
  imports: [RouterModule, RouterOutlet, CommonModule],
})
export class AdminDashboardComponent {
  public currentAdmin: string = '';

  constructor(private authService: AuthService, private router: Router) {
    this.currentAdmin = this.authService.getCurrentAdmin();
  }

  public logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}