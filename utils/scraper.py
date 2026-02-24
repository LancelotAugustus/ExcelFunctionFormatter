from bs4 import BeautifulSoup
from pathlib import Path

from utils.crawler import load_html, save_html, fetch_soup


def get_cache(identifier):
    cache_dir = Path(__file__).parent.parent / "cache"
    cache_dir.mkdir(exist_ok=True)
    file_path = cache_dir / f"{identifier}.html"
    return file_path


def build_soup(identifier, url_maker):
    file_path = get_cache(identifier)
    if file_path.exists():
        data = load_html(file_path)
        soup = BeautifulSoup(data, 'html.parser')
    else:
        url = url_maker(identifier)
        soup = fetch_soup(url)
        save_html(soup, file_path)
    return soup
