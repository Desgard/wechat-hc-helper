from wxpy import *
from source.bytedance import valid_bytedance_jd_query, query_bytedance_jd
from source.github import fetch_trending
from source.old_driver import fetch_old_driver_list
from source.awesome_tips import fetch_awesome_tips_list
from log import logger
from bs4 import BeautifulSoup

import random

import requests
import json
import re


GROUP_NAME = "Sepicat"
bot = Bot(console_qr=True, cache_path=True)
friends = bot.friends
guagua = bot.friends().search("冬瓜")

related_group: Group = None
if len(bot.groups().search(GROUP_NAME)) > 0:
    related_group = bot.groups().search(GROUP_NAME)[0]


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

        elif str(msg.text).lower().find("算法打卡") >= 0:
            logger.log("打卡操作，写数据库")

            pass

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
        elif str(msg.text).lower().find("g-driver") >= 0 or str(msg.text).lower().find("老司机") >= 0:
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
            resp = requests\
                .get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/source/testflight.json")
            result = json.loads(s=resp.text)
            txt = "Testflight 列表: \n"
            for name, url in result.items():
                txt += f'{name} - {url} \n'
            msg.sender.send(txt)

        elif str(msg.text).find("我要学习") >= 0:
            resp = requests.get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/source/study.json")
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
            resp = requests.get("https://raw.githubusercontent.com/Desgard/wechat-hc-helper/master/source/AI.json")
            result = json.loads(s=resp.text)
            if type(result) is dict:
                for k, v in result.items():
                    if fetch(k):
                        msg.sender.send(v)
                        return


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
        soup = BeautifulSoup(resp.content, "html.parser")
        title = soup.head.title.text
        url = resp.url
        text += f'《{title}》\n'
        text += f'{url}\n\n'

        # 极客时间红包
        text += "0x02 每日福利\n"
        text += "极客时间打卡红包\n"
        text += "https://promo.geekbang.org/activity/v2/checkin"

    except:
        host = bot.friends().search(u'冬瓜')[0]
        host.send(u'今天每日新闻发失败了')


embed()
