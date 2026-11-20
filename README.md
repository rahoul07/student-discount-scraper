# Student Discount Scraper

Finds brands on the internet that offer discounts to college students by scraping a set amount of sites. This started as a small resume-builder project and kept growing as new problems came up.

How it works
- Threading: it runs 10 threads at once, and each one works on a different link from the sites. This brought the runtime down from about 10 minutes to about 2.
- Locks: with multiple threads saving results at the same time I ran into a race condition, so I used locks to fix it.
- Error handling: every link goes through a try/except that catches HTTP errors, timeouts and anything else that goes wrong when opening it, so one broken link doesn't kill the whole run.
- Affiliate links: you can't open these directly, so I parse the HTML to find where they actually go, then run them through the same try/except process.
- Dedupe: removes repeat brands before saving.

 Output
All the data gets saved into a dictionary with the brand names, links and statuses, then written to a CSV. `discounts.csv` in this repo is an example of the output.

 How to run
pip install -r requirements.txt
python scraper.py

 What's next
- Add more sites
- Web crawler instead of a scraper
- Eventually turn this into a free-deals app for students
