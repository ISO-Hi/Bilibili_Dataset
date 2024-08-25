
import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import pandas as pd
import re
from bilibili_api import video, sync
from datetime import datetime

from getlink import file_path_csv
from getlink import base_dir


 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
links = []
plays_num=[]
description=[]
bullet_comments_num=[]
likes_num=[]
coin_num=[]
fav_num=[]
share_num=[]
tags=[]
date=[]
with open(file_path_csv, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        links.append(row[2])
for i in range (100):
    
    url = links[i]
    video_request = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(video_request.text, "html.parser")
    if True:
        
        #获取弹幕文件
        # 查找包含 'window.__playinfo__' 的 <script> 标签
        script_tag = soup.find("script", string=lambda t: t and "window.__playinfo__" in t)
        if script_tag:

            script_content = script_tag.string
            base_url_match = script_content[script_content.find("baseUrl")+10:script_content.find("baseUrl")+1000]
            #print(base_url_match)
        
            cid=base_url_match.split('/')[6]
            
            

                #print(f"Found CID: {cid}")

                # 构建弹幕的 URL
            danmaku_url = f"https://comment.bilibili.com/{cid}.xml"

            # 获取弹幕数据
            danmaku_request = requests.get(url=danmaku_url, headers=headers)
            danmaku_request.encoding = 'utf-8'

                # 提取弹幕内容            
            danmaku_soup = BeautifulSoup(danmaku_request.text, 'lxml')
            results = danmaku_soup.find_all('d')

                # 数据处理
            data = [d.text.strip() for d in results]  # 使用 strip() 去除多余的空格和换行
            
                    # 保存到 CSV 文件
            df = pd.DataFrame(data)
            df.to_csv(base_dir+"/"+links[i][-12:]+".csv", index=False, header=None, encoding="utf_8_sig")
        else: print(url+" Failed")


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
    element=soup.find("span", class_="video-share-info video-toolbar-item-text")
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
    #获取日期
    element=soup.find("div", class_="pubdate-ip-text")
    if element:
        date.append(element.get_text(strip=True))
    else:
        date.append("Not Found")

    print(str(i)+" success")
   

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
df['上传日期']=date
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



