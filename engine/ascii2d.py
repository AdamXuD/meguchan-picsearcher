import asyncio
import aiohttp
from bs4 import BeautifulSoup, Tag
from setting import setting


def parseResultItem(tag: Tag):
    thumbnail = f"https://ascii2d.net{tag.select_one('.image-box img').attrs['src']}"
    similarity = ""
    title = tag.select_one(".detail-box").get_text(" ", True)
    relativeUrl = [
        a.attrs["href"] for a in tag.select(".detail-box h6 a")
    ]
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
        resultList = soup.select(".row.item-box")
        return [{
            **parseResultItem(item),
            "engine": "ascii2d"
        } for item in resultList]
    except Exception as e:
        print(repr(e))
        return [], "ascii2d: Unexpected error when parsing HTML."


async def getResult(imgUrl: str):
    realUrl = ""
    result = []
    try:
        async with aiohttp.request(
            "GET",
            "https://ascii2d.net/search/url/" + imgUrl,
            proxy=setting.ascii2d_proxy,
            timeout=aiohttp.ClientTimeout(setting.query_timeout)
        ) as resp:
            if resp.status != 200:
                return result, "Status code is not 200."
            realUrl = str(resp.real_url)
            result.extend(parseHTML(await resp.text())[0: 5])

        async with aiohttp.request(
            "GET",
            realUrl.replace("/color/", "/bovw/"),
            proxy=setting.ascii2d_proxy,
            timeout=aiohttp.ClientTimeout(setting.query_timeout)
        ) as resp:
            if resp.status != 200:
                return result, "Status code is not 200."
            result.extend(parseHTML(await resp.text())[0: 5])
    except asyncio.TimeoutError:
        return result, f"ASCII2D Timeout (operation >= {setting.query_timeout} seconds)."

    return result, ""
