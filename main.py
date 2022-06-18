from fastapi import FastAPI
import uvicorn

from setting import setting
from router import router

DEBUG_MODE = setting.environment == "dev"


app = FastAPI(
    debug=DEBUG_MODE,
    title="Meguchan-Picsearcher",
    docs_url="/docs" if DEBUG_MODE else None,
    redoc_url="/redoc" if DEBUG_MODE else None
)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=setting.host,
        port=setting.port,
        reload=DEBUG_MODE,
        debug=DEBUG_MODE
    )
