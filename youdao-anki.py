# -*- coding: utf-8 -*-
"""
有道爬虫+自动生成Anki导入文本
"""

import re
import requests
from bs4 import BeautifulSoup
import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,QVBoxLayout, QWidget)
from form import Ui_Form
import os
from traceback import format_exc
CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE_PATH)



url = r'https://www.youdao.com/result?'#有道辞典url
separator = r'@'#导入ANKI时，选用的分隔符
max_meanings = 5#最大义项数
max_examples = 3#最大例句数

hiraPattern = re.compile(u'[\u3040-\u309F\-]')
kataPattern = re.compile(u'[\u30A0-\u30FF\-]')
kanjiPattern = re.compile(u'[\u4e00-\u9faf]')
enPattern = re.compile(r'[a-z\-]',re.I)
class langError(Exception):
    pass
class requestsError(Exception):
    pass
class transError(Exception):
    pass

def getWord(word):
    paramsDict={'word':re.sub(' ',r'%20',word),'lang':''}
    
    #添加语言类型标识
    lang = []
    length = len(re.sub(' ','',word))
    #print(length,len(re.findall(kataPattern,word)))
    if re.search(kanjiPattern,word):
        lang.append('kanji')
    if len(re.findall(hiraPattern,word)) == length:
        lang.append('hira')
    if len(re.findall(kataPattern,word)) == length:
        lang.append('kata')
    if len(re.findall(enPattern,word)) == length:
        lang.append('en')
    #根据标识判断语种
    if 'kanji' in lang or 'hira' in lang or 'kata' in lang:
        lang.append('ja')
        paramsDict['lang'] = 'ja'
    elif 'en' in lang:
        paramsDict['lang'] = 'en'
    else:
        raise langError(f'无法识别【{word}】的语种')
    try:
        res = requests.get(url,timeout = 10,params = paramsDict,headers = {'user-agent':'Mozilla/5.0'})
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res,lang
    except:
        raise requestsError(f'查询【{word}】时连接错误，错误码为{res.status_code}')
        
def transWord(word):
    meanings = []
    examples = []
    
    res,lang = getWord(word)
    soup = BeautifulSoup(res.content,'html.parser')
    if 'en' in lang:
        #义项
        try:
            for meaning in soup.find_all('span',class_ = 'trans'):
                meanings.append(meaning.text)
        except:
            raise transError(f'未搜到【{word}】的释义')
        #例句
        try:
            for example in soup.find('div',id = 'catalogue_sentence').find_all('div',class_ = 'col2'):
                #print(example)
                enEp = example.find('div',class_='sen-eng').text
                chEp = example.find('div',class_='sen-ch').text
                examples.append([enEp,chEp])
        except:
            pass
    
    if 'ja' in lang:
        try:
        #假名及读音
            kanaSpan = soup.find('div',class_ = 'head-content').find('span')
            if 'kanji' in lang:
                kana = kanaSpan.text
                meanings.append(kana)
            elif kanaSpan.find('sup'):
                kana = kanaSpan.find('sup').text
                meanings.append(kana)

        except:
            lang.append('nokana')
        
        #义项
        try:
            for meaning in soup.find_all('div',class_ = 'sense-ja'):
                meanings.append(meaning.text)
        except:
            raise transError(f'未搜到【{word}】的释义')
        
        #例句
        try:
            for example in soup.find('div',id = 'catalogue_sentence').find_all('li',class_ = 'mcols-layout'):
                enEp = example.find('div',class_='sen-eng').text
                chEp = example.find('div',class_='sen-ch').text
                if re.search(hiraPattern,enEp):
                    examples.append([enEp,chEp])
                else:
                    examples.append([chEp,enEp])
        except:
            pass
        
    return meanings,examples,lang

def makeCard(word):
    card = word+separator
    meanings,examples,lang = transWord(word)

    #测试义项数目。当义项过多时，删节同类义项
    mn_num = 1
    for mn in meanings:
        mn_num += len(re.findall(r'[；，。]',mn))
    if mn_num > 5:
        for index,mn in enumerate(meanings):
            if 'en' in lang:
                meanings[index] = re.sub(r'，.*?；','；',mn)
            else:
                meanings[index] = re.sub(r'，.*?。','。',mn)
    
    #再次测试义项数目。仍然过多时，保留前几个义项
    mn_num = 1
    for mn in meanings:
        mn_num += len(re.findall(r'[；。]',mn))
    if mn_num > max_meanings:
        if 'ja' in lang:
            meanings = meanings[:max_meanings]
        else:
            for index,mn in enumerate(meanings):
                meanings[index] = '；'.join(re.split(r'；',mn)[:(max_meanings+1)//2])
    #将义项编译为卡片
    if 'nokana' in lang:
        for mn in meanings[:-1]:
            card += re.sub(r'。',r'；',mn)
        card += re.sub(r'。','',meanings[-1])
    elif 'ja' in lang:
        card += meanings[0] + r'<br>'
        for mn in meanings[1:-1]:
            card += re.sub(r'。',r'；',mn)
        card += re.sub(r'。','',meanings[-1]) + r'<br>'
    else:
        for mn in meanings:
            card += mn + '<br>'
    
    #将例句编译为卡片
    exp_num = min(mn_num//2,len(examples),max_examples)
    card_des = f'【{word}】有{mn_num}个义项,共编入{exp_num}个例句'
    if not len(examples) == 0:
        card += r"<span style='font-size:12px;color:blue'>"
        for exp in examples[:exp_num]:
            card += exp[0] + r'<br>'
            card += exp[1] + r'<br>'
        card += r'</span>'
    return card,card_des



class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Youdao-Anki 卡片自动编译工具")

        self.ui.start_Button.clicked.connect(self.startProgram)
    
    def startProgram(self):
        global max_meanings
        max_meanings = self.ui.mn_box.value()
        global max_examples
        max_examples = self.ui.exp_box.value()
        inputText = self.ui.input_box.toPlainText()
        if len(inputText) > 0:
            words = re.split('\n',inputText)
            self.ui.output_box.append(f"读取词汇：\n{str(words)}\n共读取词汇{len(words)}个")
            self.ui.output_box.append("----------------------------------------------")
            cards = ''
            error_cards = []
            for w in words:
                try:
                    card,card_des = makeCard(w)
                    self.ui.output_box.append(card_des)
                    cards += card+'\n'
                except:
                    error_cards.append(w)
                    self.ui.output_box.append(format_exc().split("\n")[-2])
            self.ui.output_box.append("----------------------------------------------")
            if len(error_cards) >0:
                self.ui.output_box.append(f"以下词汇发生了错误，请检查拼写或手动添加。\n{str(error_cards)}")
            self.ui.output_box.append("运行完毕，已将文件保存至" + CURRENT_DIR)
            with open("运行结果.txt",'w',encoding='utf-8') as output_Txt:
                output_Txt.write(cards)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
