from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os
from datetime import datetime
import pandas as pd
today = datetime.today().date()

driver = webdriver.Safari()

base_dir = f"Data/{today}"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

file_path_csv = os.path.join(base_dir, f"{today}_links.csv")

file_path_html = os.path.join(base_dir, f"{today}_rank_list.html")

url = "https://www.bilibili.com/v/popular/rank/all/"
driver.get(url)


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rank-list-wrap")))
html_source = driver.page_source
driver.quit()


soup = BeautifulSoup(html_source, "html.parser")
ranklst = soup.find("div", class_="rank-list-wrap")

all_videos=ranklst.findAll("a",class_="title")
all_links=[]
with open(file_path_html, "w", encoding="utf-8") as file:
    for i in all_videos:
        file.write(i.prettify())
for  video in all_videos:
    all_links.append("https:"+video["href"])
cnt=0
for i in all_videos:
    all_videos[cnt]=i.get_text(strip=True)
    cnt+=1

all_uploader=soup.findAll("span", class_="data-box up-name")
cnt=0

for i in all_uploader:
    all_uploader[cnt]=i.get_text(strip=True)
    cnt+=1
today = datetime.today().strftime('%Y-%m-%d')


   

df = pd.DataFrame({
    "标题":all_videos,
    "Up主":all_uploader,
    "URL链接": all_links
})
df.to_csv(file_path_csv, index=False)
'''
with open(file_path_csv, "w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "URL"])  # Write header
    for video in all_videos:
        title = video.get_text(strip=True)
        href = "https:"+video['href']
        writer.writerow([title, href])
        '''

