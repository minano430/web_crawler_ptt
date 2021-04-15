# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:36:27 2019

@author: 曾嘉鴻
"""
import requests
import sys
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
        self.temp = ""
        self.count = 0
        self.temp1 = 0
        self.download_complete = 0
        self.progress_bar = QtWidgets.QProgressBar()

    def __del__(self):
        self.wait()

    def set(self, temp, temp1, count):
        self.temp = temp
        self.temp1 = temp1
        self.count = count


    def run(self):
        self.progress_bar.setValue(0)
        url = 'https://www.ptt.cc'
        current_page = self.get_web_page(url + '/bbs/Beauty/index.html')
        if current_page:
            articles = []  # 全部的今日文章
            current_articles, prev_url = self.get_articles(current_page, self.temp, 0)  # 目前頁面的今日文章
            while current_articles:  
                # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
                articles += current_articles
                current_page = self.get_web_page(url + prev_url)
                current_articles, prev_url = self.get_articles(current_page, self.temp, 1)
            # 已取得文章列表，開始進入各文章讀圖
            for article in articles:
                if article['push_count'] >=  self.temp1:
                    page = self.get_web_page(url + article['href'])
                    if page:
                        img_urls = self.parse(page)
                        self.save(img_urls, article['title'])
                        article['num_images'] = len(img_urls)
                        print("Thread ", self.count, ' Processing', article)
                    self.download_complete += 1
                    self.progress_bar.setValue((self.download_complete/len(articles))*100)
                else:
                    self.download_complete += 1
                    self.progress_bar.setValue((self.download_complete/len(articles))*100)

            print("Thread ",self.count , " Process complete!")

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
        for d in divs:
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



class Input(QtWidgets.QWidget):

    def __init__(self, parent = None):

        super().__init__(parent)
        self.Thread_List = []      #初始化時指派一個線程
        self.progress_bar = []
        self.temp = ""
        self.temp1 = 0
        self.count = 0
        self.arrange = False   #檢查此次的輸入是否有排入線程中

        self.layout = QtWidgets.QFormLayout()
        self.Label1 = QtWidgets.QLabel("Date")
        self.date = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label1, self.date)

        self.Label2 = QtWidgets.QLabel("Push_Count")
        self.good = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label2, self.good)

        self.btn2 = QtWidgets.QPushButton('Ok')
        self.btn2.clicked.connect(self.grab)
        self.layout.addRow(self.btn2)

        self.setLayout(self.layout)
        self.setWindowTitle("Practice")
        self.setGeometry(150, 150, 250, 500)

    def grab(self):             #多線程處理
        print("Get process!")
        self.temp = self.date.text()
        self.temp1 = int(self.good.text())
        self.arrange = False
        self.count += 1
        self.check()


    def check(self):
        if self.temp1 < 0:
            print("Invalid input")
            return None



        for Threads in self.Thread_List:
            if not Threads.isRunning():
                self.arrange = True
                Threads.set(self.temp, self.temp1, self.count)
                Threads.start()
                break

        if not self.arrange:
            if len(self.Thread_List) <= 10:
                self.Thread_List.append(Thread())                    #新增一個Thread到最後面
                self.Thread_List[-1].set(self.temp, self.temp1, self.count)
                self.layout.addRow(self.Thread_List[-1].progress_bar)
                self.Thread_List[-1].start()                         #將最後一個Thread指派程序
            else:
                print("Out of Process")




def main():
    app = QtWidgets.QApplication(sys.argv)
    example = Input()
    example.show()
    app.exec_()


if __name__ == '__main__':
    main()