import json
import re

from dataclasses import asdict

from excel_function import ExcelFunction
from config import SPECIAL_NAME_MAP, SPECIAL_UUID_MAP, SPECIAL_SYNTAX_MAP
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID, UUID_PATTERN
from utils.crawler import load_json, build_url, save_json
from utils.scraper import build_soup, get_text


def _make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def _get_syntax(func_name, func_uuid):
    soup = build_soup(func_uuid, _make_url)

    text = get_text(soup)
    text = text[text.find('Syntax'):]
    text = re.compile(rf'\s*{func_name}\s*', re.IGNORECASE).sub(func_name, text)
    text = text[re.compile(rf'(?<!the){func_name[:-1]}.?\(').search(text).start():]
    text = text[: text.find(')') + 1]
    text = f'{func_name}{text[text.find('('):]}'
    text = f'{text})' if 'lambda(' in text else text

    return text


def _clean_syntax(func_syntax):
    func_syntax = func_syntax.replace('((', '(')
    func_syntax = func_syntax.replace('-', '_')
    func_syntax = func_syntax.replace(' ', '')
    func_syntax = func_syntax.replace('…', '...')
    func_syntax = func_syntax.replace(',...', '...')
    func_syntax = func_syntax.replace('...', ',...')
    func_syntax = func_syntax.replace('...,', '...')

    func_syntax = re.sub(r'(?=\[)', '', func_syntax)
    func_syntax = re.sub(r'](?![),])', '],', func_syntax)
    func_syntax = re.sub(r'(?<![(,])\[', ',[', func_syntax)
    func_syntax = re.sub(r'\(([^()]*)\)', lambda m: m.group().lower(), func_syntax)

    return [func_syntax]


def _extract_excel_function_info():
    soup = build_soup(EXCEL_FUNCTIONS_UUID, _make_url)
    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows[1:]:
        cols = row.find_all('td')

        names = cols[0].find('a').get_text(strip=True)
        func_names = [func_name.strip() for func_name in names.split(',')]
        func_type = cols[1].find('b').get_text(strip=True)[: -1]
        func_desc = cols[1].get_text(strip=True)[len(func_type) + 1:]
        func_href = cols[0].find('a').get('href')
        func_uuid = UUID_PATTERN.search(func_href).group()

        for func_name in func_names:
            if func_name in SPECIAL_NAME_MAP:
                func_name = SPECIAL_NAME_MAP.get(func_name)
            if func_name in SPECIAL_UUID_MAP:
                func_uuid = SPECIAL_UUID_MAP.get(func_name)

            yield func_name, func_type, func_desc, func_uuid


def _extract_excel_function_detail(func_name, func_uuid):
    soup = build_soup(func_uuid, _make_url)
    spans = soup.find('section', attrs={"ms.cmpgrp": "applies_to"}).find_all('span')
    func_applies = []
    for span in spans:
        func_apply = span.get_text(strip=True)
        func_applies.append(func_apply)

    if func_name in SPECIAL_SYNTAX_MAP:
        func_syntax = SPECIAL_SYNTAX_MAP[func_name]
    else:
        func_syntax = _get_syntax(func_name, func_uuid)
        func_syntax = _clean_syntax(func_syntax)

    return func_applies, func_syntax


def _build_excel_function_list():
    functions = []
    for func_name, func_type, func_desc, func_uuid in _extract_excel_function_info():
        func_applies, func_syntax = _extract_excel_function_detail(func_name, func_uuid)
        excel_function = ExcelFunction(
            func_name=func_name,
            func_type=func_type,
            func_desc=func_desc,
            func_uuid=func_uuid,
            func_applies=func_applies,
            func_syntax=func_syntax
        )
        functions.append(excel_function)

    return functions


if __name__ == "__main__":
    import difflib

    funcs = _build_excel_function_list()
    json_data = [asdict(f) for f in funcs]

    # 保存成json
    # save_json(json_data, "excel_functions.json")

    json_read = load_json("excel_functions.json")

    if json_read == json_data:
        print("完全一致")
    else:
        json_read_str = json.dumps(json_read, indent=2, ensure_ascii=False)
        json_data_str = json.dumps(json_data, indent=2, ensure_ascii=False)

        diff = list(difflib.unified_diff(
            json_read_str.splitlines(keepends=True),
            json_data_str.splitlines(keepends=True),
            fromfile='本地JSON',
            tofile='生成JSON'
        ))

        if diff:
            print("存在差异：")
            print(''.join(diff))
        else:
            print("存在差异")

    print(f"本地json共有 {len(json_read)} 行.")
    print(f"生成json共有 {len(json_data)} 行.")
