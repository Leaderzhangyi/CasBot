import aiohttp
import nonebot
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent, PrivateMessageEvent
import re
import os

lor = on_regex(pattern="^lor\ ")
xj = on_regex(pattern="^xj\ ")


def parser_input(_input):
    # dq地区  hf耗费、花费  yx英雄(0,1) xj细节:编号
    res = {'name': "", 'region': "", 'rarity': "", 'costNormal': ""}
    new = _input[3:].strip().split(" ")
    for item in new:
        if item.startswith("dq"):
            res["region"] = item[2:]
        elif item.startswith("hf"):
            res["costNormal"] = int(item[2:])
        elif item.startswith("yx") and item[-1] == '1':
            res["rarity"] = "Champion"
        else:
            res["name"] = item
    print(res)
    return res


@lor.handle()
async def lorMethod(bot: Bot, event: Event):
    _input = str(event.get_message())
    res = parser_input(_input)
    msg = None
    imgs,ids = await get_img(res["name"], res["region"], res["rarity"], res["costNormal"])
    for img in imgs:
        msg += MessageSegment.image(img)
    if isinstance(event, GroupMessageEvent):
        await send_forward_msg_group(bot, event, "CasBot", msg if msg else ["没有此关键字的卡牌"],ids if ids else ["只有英雄卡牌显示ID"])
    elif isinstance(event, PrivateMessageEvent):
        await bot.send(event=event, message=msg if msg else "没有此关键字的卡牌")

@xj.handle()
async def lorMethod(bot: Bot, event: Event):
    _input = str(event.get_message())
    id = int(_input[2:].strip())
    msg = None
    imgs = await get_relate_img(id)
    for img in imgs:
        msg += MessageSegment.image(img)
    # print("************")
    # print(msg)
    msg += MessageSegment.at(event.get_user_id)
    await bot.send(event=event, message=msg if msg else "没有此ID的相关卡牌")


async def get_relate_img(id:int):
    url = f"https://api2.iyingdi.com/lor/card/info?id={id}"
    text = await _request(url)
    new = text["related"]
    return [item["img"] for item in new]



async def _request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Referer": "https://www.iyingdi.com/",
        "Content-Type": "text/json;charset=UTF-8"
    }
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url, headers=headers)
        #text = await (res.content.read()).decode('utf-8')
        text = await res.json(content_type=None,encoding="utf-8")
        #print(""text)
    return text


async def get_img(name: str, region: str, rarity: str, costNormal: int):
    url = f'https://api2.iyingdi.com/lor/card/search?name={name}&region={region}&rarity={rarity}&costNormal={costNormal}&token=&page=0&size=30&collect=0'
    print("请求url为：",url)
    text = await _request(url)
    text = str(text)
    print(text)
    ids = []
    if rarity != "":
        ids = re.findall(r"\'id\': (\d+)", text)
    imgs = re.findall(r"\'img\': \'(.*?)\'", text)
    print("相片为----------",imgs)
    return imgs,ids


async def send_forward_msg_group(bot: Bot, event: GroupMessageEvent, name: str, msgs,ids):

    def to_json(msg,id):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg+"\n英雄ID："+id}}

    messages = [to_json(msg,id) for msg,id in zip(msgs,ids)]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )
