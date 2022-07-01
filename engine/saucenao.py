import asyncio
import aiohttp
from bs4 import BeautifulSoup, Tag

from setting import setting


def parseResultItem(tag: Tag):
    thumbnailAttrs = tag.select_one(
        ".resulttableimage img"
    ).attrs
    thumbnail = thumbnailAttrs.get("data-src")
    if not thumbnail:
        thumbnail = thumbnailAttrs["src"]
    similarity = tag.select_one(".resultsimilarityinfo").get_text()
    title = tag.select_one(".resulttitle")
    title = title.get_text(" ") if title else ""
    relativeUrl = [
        a.attrs["href"] for a in tag.select(".resultcontentcolumn a.linkify")
    ]
    otherInfo = "".join([
        "\n" if t.name == "br" else t.get_text(" ", True)
        for t in tag.select(".resultcontentcolumn>*")
    ]).strip()

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
        resultList = soup.select(".result:not(#result-hidden-notification)")
        return [{
            **parseResultItem(item),
            "engine": "saucenao"
        } for item in resultList]
    except Exception as e:
        print(repr(e))
        return [], "saucenao: Unexpected error when parsing HTML."


async def getResult(imgUrl: str):
    try:
        async with aiohttp.request(
            "GET",
            "https://saucenao.com/search.php",
            params={
                "db": 999,
                "url": imgUrl,
            },
            proxy=setting.saucenao_proxy,
            timeout=aiohttp.ClientTimeout(setting.query_timeout)
        ) as resp:
            if resp.status != 200:
                return [], "Status code is not 200."
            return parseHTML(await resp.text()), ""
    except asyncio.TimeoutError:
        return [], f"SAUCENAO Timeout (operation >= {setting.query_timeout} seconds)."
