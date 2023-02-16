from email import message
from nonebot import on_fullmatch,require
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot,Event,MessageSegment


get_glist=on_fullmatch(msg = "指令查询",block=True)
@get_glist.handle()
async def ggi_handle(event: Event):
    res = """1. 测试用户(csyh):\t用于测试机器人识别用户\n2. lor:\t查询卡组信息可自由搭配\n(名字 dq地区 hf花费法力 yx英雄(0,1))\n例子：lor 德玛西亚 hf2 yx1 表示查找包含德玛西亚四个字的卡牌，并且花费为2，为英雄
    3. xj:\t查询英雄技能，后面接英雄ID 例：xj 6779
    """

    await get_glist.send(res)
