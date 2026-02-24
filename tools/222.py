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
    aaaa = 0
    for item in data:
        name = item.get("func_name")
        uuid = item.get("func_uuid")
        soup = build_soup(uuid, make_url)

        text_node = soup.find(string=re.compile("Syntax"))
        if text_node:
            syntax_div = text_node.parent
            # print(syntax_div)
        else:
            print("=" * 60)
            print(f"{times}. {name}: ")
            aaaa += 1
            pass


        times += 1
    print(f"一共{aaaa}个未处理")



def local_test():
    uuid = "8f8ae884-2ca8-4f7a-b093-75d702bea31d"
    soup = build_soup(uuid, make_url)

    syntax_div = soup.find(['div', 'h2', 'b', 'p'], string=re.compile("Syntax"))
    print(syntax_div)

    if syntax_div:
        # current = syntax_div
        # while current.parent and current.parent.name != '[document]':
        #     for sibling in current.find_previous_siblings():
        #         sibling.decompose()
        #     current.parent.unwrap()
        # print(f"{times}. {name}: Processed")
        pass
    else:
        pass






if __name__ == '__main__':
    # local_test()
    test()