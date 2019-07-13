from bs4 import BeautifulSoup
import feedparser
import ssl

feeds = None
rss_url = "https://github.com/SwiftOldDriver/iOS-Weekly/releases.atom"


def fetch_old_driver_list() -> dict:
    global feeds
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    p = feedparser.parse(rss_url)
    print(p)
    feed = p['feed']
    print("更新时间", feed['updated'])
    entries = p['entries']
    soup = BeautifulSoup(entries[0]['content'][0]['value'], 'html.parser')
    for i in soup.find_all('h3'):
        print(i)


if __name__ == '__main__':
    fetch_old_driver_list()
