from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.common.consts import MAX_API_KEY, MAX_API_WHITELIST
from app.database.conn import db
from app.database.schema import Users, ApiKeys, ApiWhiteLists
from app import models as m
from app.errors import exceptions as ex
import string
import secrets

from app.models import MessageOk, UserMe

router = APIRouter(prefix='/user')


@router.get('/me', response_model=UserMe)
async def get_me(request: Request):
    user = request.state.user
    user_info = Users.get(id=user.id)
    return user_info


@router.put('/me')
async def put_me(request: Request):
    ...


@router.delete('/me')
async def delete_me(request: Request):
    ...


@router.get('/apikeys', response_model=List[m.GetApiKeyList])
async def get_api_keys(request: Request):
    """
    API KEY 조회
    :param request:
    :return:
    """
    user = request.state.user
    api_keys = ApiKeys.filter(user_id=user.id).all()
    return api_keys


async def check_api_owner(user_id, key_id):
    api_keys = ApiKeys.get(id=key_id, user_id=user_id)
    if not api_keys:
        raise ex.NoKeyMatchEx()
