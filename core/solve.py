from wxpy import *
from .bytedance import valid_bytedance_jd_query, query_bytedance_jd
from log import logger
from bs4 import BeautifulSoup

import os
import requests
import json


GROUP_NAME = "Sepicat"
bot = Bot(console_qr=True, cache_path=True)
friends = bot.friends

related_group: Group = None
if len(bot.groups().search(GROUP_NAME)) > 0:
    related_group = bot.groups().search(GROUP_NAME)[0]


def valid_msg(msg):
    '''
    验证信息
    :param msg:
    :return:
    '''
    return '我要内推' in msg.text.lower()


def invite(user):
    '''
    邀请用户方法
    :param user: User 对象
    :param bot: Bot 对象
    :return:
    '''
    group = bot.groups().search("")
    user.send(group.name)
    if len(group) > 0:
        group[0].add_members(user, use_invitation=True)


@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    '''
    处理加好友
    :param msg:
    :return:
    '''
    user = msg.card.accept()
    if valid_msg(msg):
        invite(user)
    else:
        user.send('hello {user_name},忘记填写加群口令了,去填写吧'.format(user_name=user.name))


@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    """
    处理邀请加群信息
    :param msg:
    :return:
    """
    if valid_msg(msg):
        msg.sender.send('点击加群')
        group = bot.groups().search(GROUP_NAME)
        if len(group) <= 0:
            msg.sender.send('读取群信息失败')
        else:
            msg.sender.send(group[0].name)
            gp = group[0]
            len_mem = len(gp.members)
            global related_group
            related_group = gp
            if len_mem >= 100:
                # gp.add(users=[msg.sender], use_invitation=True)
                msg.sender.send("自动拉好友接口失效，等待手动拉好友。")
            else:
                msg.sender.send_image(os.path.join(os.getcwd(), 'qrcode.jpg'))

    else:
        msg.sender.send('hello {user_name},忘记填写加群口令了,去填写吧'.format(user_name=msg.sender.name))


@bot.register(bot.groups(), msg_types=TEXT)
def reply_bytedance_jd(msg):
    if msg.is_at:
        logger.info('text - {text}'.format(text=msg.text))
        query_res = valid_bytedance_jd_query(msg=msg)
        logger.info('query_res - {res}'.format(res=query_res))

        def fetch(text: str) -> bool:
            return str(msg.text).find(text) >= 0

        if query_res is not None:
            network_res = query_bytedance_jd(query=query_res)
            desc = ""
            for item in network_res:
                desc += "【{name}】 {base} {summary} \n {desc}\n\n".format(
                    name=item['name'],
                    base=item['base'],
                    summary=item['summary'],
                    desc=item['description'])
            msg.sender.send(desc)

        elif str(msg.text).find("来一题") >= 0 or str(msg.text).find("换一题") >= 0:
            resp = requests.get("https://leetcode-cn.com/classic/problems/random-one-question/all")
            soup = BeautifulSoup(resp.content)
            title = soup.head.title.text
            url = resp.url
            msg.sender.send(f"{title}\n{url}")

        elif str(msg.text).lower().find("testflight") >= 0:
            sepicat_url = "https://testflight.apple.com/join/4ojQCz8z"
            _996calendar_url = "https://testflight.apple.com/join/G5anpfKw"
            text = f'Sepicat: {sepicat_url}\n996日历: {_996calendar_url}'
            msg.sender.send(text)

        elif str(msg.text).find("我要学习") >= 0:
            resp = requests.get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/core/study.json")
            result = json.loads(s=resp.text)
            text = ""
            if type(result) is list:
                for dic in result:
                    text += f'[{dic["title"]}]\n'
                    text += f'{dic["desc"]}\n'
            if len(text) <= 0:
                text = "未获取到有效资源"
            msg.sender.send(text)

        # 傻屌对话语录
        elif fetch("开车"):
            text = f'开车就去: https://pornhub.com\n晕车请去: https://github.com'
            msg.sender.send(text)

        elif fetch("好骚"):
            text = f'你怎么穿着品如的衣服'
            msg.sender.send(text)

        elif fetch("开花") or fetch("今年夏天") or fetch("战术后仰") or fetch("中美合拍"):
            text = f'两开花 两开花'
            msg.sender.send(text)

        elif fetch("996") or fetch("icu") or fetch("加班"):
            text = f'你不配做东哥的兄弟，不配留在京东'
            msg.sender.send(text)

        elif str(msg.text).find("冬瓜") > 5:
            text = f'别总叫冬瓜，冬瓜是你爸爸吗？'
            msg.sender.send(text)

        elif fetch("我不懂，自己想。想明白了告我"):
            text = f'那就死锁了'
            msg.sender.send(text)

        else:
            msg.sender.send("我不懂，自己想。想明白了告我。")

embed()
