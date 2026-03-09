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
        text = text[text.find('Syntax'):]
        text = re.compile(rf'\s*{func_name}\s*', re.IGNORECASE).sub(func_name, text)

        match = re.compile(rf'(?<!the){func_name[:-1]}.\(').search(text)
        if match:
            text = text[match.start():]
        else:
            text = func_name + text[text.find('('):]

        text = text[: text.find(')') + 1]
        text = f'{text})' if 'lambda(' in text else text

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
    return [syntax_string]


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
