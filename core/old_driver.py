from bs4 import BeautifulSoup
import feedparser
import ssl

feeds = None
rss_url = "https://github.com/SwiftOldDriver/iOS-Weekly/releases.atom"


def fetch_old_driver_list() -> list:
    global feeds
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    p = feedparser.parse(rss_url)
    # print(p)
    feed = p['feed']
    print("更新时间", feed['updated'])
    entries = p['entries']
    soup = BeautifulSoup(entries[0]['content'][0]['value'], 'html.parser')
    h3s = soup.find_all('h3')
    result = []
    for article in h3s:
        current_a = article.find('a')
        if current_a is None: 
            continue
        current_info = {
            'updated': feed['updated'],
            'title': article.text,
            'link': current_a['href'],
        }
        result.append(current_info)
    return result

if __name__ == '__main__':
    res = fetch_old_driver_list()
    print(res)
