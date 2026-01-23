from fastapi import APIRouter

from admin_app.views.admins import admin_router
from admin_app.views.auth import auth_router
from admin_app.views.files import files_router
from admin_app.views.organizations import organization_router
from admin_app.views.users import user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(user_router)
router.include_router(files_router)
router.include_router(organization_router)
