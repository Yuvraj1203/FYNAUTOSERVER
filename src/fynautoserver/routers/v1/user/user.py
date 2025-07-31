from fastapi import APIRouter
from fynautoserver.models.index import ResponseModel, UserModel
from fynautoserver.crud.user_crud import create_user

user_router = APIRouter()

@user_router.post('/signup',response_model=ResponseModel)
async def sign_up(payload:UserModel):
    user_response = await create_user(payload)
    return user_response