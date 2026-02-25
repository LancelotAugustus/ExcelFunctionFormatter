import re

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

        text_node = soup.find(string=re.compile("Syntax"))
        syntax_div = text_node.parent.parent
        current = syntax_div
        while current.parent and current.parent.name != '[document]':
            for sibling in current.find_previous_siblings():
                sibling.decompose()
            current.parent.unwrap()
        print(f"{times}. {name}:")
        print(f"{current}")
        print("="*60)

        times += 1






if __name__ == '__main__':
    # local_test()
    test()