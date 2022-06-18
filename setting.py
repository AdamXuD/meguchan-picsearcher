from typing import Optional
from pydantic import AnyHttpUrl, BaseSettings


class Setting(BaseSettings):
    environment: str = "dev"
    host: str = "0.0.0.0"
    port: int = 3000

    db_path: str = "./data/data.db"       # only sqlite3

    ascii2d_proxy: Optional[AnyHttpUrl] = None
    iqdb_proxy: Optional[AnyHttpUrl] = None
    saucenao_proxy: Optional[AnyHttpUrl] = None
    tracemoe_proxy: Optional[AnyHttpUrl] = None

    query_timeout: int = 10
    result_ttl: int = 3600
    secret: Optional[str] = None


setting = Setting()
