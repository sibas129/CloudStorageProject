from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from admin_app.schemas.auth import TokenData
from admin_app.schemas.organizations import OrganizationResponse, OrganizationsWithFolders
from admin_app.services.admins import get_current_user
from admin_app.services.organizations import OrganizationService
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Organizations

organization_router = APIRouter()
database_worker = DatabaseWorkerAsync(database_engine_async)


@organization_router.get('/organization')
async def organizations_list(current_user: Annotated[TokenData, Depends(get_current_user)]) -> list[
    OrganizationResponse]:
    org_list = await database_worker.custom_orm_select(cls_from=Organizations)
    return org_list


@organization_router.get('/organization/{org_id}', response_model=OrganizationsWithFolders)
async def organization_detail(org_id: int, current_user: Annotated[TokenData, Depends(get_current_user)]):
    organization = await OrganizationService(database_worker).organization_by_id(org_id)
    if not organization:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'User files does not exist'})
    return organization


@organization_router.delete('/organization/{org_id}')
async def organization_delete(org_id: int, current_user: Annotated[TokenData, Depends(get_current_user)]):
    try:
        await OrganizationService(database_worker).delete_organization(org_id)
    except Exception as e:
        return {'success': False}
    return {'success': True}
