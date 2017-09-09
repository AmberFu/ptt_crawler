# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

aa = input('Your keywords: ')
keylist = aa.split()

query = 'q='

for i in keylist:
    query += '%s+' % i

q = query[:-1]
print('query = %s' % q)

url = 'https://www.google.com.tw/search?%s' % q
print('url : %s' % url)
print('\n'
      '---------------')

#設置假的瀏覽器資訊
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

#發送請求
req = urllib.request.Request(url = url,headers=headers)
page = urllib.request.urlopen(req)
contentBytes = page.read()

#進行分割
soup = BeautifulSoup(contentBytes, 'html.parser')
listall = soup.find_all('h3', 'r')
for title in listall:
    print('title: ', title.string)
    print('url: ', title.a['href'])
    print('----------------------')

