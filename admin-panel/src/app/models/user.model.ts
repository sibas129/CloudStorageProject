export interface User {
  id: number;
  telegram_id: string;
  telegram_name: string;
  created_at: string;
  updated_at: string;
  folder: Folder[];
  size: number;
}

export interface Folder {
  id: number;
  name: string;
  files: File[];
  folders: Folder[];
  created_at: string;
  updated_at: string;
  root?: boolean;
}

export interface File {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
}