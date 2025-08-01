from fynautoserver.models.index import UserModel, LoginModel
from fynautoserver.schemas.index import UserSchema
from fynautoserver.utils.index import create_response
from fynautoserver.crud.auth_crud import hash_passsword, verify_password, create_Access_token, decode_access_token

async def create_user(payload:UserModel):
    existing = await UserSchema.find_one({'username':payload.username})

    if existing:
        response = 'User already exist with this username, Please choose different username.'
        return create_response(success=False, error_message=response, status_code=201)
    
    else:
        hashedPassword = hash_passsword(payload.password)
        user = UserSchema(
            username = payload.username,
            password = hashedPassword
        )

        response = await user.insert()
        response.id = str(response.id)
        return create_response(success=True, result=response, status_code=201)


async def login_user(payload:LoginModel):
    isValidUser = await UserSchema.find_one({'username':payload.username})

    if isValidUser:
        isValidPassword = verify_password(payload.password,isValidUser.password)

        if isValidPassword:
            isValidUser = isValidUser.model_dump()
            isValidUser['id'] = str(isValidUser['id'])
            access_token = create_Access_token(isValidUser)
            authenticated_data = {
                'accessToken': access_token,
                'tokenType': 'bearer',
                'user' : isValidUser,
                "message":'user logged in successfully'
            }
            return create_response(success=True, result=authenticated_data, status_code=201)
        else:
            return create_response(success=False, error_message='invalid password', status_code=201)
    else:
        return create_response(success=False, error_message='invalid email and password', status_code=201)