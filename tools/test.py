import requests
from bs4 import BeautifulSoup



def test():
    url = "https://support.microsoft.com/en-us/office/sequence-function-57467a98-57e0-4817-9f14-2eb78519ca90" # MID
    # url = "https://support.microsoft.com/en-us/office/abs-function-3420200f-5628-4e8c-99da-c99d7c87713c" # ABS
    print(f"Fetching data from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # 目前相对稳定
    # spans = soup.find('section', attrs={"ms.cmpgrp": "applies_to"}).find_all('span')
    # print(spans)
    # for span in spans:
    #     print(span.get_text(strip=True))

    # 重新处理
    name = "SEQUENCE"
    b = soup.find_all('section', attrs={"class": "ocpSection"})
    c = soup.find_all('div', attrs={"class": "ocpSection"})
    for i in b + c:
        if i.find('p').get_text(strip=True).startswith(f"{name}(") or i.find('p').get_text(strip=True).startswith(f"={name}("):
            print("__________________________")
            print(i.find('p').get_text(strip=True))
            print("__________________________")
            continue
        else:
            print("==========================")
            print(i)
            print("==========================")




if __name__ == "__main__":
    test()
