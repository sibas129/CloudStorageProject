import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { Folder } from '../models/user.model';
import { CommonModule } from '@angular/common';
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.scss'],
  standalone: true,
  imports: [CommonModule],
  animations: [
    trigger('slideToggle', [
      state('collapsed', style({ height: '0', overflow: 'hidden' })),
      state('expanded', style({ height: '*', overflow: 'hidden' })),
      transition('expanded <=> collapsed', [animate('300ms ease-in-out')]),
    ]),
  ],
})
export class FolderComponent implements OnInit{
  @Input() public folder!: Folder;
  @Output() public fileDeleted = new EventEmitter<number>();
  @Output() public folderDeleted = new EventEmitter<number>();

  public isExpanded: boolean = false;

  public ngOnInit(): void {
  console.log("folder: "
  , this.folder

  );
}

  public toggle(): void {
    this.isExpanded = !this.isExpanded;
  }

  public evenRow(id: number): boolean {
    return id % 2 === 0;
  }
}