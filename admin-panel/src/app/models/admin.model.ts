export interface Admin {
    id: number;
    username: string;
    password?: string;
    is_superadmin: boolean;
  }