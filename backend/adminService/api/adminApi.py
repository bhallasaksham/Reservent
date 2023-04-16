
from fastapi import APIRouter
from fastapi import Request as FastAPIRequest
from fastapi.responses import JSONResponse
from adminService.handler.adminHandler import AdminHandler
from database.schemas.userSchema import UserPrivilege

adminRoutes = APIRouter()
adminHandler = AdminHandler()

@adminRoutes.get("/")
async def root():
    return {"message": "Hello World"}


@adminRoutes.get("/admin/users")
async def get_users():
    users = adminHandler.get_users()
    return users

@adminRoutes.put("/admin/users/privilege")
async def update_user_privilege(request: FastAPIRequest):
    email = request.state.user['email']
    body = await request.json()
    privilege = body.get("privilege")
    try:
        adminHandler.update_user_privilege(email, privilege)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error updating user privilege", "error": str(e)})
    return JSONResponse(status_code=200, content={"message": "User privilege updated"})
