# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from bs4 import BeautifulSoup
import re
import argparse
import yaml
import os

#%% argument parser

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--yaml")
args = parser.parse_args()

f = open(args.yaml, "r", encoding="utf8")
data = yaml.safe_load(f)
f.close()

driver_path = data["driver_path"]
search = data["search"]
text_directory = data["text_directory"]
html_directory = data["html_directory"]

for i in [text_directory, html_directory]:
    if not os.path.exists(i):
        os.makedirs(i)


#%% selenium get the links

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(driver_path, options=chrome_options) 

# driver configuration and some variables for the loop.
time.sleep(2)  
scroll_pause_time = 2 
screen_height = driver.execute_script("return window.screen.height;")   
i = 1

# you need tripple quotes to properly print such text as text
website = f"""{search}"""

driver.get(website)

while True:
  #page_sourcel one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

# Once the page has scrolled to the bottom, all cases are "in" We can get the whole page as html
html = driver.page_source
f.close()
# Don't forget to shut down selenium!
driver.close()

#%%

# Parsing html with BS4, save results to DataFrame
mysoup = BeautifulSoup(html, "html.parser")
casenames = mysoup.find_all(class_ ="document-link headline")
rawresults = pd.DataFrame({"rawres":casenames})

#%%


case_titles = []
for i in rawresults.rawres:
    smallsoup = BeautifulSoup(str(i), "html.parser")
    temp = smallsoup.text
    case_titles.append(temp)

pattern = re.compile(r"href='.+'")
href = []
for i in rawresults.rawres:
    temp = re.findall(pattern, str(i))
    href.append(temp)
    

pattern = re.compile(r"\d+-\d+")
itemid = []
for i in rawresults.rawres:
    temp = re.findall(pattern, str(i))
    itemid.append(temp[0])


df = pd.DataFrame({"casename":case_titles, "href":href, "itemid":itemid})


#%%

target = list(df.itemid)



for i in target:
    try:
        driver = webdriver.Chrome(driver_path, options=chrome_options) 
        driver.get(f'https://hudoc.echr.coe.int/eng#{{"itemid":["{i}"]}}')
        time.sleep(2)
        html = driver.page_source
        x = open(f"{html_directory}{i}.txt", "w", encoding="Utf8")
        x.write(html)
        f.close()
        soup = BeautifulSoup(html, "html.parser")
        f = open(f"{text_directory}{i}.txt", "w", encoding="utf8")
        f.write(soup.text)
        f.close()
        driver.close()
    except:
        print(f"something went wrong with {i}")
        driver.close()
    

