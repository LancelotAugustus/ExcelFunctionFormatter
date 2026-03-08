import re

from utils.crawler import build_url, load_json, load_html, fetch_soup, save_html
from utils.scraper import build_soup
from config import BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, EXCEL_FUNCTIONS_UUID
from config import SPECIAL_SYNTAX_MAP


def make_url(uuid):
    url = build_url(BASE_DOMAIN, LANGUAGE_CODE, PRODUCT_SEGMENT, uuid)
    return url


def extract_function_syntax(soup, name):
    text = soup.get_text(separator=' ', strip=True).replace('\n', '')
    
    syntax_idx = text.find('Syntax')
    text = text[syntax_idx + 6:].strip().lstrip(':').strip()
    
    text = re.sub(re.escape(name), lambda m: m.group(0).upper(), text, flags=re.IGNORECASE)
    text = re.sub(rf'\s*{re.escape(name)}\s*', name, text, flags=re.IGNORECASE)
    
    if match := re.search(rf'{re.escape(name)}\(', text, re.IGNORECASE):
        text = text[match.start():]
    
    text = text[:text.find(')') + 1]
    text = re.sub(r'\(\(', '(', text)
    
    text = text.replace(' ', '').replace('\xa0', '')
    
    if 'lambda(' in text:
        text += ')'
    
    text = re.sub(r'(?<!\[),(?=\[)', '', text)
    text = re.sub(r'(?<![(,])\[', ',[', text)
    text = re.sub(r'\(([^()]*)\)', lambda m: f'({m.group(1).lower()})', text)
    
    return text.replace('-', '_').replace('defaultorvalue', 'default_or_value')


def test():
    data = load_json("excel_functions.json")
    for times, item in enumerate(data, 1):
        name = item.get("func_name")
        uuid = item.get("func_uuid")
        soup = build_soup(uuid, make_url)

        combined_text = extract_function_syntax(soup, name)

        print(f"{times}. {name}")
        print(combined_text)
        print("-" * 60)


if __name__ == '__main__':
    test()
