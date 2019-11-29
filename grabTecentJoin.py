# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-23 09:36:08'

import requests
from bs4 import BeautifulSoup
import html2text

parser = html2text.HTML2Text()

fid = 97
url = "https://join.qq.com/post.php?fid=%s" % fid

proxies = {"http": "127.0.0.1:12639"}
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
req=requests.get(url,headers=header,proxies=proxies,timeout=5)

html=req.text

# print(html)

soup=BeautifulSoup(html,'lxml')
content = soup.findAll("div", {"class":"item mt30"})

print (soup.find("span", {"class":"selected"}).text)

for data in content:
    title = data.find("div", {"class":"title"}).text
    description = parser.handle(str(data.find("div", {"class":"contxt mt10"}))).strip()
    if title == "岗位描述":
        # print(dir(data.find("div", {"class":"contxt mt10"})))
        print ("\n" + title + "\n" + description)
    elif title == "岗位要求":
        print ("\n" + title + "\n" + description)
