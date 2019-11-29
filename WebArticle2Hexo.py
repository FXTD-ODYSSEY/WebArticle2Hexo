# coding:utf 8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-17 21:16:27'

# NOTE Python2 coding
# import urllib2
# if __name__ == "__main__":
#     url = r"https://www.aducg.com/2018/07/16/1957/"
    
#     proxy_support = urllib2.ProxyHandler({"https":"127.0.0.1:12639"})  
#     opener = urllib2.build_opener(proxy_support)  
#     urllib2.install_opener(opener)  
    
#     req = urllib2.Request(url)  
#     req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3819.400")  

#     html = urllib2.urlopen(req)
#     print (html.read())

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import requests
import html2text
from bs4 import BeautifulSoup
from textwrap import dedent
import time
import re


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(487, 131)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.URL_LE = QtWidgets.QLineEdit(Form)
        self.URL_LE.setObjectName("URL_LE")
        self.horizontalLayout.addWidget(self.URL_LE)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Proxy_LE = QtWidgets.QLineEdit(Form)
        self.Proxy_LE.setObjectName("Proxy_LE")
        self.horizontalLayout_2.addWidget(self.Proxy_LE)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.Tag_LE = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tag_LE.sizePolicy().hasHeightForWidth())
        self.Tag_LE.setSizePolicy(sizePolicy)
        self.Tag_LE.setMinimumSize(QtCore.QSize(0, 0))
        self.Tag_LE.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Tag_LE.setObjectName("Tag_LE")
        self.horizontalLayout_3.addWidget(self.Tag_LE)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.Attr_LE = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Attr_LE.sizePolicy().hasHeightForWidth())
        self.Attr_LE.setSizePolicy(sizePolicy)
        self.Attr_LE.setObjectName("Attr_LE")
        self.horizontalLayout_3.addWidget(self.Attr_LE)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.Param_LE = QtWidgets.QLineEdit(Form)
        self.Param_LE.setObjectName("Param_LE")
        self.horizontalLayout_3.addWidget(self.Param_LE)
        self.Republish_CB = QtWidgets.QCheckBox(Form)
        self.Republish_CB.setChecked(True)
        self.Republish_CB.setObjectName("Republish_CB")
        self.horizontalLayout_3.addWidget(self.Republish_CB)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.Output_BTN = QtWidgets.QPushButton(Form)
        self.Output_BTN.setObjectName("Output_BTN")
        self.verticalLayout.addWidget(self.Output_BTN)
        self.Output_HTML_BTN = QtWidgets.QPushButton(Form)
        self.Output_HTML_BTN.setObjectName("Output_HTML_BTN")
        self.verticalLayout.addWidget(self.Output_HTML_BTN)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("网页文章 MarkDown 抓取器")
        self.label.setText("抓取网址")
        self.label_2.setText("代理设置")
        self.Proxy_LE.setText("127.0.0.1:12639")
        self.label_3.setText("抓取标签")
        self.Tag_LE.setText("div")
        self.label_4.setText("标签属性")
        self.Attr_LE.setText("class")
        self.label_5.setText("属性参数")
        self.Republish_CB.setText("输出转载信息")
        self.Output_BTN.setText("输出 markdown 文件")
        self.Output_HTML_BTN.setText("输出 HTML 文件")



class WebArticle2Hexo(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Output_BTN.clicked.connect(self.getMarkdown)
        self.Output_HTML_BTN.clicked.connect(self.getHTML)

    def readHtml(self,url):

        if url.startswith("http"):
            http = "http"
        elif url.startswith("https"):
            http = "https"
        else:
            QtWidgets.QMessageBox.warning(self,"警告","请输入正确的http协议网址↓↓↓\n%s"%url)
            return

        proxies = {http: self.Proxy_LE.text()}

        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        req=requests.get(url,headers=header,proxies=proxies,timeout=5)

        return req.text

    def getHTML(self):
        
        output_path,_ = QtWidgets.QFileDialog().getSaveFileName(self,caption="保存 HTML 文件",filter="HTML 文件 (*.html)")

        # NOTE 判断路径是否存在
        if not output_path:
            return

        url= self.URL_LE.text()
        html = self.readHtml(url)

        with open(output_path,'w',encoding="utf-8") as f:
            f.write(html)

        QtWidgets.QMessageBox.information(self,"输出成功","输出成功")

    def getMarkdown(self):

        output_path,_ = QtWidgets.QFileDialog().getSaveFileName(self,caption="保存 Markdown 文件",filter="Markdown 文件 (*.md)")

        # NOTE 判断路径是否存在
        if not output_path:
            return

        url= self.URL_LE.text()
        html = self.readHtml(url)
        
        parser = html2text.HTML2Text()

        soup=BeautifulSoup(html,'lxml')

        tag = self.Tag_LE.text()
        attr = self.Attr_LE.text()
        param = self.Param_LE.text()

        # NOTE Beatiful Soup extract data
        # cotent = soup.find('div', {"class":"kratos-post-content"})
        content = soup.find(tag, {attr:param})

        md = parser.handle(str(content)).strip()

        if self.Republish_CB.isChecked():
            title = soup.find("title").text
            domain =  re.search(r"://(.*?)/",url).group(1)
            info = f"""
            ---
            title: 【转载】 {title}
            tags:
            - 转载
            categories:
            - 转载
            date: {time.strftime("%Y-%m-%d %X", time.localtime())}
            ---

            # 转载自 {domain}

            <!-- more -->

            ---
            
            <a href="{url}" style="display: flex;
            text-align: center;
            flex-direction: column;">原文链接
            </a>
            
            ---

            """
            # NOTE 去掉第一行换行
            info = dedent(info)[1:]
            md = info + md

        with open(output_path,'w',encoding="utf-8") as f:
            f.write(md)

        QtWidgets.QMessageBox.information(self,"输出成功","输出成功")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    win = WebArticle2Hexo()
    win.show()

    app.exec_()