from fynautoserver.models.index import UserModel, LoginModel
from fynautoserver.schemas.index import UserSchema
from fynautoserver.utils.index import create_response
from fynautoserver.crud.auth_crud import hash_passsword, verify_password, create_Access_token, decode_access_token, create_refresh_token
from bson import ObjectId

async def create_new_tokens(isValidUser:UserModel,payload:LoginModel,message:str):
    isValidUser = isValidUser.model_dump()
    isValidUser['id'] = str(isValidUser['id'])
    minimalUser = {
        "id": isValidUser["id"],
        "username": isValidUser["username"],
        "role": isValidUser["role"]
    }
    access_token = create_Access_token(minimalUser)
    refresh_token = create_refresh_token(minimalUser)

    await UserSchema.find_one(UserSchema.username == payload.username).update(
        {"$set": {"refreshToken": refresh_token}}
    )

    authenticated_data = {
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'tokenType': 'bearer',
        'user' : isValidUser,
        "message": message
    }
    return create_response(success=True, result=authenticated_data, status_code=201)

async def create_user(payload:UserModel):
    existing = await UserSchema.find_one({'username':payload.username})

    if existing:
        response = 'User already exist with this username, Please choose different username.'
        return create_response(success=False, error_message=response, status_code=201)
    
    else:
        hashedPassword = hash_passsword(payload.password)
        user = UserSchema(
            username = payload.username,
            password = hashedPassword,
            role = payload.role
        )

        response = await user.insert()
        response.id = str(response.id)
        return create_response(success=True, result=response, status_code=201)


async def login_user(payload:LoginModel):
    isValidUser = await UserSchema.find_one({'username':payload.username})

    if isValidUser:
        isValidPassword = verify_password(payload.password,isValidUser.password)

        if isValidPassword:
            auth_data = await create_new_tokens(isValidUser,payload,'User logged in successfully')
            return auth_data
        else:
            return create_response(success=False, error_message='invalid password', status_code=201)
    else:
        return create_response(success=False, error_message='invalid email and password', status_code=201)
    
async def create_access_from_refresh(refresh_token: str):
    try:
        refresh_data = decode_access_token(refresh_token)
        user_id = ObjectId(refresh_data['id'])

        isVerifiedUser = await UserSchema.find_one({'_id':user_id})

        if not isVerifiedUser:
            return create_response(success=False, error_message="User not found", status_code=404)

        #is both the refresh token matched else return error
        if isVerifiedUser.refreshToken != refresh_token:
            return create_response(success=False, error_message='Unauthorized User', status_code=401)

        payload = LoginModel(
            username= isVerifiedUser.username,
            password= isVerifiedUser.password
        )
        auth_data = await create_new_tokens(isVerifiedUser,payload,'Tokens Generated')
        return auth_data
    except Exception as e:
        return create_response(success=False, error_message=f'unable to create access token : {e}', status_code=201)
    