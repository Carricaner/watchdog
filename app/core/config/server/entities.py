from typing import Optional, Any

from pydantic import Field, BaseModel


class StandardBaseResponseEntity(BaseModel):
    success: bool = Field(description='Response\'s success status')


class StandardSuccessResponseEntity(StandardBaseResponseEntity):
    success: bool = True
    data: Optional[Any] = Field(description='Response\'s data')


class StandardErrorResponseEntity(StandardBaseResponseEntity):
    success: bool = False
    error_code: int = Field(default=100, description='Response\'s error code')
    message: Any = Field(default='', description='Response\'s message')


# All should be rewritten using Pydantic's BaseModel
_404_not_found_response = {
    'description': 'Not found'
}

http_status_to_response_map = {
    404: _404_not_found_response
}

__all__ = [
    'StandardSuccessResponseEntity',
    'StandardErrorResponseEntity',
    'http_status_to_response_map'
]
