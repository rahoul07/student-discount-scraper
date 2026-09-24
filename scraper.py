import requests
import time
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.url_list = ["https://www.cnbc.com/select/where-to-find-use-college-student-discounts/", "https://www.collegedata.com/resources/study-break/best-student-discounts-to-use-in-college", "https://www.nbcnews.com/select/shopping/best-college-discounts-2026-rcna590001"]
        self.soup_list = [None] * len(self.url_list)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        self.brand_titles = set()
    
    def scrape(self, list_strong, brand_titles):
        deals = []
        num = 0
        for strong in list_strong:
            length = len(brand_titles)
            text = strong.get_text(strip = True).replace('\xa0', '')
            if text == ":":
                continue
            num += 1
            brand_titles.add(text)
            if len(brand_titles) > length:
                print(text)
                print()
        time.sleep(1)
    
    def run(self):
        for i in range(len(self.url_list)):
            response = requests.get(self.url_list[i], headers=self.headers)
            self.soup_list[i] = BeautifulSoup(response.text, "html.parser")
            list_strong = self.soup_list[i].select('li strong')
            self.scrape(list_strong, self.brand_titles)
scraper = Scraper()
scraper.run()


