import asyncio
import aiohttp
from bs4 import BeautifulSoup, Tag

from setting import setting


def parseResultItem(tag: Tag):
    thumbnail = f"https://www.iqdb.org{tag.select_one('.image img')['src']}"
    similarity = tag.select_one("tr:nth-last-child(1)").get_text()
    title = ""
    relativeUrl = [tag.select_one(".image a")["href"]]
    otherInfo = ""

    return {
        "thumbnail": thumbnail,
        "similarity": similarity,
        "title": title,
        "relative_url": relativeUrl,
        "other_info": otherInfo
    }


def parseHTML(html: str):
    try:
        soup = BeautifulSoup(html, "html.parser")
        resultList = soup.select(".pages>div:nth-child(n+3)")
        return [{
            **parseResultItem(item),
            "engine": "iqdb"
        } for item in resultList]
    except Exception as e:
        print(repr(e))
        return [], "iqdb: Unexpected error when parsing HTML."


async def getResult(imgUrl: str):
    try:
        async with aiohttp.request(
            "GET",
            "https://www.iqdb.org/",
            params={
                "url": imgUrl
            },
            proxy=setting.iqdb_proxy,
            timeout=aiohttp.ClientTimeout(setting.query_timeout)
        ) as resp:
            if resp.status != 200:
                return [], "Status code is not 200."
            return parseHTML(await resp.text()), ""
    except asyncio.TimeoutError:
        return [], f"IQDB Timeout (operation >= {setting.query_timeout} seconds)."
