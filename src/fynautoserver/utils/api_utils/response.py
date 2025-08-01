from typing import Any, Union
from fastapi.responses import JSONResponse
from fynautoserver.models.index import ResponseModel


def create_response(
    success: bool,
    result: Any = None,
    error_message: str = None,
    error_detail: str = None,
    status_code: Union[int, str] = 200,
    unAuthorizedRequest: bool = True
) -> JSONResponse:
    content = ResponseModel(
        success=success,
        result=result,
        message=error_message,
        detail=error_detail,
        status_code=status_code,
        unAuthorizedRequest=unAuthorizedRequest,
    ).model_dump()

    print(f"🚨 DEBUG: Returning JSON Response → {content}")  # Ensure response is logged
    response = JSONResponse(content=content, status_code=status_code)

    # Force JSON response type
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers["Access-Control-Allow-Origin"] = "*"  # Explicitly allow origin
    return response

