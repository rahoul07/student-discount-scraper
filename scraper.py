import requests
import time
from bs4 import BeautifulSoup

url_list = ["https://www.cnbc.com/select/where-to-find-use-college-student-discounts/", "https://www.collegedata.com/resources/study-break/best-student-discounts-to-use-in-college", "https://www.nbcnews.com/select/shopping/best-college-discounts-2026-rcna590001"]
soup_list = [None] * len(url_list)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
brand_titles  = set()
for i in range(len(url_list)):
    response = requests.get(url_list[i], headers=headers)
    soup_list[i] = BeautifulSoup(response.text, "html.parser")
    list_strong = soup_list[i].select('li strong')
    deals = []
    num = 0
    for strong in list_strong:
        length = len(brand_titles)
        text = strong.get_text(strip = True).replace('\xa0', '')
        if text == ":":
            continue
        num += 1
        if text == "Carnegie Hall":
            continue
        brand_titles.add(text)
        if len(brand_titles) > length:
            print(text)
            print()
    time.sleep(1)
    

