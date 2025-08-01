from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel, UserModel, LoginModel
from fynautoserver.crud.user_crud import create_user, login_user

user_router = APIRouter()

@user_router.post('/signup',response_model=ResponseModel)
async def sign_up(payload:UserModel):
    user_response = await create_user(payload)
    return user_response

@user_router.post('/login',response_model=ResponseModel)
async def sign_up(payload:LoginModel):
    user_response = await login_user(payload)
    return user_response