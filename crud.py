import functools
from pathlib import Path
import random
import string
from playhouse.pool import PooledSqliteDatabase
from playhouse.shortcuts import model_to_dict
from peewee import Model, TextField, CharField, BigIntegerField
from datetime import datetime

from setting import setting

p = Path("./data")
if not p.is_dir():
    p.mkdir(parents=True)

db = PooledSqliteDatabase(setting.db_path)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db


class Results(BaseModel):
    created_time = BigIntegerField()
    data = TextField()
    key = CharField(unique=True)

    class Meta:
        table_name = 'results'


def CRUD(func):
    @functools.wraps(func)
    def _wrappedFunc(*args, **kwargs):
        with db:
            return func(*args, **kwargs)
    return _wrappedFunc


def nowTimestamp():
    return round(datetime.now().timestamp())


@CRUD
def clearExpiredResults():
    return Results.delete().where(
        Results.created_time <= nowTimestamp() - 3600
    ).execute() > 0


@CRUD
def initDB():
    Results.create_table(safe=True)
    clearExpiredResults()


@CRUD
def createResult(data: str):
    key = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    o = Results(
        key=key,
        data=data,
        created_time=int(datetime.now().timestamp())
    )
    if o.save():
        return key
    else:
        return None


@CRUD
def selectResult(key: str):
    query = Results.select().where(
        Results.key == key
    )
    if not query:
        return None
    res: Results = query.first()
    if nowTimestamp() - res.created_time >= 3600:
        clearExpiredResults()
        return None
    return model_to_dict(res)


initDB()
