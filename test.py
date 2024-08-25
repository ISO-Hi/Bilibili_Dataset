
import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import pandas as pd
import re
from bilibili_api import video, sync
from datetime import datetime



 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
    
url = 'https://www.bilibili.com/video/BV1DsWLeLEzQ'

video_request = requests.get(url=url, headers=headers)
soup = BeautifulSoup(video_request.text, "html.parser")


script_tag = soup.find("script", text=lambda t: t and "window.__playinfo__" in t)
script_content = script_tag.string
    
    # Use a regular expression to extract the full baseUrl
base_url_match = script_content[script_content.find("baseUrl")+10:script_content.find("baseUrl")+300]
print(base_url_match)
#


with open("test1.html", "w", encoding="utf-8") as file:
    file.write(script_tag.prettify())
cid=base_url_match.split('/')[6]
cid=1657925409

     # 构建弹幕的 URL
danmaku_url = f"https://comment.bilibili.com/1657925409.xml"

            # 获取弹幕数据
danmaku_request = requests.get(url=danmaku_url, headers=headers)
danmaku_request.encoding = 'utf-8'

            # 提取弹幕内容
danmaku_soup = BeautifulSoup(danmaku_request.text, 'lxml')
results = danmaku_soup.find_all('d')

            # 数据处理
            # 
            #  
data = [d.text.strip() for d in results]  # 使用 strip() 去除多余的空格和换行

            # 保存到 CSV 文件
df = pd.DataFrame(data)
df.to_csv("12.csv", index=False, header=None, encoding="utf_8_sig")