from schemas import EngineEnum
from .ascii2d import getResult as ascii2dSearch
from .iqdb import getResult as iqdbSearch
from .saucenao import getResult as saucenaoSearch
from .tracemoe import getResult as traceSearch


async def picSearch(imgUrl: str, engine: EngineEnum):
    if engine == EngineEnum.ascii2d:
        return await ascii2dSearch(imgUrl)
    elif engine == EngineEnum.iqdb:
        return await iqdbSearch(imgUrl)
    elif engine == EngineEnum.saucenao:
        return await saucenaoSearch(imgUrl)
    elif engine == EngineEnum.tracemoe:
        return await traceSearch(imgUrl)
    elif engine == EngineEnum.all:
        resList = []
        hintList = []
        for item in [
            await saucenaoSearch(imgUrl),
            await iqdbSearch(imgUrl),
            await ascii2dSearch(imgUrl),
            await traceSearch(imgUrl)
        ]:
            res, hint = item
            resList.extend(res)
            hintList.append(hint)
        return resList, "\n".join(hintList)
    else:
        return [], ""
