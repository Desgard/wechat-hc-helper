import requests
from bs4 import BeautifulSoup


def strip_black(txt: str) -> str:
    res = ""
    for c in txt:
        if c != " ":
            res += c
    return res


def fetch_trending() -> []:
    resp = requests.get("https://github.com/trending")
    soup = BeautifulSoup(resp.content, "html.parser")

    box_eles = soup.find_all("article", class_="Box-row")
    res = []
    for index, box in enumerate(box_eles):
        desc = box.find('p').text.strip()
        name = strip_black(box.find('h1').text.strip())
        star_cnt = box.find('a', class_="muted-link d-inline-block mr-3").text.strip()
        link = "https://github.com/" + name
        print(index)
        print("仓库名", name)
        print("链接", link)
        print("描述", desc)
        print("✨", star_cnt)
        print("")
        current_res = {
            "desc": desc,
            "link": link,
            "name": name,
            "star": star_cnt,
        }
        res.append(current_res)
    return res


if __name__ == '__main__':
    fetch_trending()
