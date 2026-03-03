import re

from utils.crawler import build_url, load_json, load_html, fetch_soup, save_html
from utils.scraper import build_soup
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID


def make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def test():
    data = load_json("excel_functions.json")
    count_zero = 0
    count_one = 0
    count_other = 0
    for times, item in enumerate(data, 1):
        name = item.get("func_name")
        uuid = item.get("func_uuid")
        soup = build_soup(uuid, make_url)

        escaped_name = re.escape(name)
        escaped_name_trimmed = re.escape(name[:-1]) if name else ""
        pattern = rf'(?:=)?(?:{escaped_name}|{escaped_name_trimmed})\(.*\)'

        matches = soup.find_all(string=re.compile(pattern))
        text_node = []
        for m in matches:
            m = m.strip()
            if any(op in m for op in '+-*/'):
                continue
            # if re.search(r'[A-Z]+\d+', m):
            #     continue
            # if re.search(r'\(\d+\)', m):
            #     continue
            # if re.search(r'[a-z] [a-z]', m):
            #     continue

            text_node.append(m.strip())

        if len(text_node) != 1:
            print(f"{times}. {name} (Length {len(text_node)}):")
            print(text_node)
            print("=" * 60)

        if len(text_node) == 0:
            count_zero += 1
        elif len(text_node) == 1:
            count_one += 1
        else:
            count_other += 1

    print(f"长度0: {count_zero}, 长度1: {count_one}, 其他: {count_other}")



if __name__ == '__main__':
    # local_test()
    test()
