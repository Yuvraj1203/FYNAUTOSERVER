from fastapi import HTTPException
from starlette.status import HTTP_421_MISDIRECTED_REQUEST,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_404_NOT_FOUND,HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN,HTTP_422_UNPROCESSABLE_ENTITY
from pymongo.errors import DuplicateKeyError,ServerSelectionTimeoutError,PyMongoError

class APIExceptionHandler:
    @staticmethod
    def bad_request(detail:str="Bad Request"):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,detail={"error":detail})
    
    @staticmethod
    def unauthorized(detail:str="Unauthorized Access"):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail={"error":detail})
    
    @staticmethod
    def unprocessable_entity(detail: str = "Unprocessable entity"):
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail={"error": detail})

    @staticmethod
    def internal_server_error(detail: str = "Internal server error"):
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": detail})

    @staticmethod
    def not_found(detail: str = "Resource not found"):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={"error": detail})
    
    @staticmethod
    def mongo_error(error:Exception):
        if isinstance(error,DuplicateKeyError):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,detail={"error": "Duplicate key error. This entry already exists."}
            )
        elif isinstance(error, ServerSelectionTimeoutError):
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "MongoDB server is unreachable. Please check connection."}
            )
        elif isinstance(error, PyMongoError):
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": f"MongoDB error: {str(error)}"}
            )
        else:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": f"Unknown database error: {str(error)}"}
            )

    @staticmethod
    def custom_exception(status_code: int, detail: str):
        raise HTTPException(status_code=status_code, detail={"error": detail})