from __future__ import annotations
import typing
from typing import Any

from fastapi import HTTPException
from fastapi import status


class AbstractHttpException(HTTPException):
    """Abstract class for HTTP exceptions."""

    _status_code: typing.ClassVar = None
    _detail: typing.ClassVar = None
    _description: typing.ClassVar = None
    _headers: typing.ClassVar = None

    def __init__(self, detail: str | None = None, *, headers: dict[str, str] | None = None) -> None:
        if headers is None:
            headers = {}
        super().__init__(
            status_code=self._status_code,
            detail=detail or self._detail,
            headers=headers.update(self._headers or {}),
        )

    @classmethod
    def docs(
        cls: type[AbstractHttpException],
    ) -> dict[int | str, dict[str, Any]] | None:
        return {
            cls._status_code: {
                'description': cls._description,
                'content': {
                    'application/json': {
                        'example': {'detail': cls._detail},
                    },
                },
            },
        }


class UnauthorizedHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_401_UNAUTHORIZED
    _detail: typing.ClassVar = 'Could not validate credentials.'
    _headers: typing.ClassVar = {'WWW-Authenticate': 'Bearer'}


class ForbiddenHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_403_FORBIDDEN
    _detail: typing.ClassVar = "You don't have enough rights."


class NotFoundHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_404_NOT_FOUND
    _detail: typing.ClassVar = 'Object not found.'


class NotAcceptableHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_406_NOT_ACCEPTABLE
    _detail: typing.ClassVar = (
        'Your queries do not meet the required conditions. You will get more details when a real error occurs.'
    )


class BadRequestHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_400_BAD_REQUEST
    _detail: typing.ClassVar = (
        'Your queries do not meet the required conditions. You will get more details when a real error occurs.'
    )


class ImUsedHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_226_IM_USED
    _detail: typing.ClassVar = 'Im used ;D'


class DoubtfulButOkayHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = 267
    _detail: typing.ClassVar = 'Doubtful but okay (-_-)'


class GatewayTimeoutHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_504_GATEWAY_TIMEOUT
    _detail: typing.ClassVar = 'Gateway timeout. Please try again later.'


class UnprocessableEntityHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_422_UNPROCESSABLE_ENTITY
    _detail: typing.ClassVar = 'Unprocessable entity. Please check the request body.'


# Custom cases
class InvalidOTPCodeHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_400_BAD_REQUEST
    _detail: typing.ClassVar = 'Invalid OTP code or password.'


class InvalidPasswordHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_400_BAD_REQUEST
    _detail: typing.ClassVar = 'Invalid password.'


class InvalidOTPCodeOrPasswordHTTPException(AbstractHttpException):
    _status_code: typing.ClassVar = status.HTTP_400_BAD_REQUEST
    _detail: typing.ClassVar = 'Invalid OTP code or password.'
