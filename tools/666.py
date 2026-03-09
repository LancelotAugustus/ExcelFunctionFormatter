import re

from utils.crawler import build_url, load_json, load_html, fetch_soup, save_html
from utils.scraper import build_soup
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID
from config import SPECIAL_SYNTAX_MAP


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

        # 将所有name文本转为大写
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        combined_text = pattern.sub(lambda m: m.group(0).upper(), combined_text)

        # 找到所有name文本，移除两端空格
        pattern = re.compile(r'\s*' + re.escape(name) + r'\s*', re.IGNORECASE)
        combined_text = pattern.sub(name, combined_text)

        # 找到第一个前面不为the的{name}(，移除所有在此之前的内容
        pattern = re.compile(r'(?<!the)' + re.escape(name) + r'\(', re.IGNORECASE)
        match = pattern.search(combined_text)
        if match:
            combined_text = combined_text[match.start():]
        else:
            paren_index = combined_text.find('(')
            combined_text = name + combined_text[paren_index:]

        # 移除所有右括号之后的文本
        right_paren_index = combined_text.find(')')
        combined_text = combined_text[:right_paren_index + 1]

        # 如果包含子串'lambda('，则在结尾补充一个右括号
        if 'lambda(' in combined_text:
            combined_text += ')'

        # 替换相关
        combined_text = combined_text.replace('((', '(')
        combined_text = combined_text.replace('-', '_')
        combined_text = combined_text.replace(' ', '')
        combined_text = combined_text.replace('\xa0', '')
        combined_text = combined_text.replace('…', '...')
        combined_text = combined_text.replace(',...', '...')
        combined_text = combined_text.replace('...', ',...')
        combined_text = combined_text.replace('...,', '...')

        # re.sub
        combined_text = re.sub(r'(?<!\[),(?=\[)', '', combined_text)
        combined_text = re.sub(r'(?<![(,])\[', ',[', combined_text)
        combined_text = re.sub(r'](?![),])', '],', combined_text)
        combined_text = re.sub(r'\(([^()]*)\)', lambda m: m.group().lower(), combined_text)

        print(f"{times}. {name}")
        print(combined_text)
        print("-" * 60)






if __name__ == '__main__':
    # local_test()
    test()
