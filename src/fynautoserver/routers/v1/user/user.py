from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel, UserModel, LoginModel
from fynautoserver.crud.user_crud import create_user, login_user, create_access_from_refresh

user_router = APIRouter()

@user_router.post('/signup',response_model=ResponseModel)
async def sign_up(payload:UserModel):
    user_response = await create_user(payload)
    return user_response

@user_router.post('/login',response_model=ResponseModel)
async def sign_up(payload:LoginModel):
    user_response = await login_user(payload)
    return user_response

@user_router.post('/getAccessFromRefresh',response_model=ResponseModel)
async def get_access_from_refresh(refresh_token: str):
    access_token = await create_access_from_refresh(refresh_token)
    return access_token