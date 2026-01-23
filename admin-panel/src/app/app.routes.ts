import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: 'admin',
    component: AdminDashboardComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'users',
        loadComponent: () =>
          import('./user-list/user-list.component').then((m) => m.UserListComponent),
      },
      {
        path: 'users/:id',
        loadComponent: () =>
          import('./user-details/user-details.component').then((m) => m.UserDetailsComponent),
      },
      {
        path: 'organization',
        loadComponent: () =>
          import('./organization-list/organization-list.component').then((m) => m.OrganizationListComponent),
      },
      {
        path: 'organization/:id',
        loadComponent: () =>
          import('./organization-details/organization-details.component').then((m) => m.OrganizationDetailsComponent),
      },
      {
        path: 'admins',
        loadComponent: () =>
          import('./admin-list/admin-list.component').then((m) => m.AdminListComponent),
      },
      { path: '', redirectTo: 'users', pathMatch: 'full' },
    ],
  },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' },
];