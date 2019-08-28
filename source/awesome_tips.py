from bs4 import BeautifulSoup
import feedparser
import ssl
import datetime

feeds = None
rss_url = "https://577528249.github.io/search.xml"
host = "https://577528249.github.io"


def get_current_month_day(currentday):
    currentMonth = currentday.strftime('%m')
    currentYear = currentday.strftime('%Y')
    d1 = datetime.datetime(int(currentYear),int(currentMonth),1)
    d2 = datetime.datetime(int(currentYear),int(currentMonth)+1,1)
    days = d2 - d1
    day = days.days
    return datetime.date(int(currentYear),int(currentMonth),1),\
           datetime.date(int(currentYear),int(currentMonth),day)


def resolve(item: dict) -> dict:
    res = {}
    if "title" in item.keys():
        res["title"] = item["title"]
    if "links" in item.keys():
        res["link"] = item["links"][0]['href']
    return res


def fetch_awesome_tips_list() -> list:
    global feeds
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    p = feedparser.parse(rss_url)
    # print(p['entries'][0]["links"][0]['href'])
    # print(len(p['entries']))
    return list(map(resolve, p['entries']))


if __name__ == '__main__':
    res = fetch_awesome_tips_list()
    print(res)
