from pydantic import BaseModel, Field
from typing import Any, Optional


class ResponseModel(BaseModel):
    success: bool
    result: Optional[Any] = None
    error_message: Optional[str] = Field(default=None, alias="message")
    error_detail: Optional[str] = Field(default=None, alias="detail")
    status_code: int 
    unAuthorizedRequest: Optional[bool] = False

    class Config:
        from_attributes = True
