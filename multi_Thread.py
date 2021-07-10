# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:36:27 2019

@author: 曾嘉鴻
"""
import requests
from PyQt5 import QtWidgets, QtCore
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json


class Thread(QtCore.QThread):

    update = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.date_string = ""
        self.Thread_count = 0
        self.like_count = 0
        self.download_complete = 0
        self.progress_bar = QtWidgets.QProgressBar()

    def __del__(self):
        self.wait()

    def set(self, date_string, like_count, Thread_count):
        
        self.date_string = date_string
        self.like_count = like_count
        self.Thread_count = Thread_count


    def run(self):
        
        self.progress_bar.setValue(0)
        url = 'https://www.ptt.cc'
        current_page = self.get_web_page(url + '/bbs/Beauty/index.html')
        
        if current_page:
            articles = []  # 全部的今日文章
            current_articles, prev_url = self.get_articles(current_page, self.date_string, 0)  # 目前頁面的今日文章
            while current_articles:  
                # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
                articles += current_articles
                current_page = self.get_web_page(url + prev_url)
                current_articles, prev_url = self.get_articles(current_page, self.date_string, 1)

            # 已取得文章列表，開始進入各文章讀圖
            for article in articles:
                if article['push_count'] >=  self.like_count :
                    page = self.get_web_page(url + article['href'])
                    
                    if page:
                        img_urls = self.parse(page)
                        self.save(img_urls, article['title'])
                        article['num_images'] = len(img_urls)
                        print("Downloading ", article)
                        
                    self.download_complete += 1
                    self.progress_bar.setValue((self.download_complete/len(articles))*100)
                else:
                    self.download_complete += 1
                    self.progress_bar.setValue((self.download_complete/len(articles))*100)

            print(article ," Download complete!")

            # 儲存文章資訊
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)
                  
    def get_articles(self,_dom, _date, _interger):
        
        soup = BeautifulSoup(_dom, 'html.parser')
        url = 'https://www.ptt.cc'
        # 取得上一頁的連結
        paging_div = soup.find('div', 'btn-group btn-group-paging')
        prev_url = paging_div.find_all('a')[1]['href']
    
        articles = []  # 儲存取得的文章資料
        divs = soup.find_all('div', 'r-ent')
        print("date_input",_date)
        
        for d in divs:
            print(d.find('div', 'date').string.strip())
            if d.find('div', 'date').string.strip() == _date:  # 發文日期正確
                if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                    if d.find('a').string.find("公告") == -1:     #不抓取公告
                        # 取得推文數
                        push_count = 0
                        if d.find('div', 'nrec').string == "爆":
                            push_count = 100
                        elif d.find('div', 'nrec').string:
                            try:
                                push_count = int(d.find('div', 'nrec').string)  # 轉換字串為數字
                            except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                                pass
                        
                        # 取得文章連結及標題
                        href = d.find('a')['href']
                        title = d.find('a').string
                        articles.append({
                            'title': title,
                            'href': href,
                            'push_count': push_count,
                            'num_images' : 0
                        })
        if articles:
            return articles, prev_url
        elif _interger == 0:
            current_page = self.get_web_page(url + prev_url)
            current_articles, prev_url = self.get_articles(current_page, _date, 0)
            return current_articles, prev_url
        else:
            return articles, prev_url
    
    def get_web_page(self,url):
        
        resp = requests.get(
            url=url,
            cookies={'over18': '1'}
        )
        if resp.status_code != 200:
            print('Invalid url:', resp.url)
            return None
        else:
            return resp.text
        
    def parse(self,_dom):
        soup = BeautifulSoup(_dom, 'html.parser')
        links = soup.find(id='main-content').find_all('a')
        img_urls = []
        for link in links:
            if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
                img_urls.append(link['href'])
        return img_urls
    
    
    def save(self,img_urls, title):
        if img_urls:
            try:
                path = 'C:/Users/user/Desktop/練習圖片/'
                directory_name = title.strip()  # 用 strip() 去除字串前後的空白
                os.makedirs(path + directory_name)
                for img_url in img_urls:
                    if img_url.split('//')[1].startswith('m.'):
                        img_url = img_url.replace('//m.', '//i.')
                    if not img_url.split('//')[1].startswith('i.'):
                        img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                    if not img_url.endswith('.jpg'):
                        img_url += '.jpg'
                    fname = img_url.split('/')[-1]
                    urllib.request.urlretrieve(img_url, path + os.path.join(directory_name, fname))
            except Exception as e:
                print(e)
