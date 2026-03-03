import re

from utils.crawler import build_url, load_json, load_html, fetch_soup, save_html
from utils.scraper import build_soup
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID


def make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def test():
    data = load_json("excel_functions.json")
    for times, item in enumerate(data, 1):
        name = item.get("func_name")
        uuid = item.get("func_uuid")
        soup = build_soup(uuid, make_url)

        # 合并为空格分割的长字符串
        all_text = soup.get_text(separator=' ', strip=True)
        text_lines = all_text.split('\n')
        combined_text = ''.join(text_lines)

        # 找到第一个‘ Syntax ’移除掉所有在此之前的内容，并移除两端空格
        syntax_index = combined_text.find('Syntax')
        combined_text = combined_text[syntax_index + 6:].strip()

        # 如果首个字符为‘:'，则移除它
        if combined_text[0] == ":":
            combined_text = combined_text[1:].strip()

        # 在这里应该检查一次是否存在双语法情况
        if combined_text.startswith(name[: -1]):
            pass
        elif combined_text.startswith("="):
            pass
        else:
            print(f"{times}. {name}")
            print(combined_text[: 500])
            print("=" * 60)



        # # 将所有name文本转为大写
        # pattern = re.compile(re.escape(name), re.IGNORECASE)
        # combined_text = pattern.sub(lambda m: m.group(0).upper(), combined_text)
        #
        # # 找到所有name文本，移除两端空格
        # pattern = re.compile(r'\s*' + re.escape(name) + r'\s*', re.IGNORECASE)
        # combined_text = pattern.sub(name, combined_text)
        #
        # # 找到所有name+左括号文本，移除所有在此之前的内容，注意保留if，这是为了'XXXB'服务的
        # pattern = re.compile(re.escape(name) + r'\(', re.IGNORECASE)
        # match = pattern.search(combined_text)
        # if match:
        #     combined_text = combined_text[match.start():]
        #
        # # 移除所有右括号之后的文本
        # right_paren_index = combined_text.find(')')
        # combined_text = combined_text[:right_paren_index + 1]
        

        # print(f"{times}. {name}")
        # print(combined_text)
        # print("=" * 60)






if __name__ == '__main__':
    # local_test()
    test()
