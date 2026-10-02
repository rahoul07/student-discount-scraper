import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class Scraper:
    def __init__(self):
        self.url_list = ["https://www.cnbc.com/select/where-to-find-use-college-student-discounts/", "https://www.collegedata.com/resources/study-break/best-student-discounts-to-use-in-college", "https://www.nbcnews.com/select/shopping/best-college-discounts-2026-rcna590001"]
        self.soup_list = [None] * len(self.url_list)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        self.brand_titles = {}
    
    def scrape(self, list_strong):
        for strong in list_strong:
            text = strong.get_text(strip = True).replace('\xa0', '').rstrip(":")
            if not text:
                continue
            li = strong.find_parent('li')
            a = li.select_one('a[href]') if li else None
            if a is not None:
                href = a['href'].rstrip(")")
                params = parse_qs(urlparse(href).query)
                link = (params.get("url") or params.get("u") or params.get("d") or [href])[0]
                if link.startswith('https://'):
                    print(f"{text}: {link}")
                else:
                    print(f"{text}: No Link Supplied")
                self.brand_titles[text] = link
            else:
                print(f"{text}: No Link Supplied")
                self.brand_titles[text] = None
            print()
        time.sleep(1)

    # def test_links (self):
        

    def run(self):
        for i in range(len(self.url_list)):
            print(self.url_list[i])
            response = requests.get(self.url_list[i], headers=self.headers)
            self.soup_list[i] = BeautifulSoup(response.text, "html.parser")
            list_strong = self.soup_list[i].select('li strong')
            self.scrape(list_strong)
scraper = Scraper()
scraper.run()


