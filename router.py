import json
from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import AnyHttpUrl
from crud import createResult, selectResult
from engine import picSearch

from schemas import DataTypeEnum, EngineEnum, Response
from setting import setting

router = APIRouter()


def checkSecret(secret: Optional[str] = None):
    if not setting.secret or len(setting.secret) == 0:
        return True
    return setting.secret == secret


@router.get("/search", response_model=Response)
async def _(
    url: AnyHttpUrl,
    engine: EngineEnum = EngineEnum.ascii2d,
    dataType: DataTypeEnum = DataTypeEnum.web,
    isAuth: bool = Depends(checkSecret)
):
    if not isAuth:
        return {
            "success": False,
            "msg": "Query illegal.",
            "data": None
        }
    res, hint = await picSearch(url, engine)
    if len(res) == 0:
        return {
            "success": False,
            "msg": "No result founded.",
            "data": None
        }
    data = {
        "pic_url": url,
        "hint": hint,
        "results": res
    }
    if dataType == DataTypeEnum.json:
        return {
            "success": True,
            "msg": "",
            "data": data
        }
    elif dataType == DataTypeEnum.web:
        return {
            "success": True,
            "msg": "",
            "data": {
                "key": createResult(json.dumps(data))
            }
        }


@router.get("/result")
async def _(key: str = Query(default=..., min_length=6, max_length=6)):
    result = selectResult(key)
    if result:
        return {
            "success": True,
            "msg": "",
            "data": json.loads(result["data"])
        }
    else:
        return {
            "success": False,
            "msg": "Result is expired.",
            "data": None
        }
