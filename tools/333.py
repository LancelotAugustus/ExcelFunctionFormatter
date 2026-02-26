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
    a = 0
    for item in data:
        name = item.get("func_name")
        uuid = item.get("func_uuid")
        soup = build_soup(uuid, make_url)

        b = name + r"\("
        c = name[: -1] + r"\("
        d = name + r"("
        e = name[: -1] + r"("
        f = "=" + name + r"("
        g = "=" + name[: -1] + r"("

        text_1 = soup.find_all(string=re.compile(b))
        text_2 = soup.find_all(string=re.compile(c))
        output = []
        for i in text_1 + text_2:
            j = i.strip()
            if j.startswith(d) or i.startswith(e) or i.startswith(f) or i.startswith(g):
                output.append(j)

        if output:
            text_node = output[0]
        else:
            text_node = None


        if text_node is not None:
            print(f"{times}. {name}:")
            print(f"{text_node}")
            print("="*60)
            pass
        else:
            # a = a + 1
            # print(f"{times}. {name}:")
            # print(f"{text_node}")
            # print("=" * 60)
            pass

        times += 1
    print(a)


if __name__ == '__main__':
    # local_test()
    test()
