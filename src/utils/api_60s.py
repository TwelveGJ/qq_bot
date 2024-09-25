# 感谢开源项目 https://github.com/vikiboss/60s?tab=readme-ov-file

import time

import aiohttp
import asyncio

# region 60s_url
url_60s = 'https://60s.viki.moe/60s?v2=1'
url_today_in_history = 'https://60s.viki.moe/today_in_history'
# endregion

# region 每天60s
async def request_data_60s():
    async with aiohttp.ClientSession() as session:
        async with session.get(url_60s) as response:
            json_60s = await response.json()

    status = json_60s['status']
    if status != 200:
        return None

    # dict{news, tip, url, cover}
    # news: list[str]
    # tip: str
    # updated: str
    # url: str
    # cover: str
    data = json_60s['data']

    return data

async def get_60s(type='text'):
    assert type in ['text', 'markdown'], f'type must be text or markdown, can\'t be {type}'
    data_60s = await request_data_60s()
    news = data_60s['news']
    news = [f'{i+1}. {news[i]}' for i in range(len(news))]
    tip = data_60s['tip']

    # updated中的内容为时间戳，需将其转化为实际时间
    updated = data_60s['updated']
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(updated)/1000 + 8*3600))

    if type == 'text':
        combined_content = f"\n于 {update_time} 更新\n每日新闻:\n" + "\n".join(news)
        combined_content += "\n\n每日一句:\n" + tip
    elif type == 'markdown':
        combined_content = f"\n### 于 {update_time} 更新\n# 每日新闻:\n## " + "\n## ".join(news)
        combined_content += "\n\n# 每日一句:\n## " + tip
    else:
        raise ValueError(f'Invalid type: {type}')

    return combined_content

# endregion

# region 历史上的今天
async def request_data_history_today():
    async with aiohttp.ClientSession() as session:
        async with session.get(url_today_in_history) as response:
            json_history_today = await response.json()

    status = json_history_today['status']
    if status != 200:
        return None
    
    # list[dict{title, year, date, desc, type, link}]
    # type: str 1-event 2-birth 3-death
    data = json_history_today['data'] 

    return {
        'data': data
    }
        
async def get_history_today(type='text'):
    assert type in ['text', 'markdown'], f'type must be text or markdown, can\'t be {type}'

    data_history_today = await request_data_history_today()
    data = data_history_today['data']

    history_today = [f'{i+1}. [{data[i]["year"]}]-{data[i]["date"]} {data[i]["title"]}：{data[i]["desc"]}' for i in range(len(data))]

    if type == 'text':
        combined_content = "历史上的今天:\n" + "\n".join(history_today)
    elif type == 'markdown':
        combined_content = "\n# 历史上的今天:\n## " + "\n## ".join(history_today)
    else:
        raise ValueError(f'Invalid type: {type}')

    return combined_content

# endregion

if __name__ == '__main__':
    # print(asyncio.run(get_60s('text')))
    # print(asyncio.run(get_60s('markdown')))
    # print(asyncio.run(get_history_today('text')))
    print(asyncio.run(get_history_today('markdown')))
