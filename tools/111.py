import requests
from bs4 import BeautifulSoup
import time
import json
from pathlib import Path
from utils.crawler import build_url, load_json, load_html, fetch_soup, save_html
from utils.scraper import build_soup
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID


def make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def test():
    data = load_json("excel_functions.json")
    times = 1
    for item in data:
        name = item.get("func_name")
        uuid = item.get("func_uuid")
        soup = build_soup(uuid, make_url)

        print("=" * 60)
        print(f"{times}. {name}: ")
        times += 1

        # L26-34 逻辑
        # IF逻辑错误
        # 移除掉内部空格
        # 部分省略号需要处理
        b = soup.find_all('section', attrs={"class": "ocpSection"})
        c = soup.find_all('div', attrs={"class": "ocpSection"})
        result = ""
        for i in b + c:
            p_tag = i.find('p')
            if p_tag:
                p_text = p_tag.get_text(strip=True)
                if p_text.startswith(f"{name}(") or p_text.startswith(f"={name}(" or p_text.startswith(f"={name}B(")):
                    result = p_text
                    print(p_text)
                    break


        if result:
            pass
        else:
            # print(f"{times}. {name}: ")
            # print(len(b))
            # print(len(c))
            pass




if __name__ == "__main__":
    test()
