from nonebot import get_driver, on_command,on_fullmatch
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageEvent, MessageSegment
from .config import Config
from .write_user import InitData, write_file
from .read_user import user_list, user_data, user_wordID, user_date
import time
global_config = get_driver().config
config = Config.parse_obj(global_config)


# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
word = on_fullmatch(msg="测试用户", block=True)

InitData()


@word.handle()
async def _(bot: Bot, event: MessageEvent):
    qq = str(event.user_id)  # 获取用户qq
    login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event.time))
    get_user_data = user_data()  # 所有用户信息 students.json文件信息
    get_user_list = user_list()  # 用户列表
    if qq in get_user_list:
        #write_file(user_id=qq, date=login_time, bool=False)
        await word.send(qq+"用户您好，你已使用CasBot机器人，感谢您的信任。")

    # 新用户
    else:
        write_file(user_id=qq, date=login_time, bool=True)  # 更新json中用户数据
        await word.send("正在创建->"+qq+"<-用户")
        await word.finish(qq+"用户已创建，后续计划开发\'个人课程表\'、\'fastlinkcookies自动绑定\'....敬请期待😎！")
