import { Folder, User } from "./user.model";

export interface Organization {
    id: number;
    user_id: number;
    name: string;
    is_deleted: boolean;
    created_at: string;
    folder: Folder[];
    size: number;
    users: User[];
}