#-------------------------------------------------------------------------
# AUTHOR: Theo Nakfoor
# FILENAME: parser.py
# SPECIFICATION: A simple program to parse professor information from the CPP permament faculty website (target page).
# FOR: CS 4250- Assignment #3
# TIME SPENT: 45m
#-----------------------------------------------------------*/

from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient("localhost", 27017)

db = client['local']
pages = db['pages']
professors = db['professors']

result = pages.find_one({"target": True})
bs = BeautifulSoup(result["html"], 'html.parser')

tiles = bs.find_all("div", class_="clearfix")
for tile in tiles:

    titles = tile.find_all("h2")
    for title in titles:

        data = {}
        data['name'] = str(title.text).strip()

        for strong in title.next_element.next_element.next_element.find_all("strong"):
            try:
                parsedText = strong.text.strip().replace(":", "")
                if(parsedText == "Title"):
                    data["title"] = str(strong.next_element.next_element).strip()
                elif(parsedText == "Office"):
                    data["office"] = str(strong.next_element.next_element).strip()
                elif(parsedText == "Phone"):
                    data["phone"] = str(strong.next_element.next_element).strip()
                elif(parsedText == "Email"):
                    data["email"] = str(strong.next_element.next_element.next_element.text).strip()
                elif(parsedText == "Web"):
                    data["website"] = str(strong.next_element.next_element.next_element['href']).strip()
            except Exception:
                continue

        professors.update_one({"name": data["name"]}, { "$set": data}, upsert=True)