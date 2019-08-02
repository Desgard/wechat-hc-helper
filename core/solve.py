from wxpy import *
from .bytedance import valid_bytedance_jd_query, query_bytedance_jd
from .github import fetch_trending
from .old_driver import fetch_old_driver_list
from .awesome_tips import fetch_awesome_tips_list
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

guagua = bot.friends().search("冬瓜")


@bot.register(guagua, msg_types=TEXT)
def _111(msg):
    if str(msg.text).lower() == "guaguagua":
        send_news(group_name="一瓜共识")
        msg.sender.send("每日一题发送成功")
    elif str(msg.text).lower() == "guaguagua_test":
        send_news(group_name="Sepicat")
        msg.sender.send("每日一题发送成功")



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
        elif str(msg.text).lower().find("g-driver") or str(msg.text).lower().find("老司机") >= 0:
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

        elif str(msg.text).find("知识小集") >= 0:
            res: list = fetch_awesome_tips_list()
            index = random.randint(1, len(res) - 1)
            text = "那就给你来一个😎\n"
            text += f'{res[index]["title"]}\n{res[index]["link"]}'
            msg.sender.send(text)

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


def send_news(group_name: str):
    try:
        # 每日老司机周报
        contents = fetch_old_driver_list()
        group = bot.groups().search(group_name)[0]
        index = random.randint(0, len(contents) - 1)
        send_content = contents[index]
        title = send_content['title']
        while title.find('优惠') >= 0 or title.find('销售') >= 0 or title.find('内推') >= 0 or title.find('免费') >= 0:
            index = random.randint(0, len(contents) - 1)
            send_content = contents[index]
            title = send_content['title']

        note = ' - test' if group_name == 'Sepicat' else ''
        text = f"今日学习 {note}\n\n"
        text += f'0x00 老司机周报随机文章\n《{send_content["title"]}》\n'
        text += f'{send_content["link"]}\n\n'

        # 每日一题
        text += "0x01 每日一题\n"
        resp = requests.get("https://leetcode-cn.com/classic/problems/random-one-question/all")
        soup = BeautifulSoup(resp.content)
        title = soup.head.title.text
        url = resp.url
        text += f'《{title}》\n'
        text += f'{url}\n\n'

        # 知识小集
        text += "0x02 知识小集\n"
        res: list = fetch_awesome_tips_list()
        index = random.randint(1, len(res) - 1)
        text += f'《{res[index]["title"]}》\n{res[index]["link"]}'

        group.send(text)

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


embed()
