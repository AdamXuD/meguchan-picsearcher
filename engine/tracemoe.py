import asyncio
import aiohttp

from setting import setting

animeInfoQuery = \
    """
        query ($id: Int) {
            Media (id: $id, type: ANIME) {
                title {
                  native
                  romaji
                  english
                }
                startDate {
                  year
                  month
                  day
                }
                endDate {
                  year
                  month
                  day
                }
                episodes
                duration
                format
                type
                status
                season
                isAdult
                siteUrl
            }
        }
    """


async def getResult(imgUrl: str):
    try:
        otherInfoList = []
        async with aiohttp.request(
            "GET",
            "https://api.trace.moe/search",
            params={
                "url": imgUrl
            },
            proxy=setting.tracemoe_proxy,
            timeout=aiohttp.ClientTimeout(setting.query_timeout)
        ) as resp:
            if resp.status != 200:
                return [], "Status code is not 200."
            data = await resp.json()

        res = data["result"].pop(0)
        if not res:
            return [], "No results found."

        anilistID = res["anilist"]
        episode = res["episode"] if res.get("episode") else "-"
        posTime = f"{int(res['from'] / 60)}:{int(res['from'] % 60)}"
        otherInfoList.append(f"该图出自第{episode}集的{posTime}")

        title = res["filename"]
        similarity = f"{round(res['similarity'] * 100)}%"
        thumbnail = res['image']
        relativeUrl = []

        async with aiohttp.request(
            "POST",
            "https://graphql.anilist.co/",
            json={
                "query": animeInfoQuery,
                "variables": {
                    "id": anilistID
                }
            }
        ) as resp:
            if resp.status != 200:
                otherInfoList.append("获取番剧信息失败~")
            else:
                aniInfo = (await resp.json())["data"]["Media"]

                episodes = aniInfo["episodes"]
                duration = aniInfo["duration"]
                fmt = aniInfo["format"]
                tp = aniInfo["type"]
                status = aniInfo["status"]
                season = aniInfo["season"]
                isAdult = aniInfo["isAdult"]
                otherInfoList.append(
                    f"番剧信息：{episodes}集 {duration}分钟 {season}-{fmt}-{tp} {status}")
                if isAdult:
                    otherInfoList.append("!!!! R18注意 !!!!")

                startDateRes = aniInfo["startDate"]
                startDate = f"{startDateRes['year']}-{startDateRes['month']}-{startDateRes['day']}"
                endDateRes = aniInfo["endDate"]
                endDate = f"{endDateRes['year']}-{endDateRes['month']}-{endDateRes['day']}"
                otherInfoList.append(f"放送时间：自 {startDate} 到 {endDate} ")

                titleRes = aniInfo["title"]
                if titleRes.get("english"):
                    title = titleRes["english"]
                    otherInfoList.append(f"英文译名：{title}")
                # if titleRes.get("chinese"):
                #     title = titleRes["chinese"]
                #     otherInfoList.append(f"中文译名：{title}")
                if titleRes.get("romaji"):
                    title = titleRes["romaji"]
                    otherInfoList.append(f"罗马音译：{title}")
                if titleRes.get("native"):
                    title = titleRes["native"]
                    otherInfoList.append(f"日文名称：{title}")

                siteUrl = aniInfo["siteUrl"]
                relativeUrl.append(siteUrl)

        otherInfo = "\n".join(otherInfoList)

        return [{
            "engine": "tracemoe",
            "thumbnail": thumbnail,
            "similarity": similarity,
            "title": title,
            "relative_url": relativeUrl,
            "other_info": otherInfo
        }], ""
    except asyncio.TimeoutError:
        return [], f"TRACEMOE Timeout (operation >= {setting.query_timeout} seconds)."
    except Exception as e:
        print(repr(e))
        return [], "tracemoe: Unexpected error when parsing data."
