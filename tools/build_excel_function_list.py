import json
from dataclasses import asdict

from excel_function import ExcelFunction
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID, UUID_PATTERN, SPECIAL_UUID_MAP
from utils.crawler import load_json, build_url, save_json
from utils.scraper import build_soup


def make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def _extract_excel_function_info(soup):
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
            # if func_name in SPECIAL_UUID_MAP:
            #     func_uuid = SPECIAL_UUID_MAP.get(func_name)
            if func_name == 'FORECAST.ETS':
                func_uuid = '15389b8b-677e-4fbd-bd95-21d464333f41'
            if func_name == 'FORECAST.ETS.CONFINT':
                func_uuid = '6d4a7557-11fa-4678-9e6a-dbcc31a7c7df'
            if func_name == 'FORECAST.ETS.SEASONALITY':
                func_uuid = '32a27a3b-d22f-42ce-8c5d-ef3649269f3c'
            if func_name == 'FORECAST.ETS.STAT':
                func_uuid = '60f2ae14-d0cf-465e-9736-625ccaaa60b4'
            if func_name == 'FORECAST.LINEAR':
                func_uuid = '50ca49c9-7b40-4892-94e4-7ad38bbeda99'

            yield func_name, func_type, func_desc, func_uuid


def _extract_excel_function_detail(soup):
    spans = soup.find('section', attrs={"ms.cmpgrp": "applies_to"}).find_all('span')
    func_applies = []
    for span in spans:
        func_apply = span.get_text(strip=True)
        func_applies.append(func_apply)

    return func_applies


def _build_excel_function_list():
    soup = build_soup(EXCEL_FUNCTIONS_UUID, make_url)

    functions = []
    for func_name, func_type, func_desc, func_uuid in _extract_excel_function_info(soup):
        excel_function = ExcelFunction(
            func_name=func_name,
            func_type=func_type,
            func_desc=func_desc,
            func_uuid=func_uuid
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
