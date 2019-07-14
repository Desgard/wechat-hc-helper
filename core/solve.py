from wxpy import *
from .bytedance import valid_bytedance_jd_query, query_bytedance_jd
from .github import fetch_trending
from .old_driver import fetch_old_driver_list
from log import logger
from bs4 import BeautifulSoup
from threading import Timer

import random

import os
import requests
import json
import re


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

        elif str(msg.text).lower().find("tqp") >= 0:
            resp = requests.get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/core/tqp.json")
            result: dict = json.loads(s=resp.text)
            logger.info('query_res - {res}'.format(res=result))
            text = msg.text
            f = re.match(r'.+?tqp(\d+)', text)
            if f:
                logger.info('query_id - {res}'.format(res=result))
                _id = f.group(1)
                if _id in result.keys():
                    msg.sender.send(result[_id])
                else:
                    msg.sender.send("未找到提前批职位")

        # 水友群功能 - GitHub Trending
        elif str(msg.text).lower().find("g-rank") >= 0:
            trendings = fetch_trending()
            text = "当前 GitHub Trending Rank: \n\n"
            for index, repo in enumerate(trendings):
                text += f'Rank {index} \n'
                text += repo["link"] + "\n"
                text += repo["desc"] + "\n"
                text += "⭐️ " + repo["star"] + "\n"
                text += "\n"
            msg.sender.send(text)
        
        # 水友群功能 - Old Driver 周报
        elif str(msg.text).lower().find("g-driver") >= 0:
            infos = fetch_old_driver_list()
            text = f'老司机周报 {infos[0]["updated"]} 期: \n\n'
            for index, info in enumerate(infos):
                text += f'{index}. {info["title"]}\n'
                text += info["link"] + '\n\n'
            msg.sender.send(text)

        elif str(msg.text).find("一题") >= 0 or str(msg.text).find("题来") >= 0:
            resp = requests.get("https://leetcode-cn.com/classic/problems/random-one-question/all")
            soup = BeautifulSoup(resp.content)
            title = soup.head.title.text
            url = resp.url
            msg.sender.send(f"{title}\n{url}")

        elif str(msg.text).lower().find("testflight") >= 0 or str(msg.text).lower().endswith("tf"):
            resp = requests.get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/core/testflight.json")
            result = json.loads(s=resp.text)
            txt = "Testflight 列表: \n"
            for name, url in result.items():
                txt += f'{name} - {url} \n'
            msg.sender.send(txt)

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
        elif str(msg.text).find("冬瓜") > 5:
            text = f'别总叫冬瓜，冬瓜是你爸爸吗？'
            msg.sender.send(text)
        else:
            resp = requests.get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/core/AI.json")
            result = json.loads(s=resp.text)
            if type(result) is dict:
                for k, v in result.items():
                    if fetch(k):
                        msg.sender.send(v)
                        return
            random_answer(msg=msg)


def send_news():
    try:
        # 每日老司机周报
        contents = fetch_old_driver_list()
        group = bot.groups().search(u"Sepicat")[0]
        index = random.randint(0, len(contents) - 1)
        send_content = contents[index]
        title = send_content['title']
        while title.find('优惠') >= 0 or title.find('销售') >= 0 or title.find('内推') >= 0 or title.find('免费') >= 0:
            index = random.randint(0, len(contents) - 1)
            send_content = contents[index]
            title = send_content['title']
        text = "今日学习 \n\n"
        text += f'0x00 老司机周报随机文章：《{send_content["title"]}》\n'
        text += f'     {send_content["link"]}\n'

        t = Timer(10, send_news)
        t.start()

    except:
        host = bot.friends().search(u'冬瓜')[0]
        host.send(u'今天每日新闻发失败了')


def random_answer(msg):
    index = random.randint(1, 1)
    if index == 1:
        msg.sender.send("别整那些没用的，先把这题做出来")
        resp = requests.get("https://leetcode-cn.com/classic/problems/random-one-question/all")
        soup = BeautifulSoup(resp.content)
        title = soup.head.title.text
        url = resp.url
        msg.sender.send(f"{title}\n{url}")
    elif index == 2:
        car = [
            "zex-201",
            "SRS-022",
            "ABP-108",
            "ABP-119",
            "CHN-037",
            "ABP-138",
            "ABP-145",
            "MGSMPL-001",
            "ABP-159",
            "ABP-171",
            "ABP-178",
            "PPT-016",
            "PPT-018",
            "GNE-105",
            "KRV-001",
        ]
        s = random.randint(0, len(car) - 1)
        msg.sender.send(f"了解一下：{car[s]} ?? ")


send_news()
embed()
