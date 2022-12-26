import json
import os
from pathlib import Path
from nonebot import get_driver

# 本地单独调试文件内容
filepath = os.path.dirname(__file__)
file_name = os.path.join(filepath, "student.json")

# 初始JSON数据(young)
student_config = [{}]


class InitData:
    def __init__(self):
        if not os.path.exists(file_name):
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(student_config, f, ensure_ascii=False, indent=4)


def write_file(user_id, date, bool):
    # 获取json数据
    with open(file_name) as f:
        get_data = json.load(f)
    # print(get_data)

    # 第一次加入新数据
    if bool == True:
        new_data = {"user": user_id, "date": date}
        get_data.append(new_data)

    # 不是第一次，修改数据
    elif bool == False:
        for i in get_data:
            if i['user'] == user_id:
                i['date'] = date
    # print(get_data)

    # 以格式化写入
    with open(file_name, 'w') as write_f:
        write_f.write(json.dumps(get_data, indent=4, ensure_ascii=False))
