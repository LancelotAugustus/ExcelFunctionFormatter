import json
import requests
from bs4 import BeautifulSoup


def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def save_html(soup, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_url(*parts):
    url = "https://" + "/".join(str(part) for part in parts)
    return url


def fetch_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
