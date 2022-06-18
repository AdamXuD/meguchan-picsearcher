from enum import Enum
from typing import List, Union
from pydantic import BaseModel


class EngineEnum(str, Enum):
    ascii2d = "ascii2d"
    iqdb = "iqdb"
    saucenao = "saucenao"
    tracemoe = "tracemoe"
    all = "all"


class DataTypeEnum(str, Enum):
    json = "json"
    web = "web"


class ResultItem(BaseModel):
    engine: EngineEnum
    thumbnail: str
    title: str
    similarity: str
    relative_url: List[str]
    other_info: str


class Result(BaseModel):
    pic_url: str
    hint: str
    results: List[ResultItem]


class Key(BaseModel):
    key: str


class Response(BaseModel):
    success: bool
    msg: str
    data: Union[Result, Key, None]
