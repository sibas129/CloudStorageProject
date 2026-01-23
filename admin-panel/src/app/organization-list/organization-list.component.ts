import { Component, OnInit } from '@angular/core';
import { Organization } from '../models/organization.mosel';
import { OrganizationService } from '../services/organization.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-organization-list',
  templateUrl: './organization-list.component.html',
  styleUrls: ['./organization-list.component.scss'],
  standalone: true,
  imports: [RouterModule, CommonModule],
})
export class OrganizationListComponent implements OnInit{
  public organizations: Organization[] = [];

  constructor(
    private orgService: OrganizationService,
     private router: Router) {
     }

     public ngOnInit(): void {
      this.orgService.getOrganizations().subscribe( (orgs) => (this.organizations = orgs));
     }

     public viewDetails(org: Organization): void {
      this.router.navigate(['/admin/organization', org.id]);
    }

    public deleteOrg(org: Organization): void {
      if (confirm(`Удалить организацию? ${org.name}?`)) {
        this.orgService.deleteOrganization(org.id).subscribe((response) => {
          if (response.success) {
            this.organizations = this.organizations.filter((o) => o.id !== org.id);
          }
        });
      }
    }
}
