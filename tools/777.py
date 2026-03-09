import re

from utils.crawler import build_url, load_json, load_html, fetch_soup, save_html
from utils.scraper import build_soup, get_text
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID
from config import SPECIAL_SYNTAX_MAP


def make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def _get_syntax_string(func_name, func_uuid):
        soup = build_soup(func_uuid, make_url)
        text = get_text(soup)

        # 找到第一个‘ Syntax ’移除掉所有在此之前的内容，并移除两端空格
        syntax_index = text.find('Syntax')
        text = text[syntax_index:]

        # 找到所有name文本，移除两端空格
        pattern = re.compile(r'\s*' + re.escape(func_name) + r'\s*', re.IGNORECASE)
        text = pattern.sub(func_name, text)

        # 找到第一个前面不为the的{name}(，移除所有在此之前的内容
        pattern = re.compile(r'(?<!the)' + re.escape(func_name) + r'\(', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            text = text[match.start():]
        else:
            paren_index = text.find('(')
            text = func_name + text[paren_index:]

        # 移除所有右括号之后的文本
        right_paren_index = text.find(')')
        text = text[:right_paren_index + 1]

        # 如果包含子串'lambda('，则在结尾补充一个右括号
        if 'lambda(' in text:
            text += ')'

        return text


def _clean_syntax_string(syntax_string):
    # 替换相关
    syntax_string = syntax_string.replace('((', '(')
    syntax_string = syntax_string.replace('-', '_')
    syntax_string = syntax_string.replace(' ', '')
    syntax_string = syntax_string.replace('…', '...')
    syntax_string = syntax_string.replace(',...', '...')
    syntax_string = syntax_string.replace('...', ',...')
    syntax_string = syntax_string.replace('...,', '...')

    # re.sub
    syntax_string = re.sub(r'(?<!\[),(?=\[)', '', syntax_string)
    syntax_string = re.sub(r'(?<![(,])\[', ',[', syntax_string)
    syntax_string = re.sub(r'](?![),])', '],', syntax_string)
    syntax_string = re.sub(r'\(([^()]*)\)', lambda m: m.group().lower(), syntax_string)
    return syntax_string


def test():
    data = load_json("excel_functions.json")
    for times, item in enumerate(data, 1):
        func_name = item.get("func_name")
        func_uuid = item.get("func_uuid")

        if func_name in SPECIAL_SYNTAX_MAP:
            syntax_string = SPECIAL_SYNTAX_MAP[func_name]
        else:
            syntax_string = _get_syntax_string(func_name, func_uuid)
            syntax_string = _clean_syntax_string(syntax_string)

        print(f"{times}. {func_name}")
        print(syntax_string)
        print("-" * 60)






if __name__ == '__main__':
    # local_test()
    test()
