
from nonebot import on_command,require
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot,Event,MessageSegment
import nonebot


# 自动任务
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

def at_all():
    return MessageSegment.at("all")

# def share(url):
#     return MessageSegment.share(url=url,title="打卡链接")
    
# https://github.com/botuniverse/onebot-11/blob/master/api/public.md#send_msg-%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF
# https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html?highlight=trigger
@scheduler.scheduled_job("cron", hour="21",minute="55",id = "Daily_Question")
async def run_every():
    (bot,) = nonebot.get_bots().values()
    await bot.send_msg(
                message_type="group", # 私聊改为 privte  group_id 改为 user_id
                group_id=111952496,
                message = at_all()+"记得22:00之前完成每日一题\n打卡链接：https://flowus.cn/1e30eb8a-fd5a-489e-8047-8b122ff17b9b"
            )


# # 设置在15:00发送信息
# @timing.scheduled_job("cron", hour='15', minute='00', id="drink_tea")
# async def drink_tea():
#     bot, = get_bots().values()
#     # 发送一条群聊信息
#     await bot.send_msg(
#         message_type="group",
#         # 群号
#         group_id=12345678,
#         message='这是一条群聊信息' + send_img('三点饮茶.gif')
#     )
#     # 随机休眠2-5秒
#     await asyncio.sleep(randint(2, 5))
#     # 发送一条私聊信息
#     await bot.send_msg(
#         message_type="private",
#         # 私聊用户QQ号
#         user_id=12345678,
#         message='这是一条私聊信息' + send_img('三点饮茶.gif')
#     )






