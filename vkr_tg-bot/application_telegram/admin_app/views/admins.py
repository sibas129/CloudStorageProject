from fastapi import APIRouter, Depends
from typing import Annotated

from fastapi.responses import JSONResponse
from starlette import status
from admin_app.schemas.auth import TokenData, AdminModel
from admin_app.schemas.admins import AdminData
from admin_app.services.admins import get_current_user, get_current_user_superadmin, database_worker, Admins, AdminService

admin_router = APIRouter()


@admin_router.get("/admin")
async def get_admins(current_user: Annotated[TokenData, Depends(get_current_user)]) -> list[AdminModel]:
    result = await AdminService(database_worker).get_admin_list()
    return result


@admin_router.post("/admin")
async def make_admins(admin_data: AdminData, current_user: Annotated[TokenData, Depends(get_current_user_superadmin)]):
    result = await AdminService(database_worker).add_admin(admin_data)
    if not result:
        return {"success": False}
    return {"success": True}


@admin_router.delete("/admin/{admin_id}")
async def remove_admins(admin_id: int, current_user: Annotated[TokenData, Depends(get_current_user_superadmin)]):
    result = await AdminService(database_worker).remove_admin(admin_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Cannot remove superadmin'})
    return {"success": True}
