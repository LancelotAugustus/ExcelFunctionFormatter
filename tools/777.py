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
        name = item["func_name"]
        uuid = item["func_uuid"]
        soup = build_soup(uuid, make_url)

        all_text = soup.get_text(separator=' ', strip=True)
        combined_text = ''.join(all_text.split('\n'))

        syntax_index = combined_text.find('Syntax')
        combined_text = combined_text[syntax_index + 6:].lstrip()
        combined_text = combined_text[1:].lstrip() if combined_text[0] == ":" else combined_text

        combined_text = re.sub(re.escape(name), lambda m: m.group().upper(), combined_text, flags=re.IGNORECASE)
        combined_text = re.sub(r'\s*' + re.escape(name) + r'\s*', name, combined_text, flags=re.IGNORECASE)

        pattern = re.compile(r'(?<!the)' + re.escape(name) + r'\(', re.IGNORECASE)
        match = pattern.search(combined_text)
        if match:
            combined_text = combined_text[match.start():]
        else:
            combined_text = name + combined_text[combined_text.find('('):]

        combined_text = combined_text[:combined_text.find(')') + 1]
        combined_text += ')' if 'lambda(' in combined_text else ''

        replacements = {
            '((': '(', '-': '_', ' ': '', '\xa0': '', '…': '...',
            ',...': '...', '...': ',...', '...,': '...'
        }
        for old, new in replacements.items():
            combined_text = combined_text.replace(old, new)

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
