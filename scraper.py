import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from requests.exceptions import HTTPError,Timeout
from concurrent.futures import ThreadPoolExecutor
import re
import threading
import pandas as pd

class Scraper:
    def __init__(self):
        self.url_list = ["https://www.cnbc.com/select/where-to-find-use-college-student-discounts/", "https://www.collegedata.com/resources/study-break/best-student-discounts-to-use-in-college", "https://www.nbcnews.com/select/shopping/best-college-discounts-2026-rcna590001"]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        self.brand_titles = {}
        self.links_seen = set()
        self.lock = threading.Lock()

    
    def scrape(self, strong):
        raw_text = strong.get_text(strip = True).replace('\xa0', '').rstrip(":")
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', raw_text)
        text = cleaned_text.lower()
        if not text:
            return
        li = strong.find_parent('li')
        a = li.select_one('a[href]') if li else None
        if a is not None:
            href = a['href'].rstrip(")")
            params = parse_qs(urlparse(href).query)
            link = (params.get("url") or params.get("u") or params.get("d") or [href])[0]
            if link.startswith('https://'):
                res = self.dedup(link)
                if res == "new":
                    status, response = self.fetch(link)
                    self.store(text, link, status)
            else:
                self.store(text, None, None)
        else:
            self.store(text, None, None)
   
    def store(self, text, link, status):
        with self.lock:
            if text in self.brand_titles:
                if link is not None:
                    self.brand_titles[text]["link"].append(link)
                    self.brand_titles[text]["status"].append(status)
            else:
                if link is not None:
                    self.brand_titles[text] = {"link" : [link], "status" : [status]}
                else:
                    self.brand_titles[text] = {"link" : [], "status" : []}    

    def dedup(self, link):
        with self.lock:
            if link in self.links_seen:
                return "duplicate"
            else:
                self.links_seen.add(link)
                return "new"


    def fetch (self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout = (3,10))
            response.raise_for_status() 
        except Timeout as e:
            return (f"{type(e).__name__}", None)
        except HTTPError as e:
            return (f"{type(e).__name__}", None)
        except requests.exceptions.RequestException as e:
            return (f"{type(e).__name__}", None)
        return ("ok",response)

    def run(self):
        for i in range(len(self.url_list)):
            status, response = self.fetch(self.url_list[i])
            if status == "ok":
                soup = BeautifulSoup(response.text, "html.parser")
                list_strong = soup.select('li strong')
                with ThreadPoolExecutor(max_workers = 10) as executor:
                    results = list(executor.map(self.scrape, list_strong))
            time.sleep(1)
        
        flattened_data = pd.DataFrame.from_dict(self.brand_titles, orient = "index").explode(["link","status"])
        flattened_data['link'] = flattened_data['link'].fillna("No Link Supplied")
        flattened_data['status'] = flattened_data['status'].fillna("N/A")
        flattened_data.to_csv("discounts.csv", index_label = "brand")

scraper = Scraper()
scraper.run()


