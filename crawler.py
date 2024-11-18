#-------------------------------------------------------------------------
# AUTHOR: Theo Nakfoor
# FILENAME: crawler.py
# SPECIFICATION: A simple program to crawl the CPP CS website to find the permanent faculty page. 
# FOR: CS 4250- Assignment #3
# TIME SPENT: 1h
#-----------------------------------------------------------*/

from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup

frontier = ["https://www.cpp.edu/sci/computer-science/"]

client = MongoClient("localhost", 27017)
db = client['local']
col = db['pages']

def storePage(url, html):
    col.update_one({"url": url}, { "$set": {
        "url": url,
        "html": html.decode('utf-8')
    }}, upsert=True)

def flagTargetPage(url):
    col.update_one({"url": url}, { "$set": {
        "target": True
    }})

def checkExists(url):
    results = col.find({"url": url})
    return len(list(results)) > 0

while len(frontier) > 0:

    url = frontier[0]
    print(f"Visiting: {url}")

    if not checkExists(url):
        html = urllib.request.urlopen(url).read()

        bs = BeautifulSoup(html, 'html.parser')

        storePage(url, html)

        # Check if page is target by looping thru h1 tags
        isTarget = False
        for tag in bs.find_all("h1"):
            if (tag['class'][0] == "cpp-h1") and tag.text == "Permanent Faculty":
                print("FOUND TARGET")
                isTarget = True
                break
        
        if(isTarget):
            flagTargetPage(url)
            frontier.clear()
            break
        else:
            for link in bs.find_all("a"):
                if(link.has_attr("href")):
                    if("https://" in link["href"]):
                        frontier.append(link["href"])
                    else:
                        frontier.append(f"https://www.cpp.edu/{link['href']}" if (link['href'][0] != "/") else f"https://www.cpp.edu{link['href']}")

    del frontier[0]