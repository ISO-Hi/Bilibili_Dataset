from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import pandas as pd
from bilibili_api import video, sync
from datetime import datetime

from getlink import file_path_csv
from getlink import base_dir


links = []
plays_num=[]
description=[]
bullet_comments_num=[]
likes_num=[]
coin_num=[]
fav_num=[]
share_num=[]
tags=[]
with open(file_path_csv, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        links.append(row[2])
driver = webdriver.Safari()
for i in range (100):
    
    #获取弹幕文件
    v = video.Video(bvid=links[i][-12:])
    try:
        dms = sync(v.get_danmakus(0))
        print("success_"+links[i][-12:])
    except KeyError:
        dms = []
        print("KE")
    with open(base_dir+"/"+links[i][-12:]+".txt", "w", encoding="utf-8") as file:
        for dm in dms:
            file.write(str(dm)+'\n')
    time.sleep(20)
   
    
    url = links[i]
    driver.get(url)
   
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "video-share-info-text"))) 
    #time.sleep(5)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    #获取播放量
    element=soup.find("div",class_="view-text")
    if element:
        plays_num.append(element.get_text(strip=True))
    else:
        plays_num.append("Not Found")
    #获取弹幕量
    element=soup.find("div", class_="dm-text")
    if element:
        bullet_comments_num.append(element.get_text(strip=True))
    else:
        bullet_comments_num.append("Not Found")
    #获取简介
    element = soup.find("span", class_="desc-info-text")
    if element:
        description.append(element.get_text(strip=True))
    else:
        description.append("Not Found")

    #获取点赞量
    element=soup.find("span", class_="video-like-info video-toolbar-item-text")
    if element:
        likes_num.append(element.get_text(strip=True))
    else:
        likes_num.append("Not Found")
    #获取投币量
    element=soup.find("span", class_="video-coin-info video-toolbar-item-text")
    if element:
        coin_num.append(element.get_text(strip=True))
    else:
        coin_num.append("Not Found")

    #获取收藏量
    element=soup.find("span", class_="video-like-info video-toolbar-item-text")
    if element:
        fav_num.append(element.get_text(strip=True))
    else:
        fav_num.append("Not Found")
    #获取分享量
    element=soup.find("span", class_="video-share-info-text")
    if element:
        share_num.append(element.get_text(strip=True))
    else:
        share_num.append("Not Found")
    #获取分区
    element=soup.find("a", class_="tag-link")
    tag=[]
    if element:
        tag=soup.findAll("a", class_="tag-link")
        cnt=0
        for j in tag:
            tag[cnt]=j.get_text(strip=True)
            cnt+=1
    else:
        tag=["Not Found"]

    tags.append(tag)
   
driver.quit()
#print(tags)
#print(share_num)

df = pd.read_csv(file_path_csv)
df["播放量"] = plays_num
df["弹幕量"] = bullet_comments_num
df["简介"]= description
df["点赞量"]=likes_num
df["投币量"]=coin_num
df["收藏量"]=fav_num
df["分享量"]=share_num
df["分区"]=tags

df.to_csv(file_path_csv, index=False)



''' 
driver = webdriver.Safari()
plays_num=[]
for i in links:
    v = video.Video(bvid=i[-12:])
    dms = sync(v.get_danmakus(0))
    with open(os.path.join(base_dir, f"{i[-12:]}_danmu.txt"), "w", encoding="utf-8") as file:
        for dm in dms:
            file.write(str(dm)+'\n')
    
    url = i
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "view-text")))
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    plays_num.append(soup.find("div",class_="view-text"))
    '''

   

#driver.quit()
#print(plays_num)



