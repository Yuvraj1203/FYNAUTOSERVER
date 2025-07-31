from fynautoserver.models.index import UserModel
from fynautoserver.schemas.index import UserSchema
from fynautoserver.utils.index import create_response,APIExceptionHandler

async def create_user(payload:UserModel):
    existing = await UserSchema.find_one({'username':payload.username})

    if existing:
        response = 'User already exist with this username, Please choose different username.'
        return create_response(success=False, error_message=response, status_code=201)
    
    else:
        user = UserSchema(
            username = payload.username,
            password = payload.password
        )

        response = await user.insert()
        response.id = str(response.id)
        return create_response(success=True, result=response, status_code=201)
