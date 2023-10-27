#自动回复小工具 V1.0
#理论上可以回复任何即时通讯软件，不止微信

import pyautogui
import pyperclip
import time
import sys
import os
import requests
from wxauto import *
# import wxauto
# import json

url = "https://openai.api2d.net/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  'Authorization': '你自己的秘钥' 
}

data = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": ""}],
#   "stream": True,
}
# base=os.path.dirname(os.path.realpath(sys.argv[0]))
base=os.path.dirname(sys.argv[0])

print(base)
taskList=[
    {"type":"单击图片","content":base+"\\red1.png"},
    {"type":"输入文字","content":""},
    {"type":"单击图片","content":base+"\send.png"},
    {"type":"回家","content":base+"\home.png"}
]
#尝试点击图片，如果点击成功返回True，否则返回False
def mouseClick(img):
    location=pyautogui.locateCenterOnScreen(img)
    if location is not None:
        print("找到图片")
        pyautogui.click(location.x,location.y,clicks=1,button="left")
        return True
    else:
        return False
    
#执行任务
def doTask(task):
    #判断任务类型
    if task["type"]=="单击图片":
        # print("开始做单击图片任务")
        img=task["content"]
        return mouseClick(img)
    elif task["type"]=="输入文字":
        
        text=task["content"]
        pyperclip.copy(text)
    #    print(text)
##        pyperclip.paste()
        pyautogui.hotkey("ctrl","v")
        return True    
    elif task["type"]=="回家":
        img=task["content"]
        return mouseClick(img)
    

# 获取ai回复
def getReplay(msg):
    data["messages"][0]["content"]=msg
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# 获取对方消息

#开始监测   
while True:
    if doTask(taskList[0]):
        print("单击图片成功")
        time.sleep(0.5) 
        
        # 获取当前微信客户端
        wx = WeChat()

        # 获取会话列表
        wx.GetSessionList()

        #获取对方消息
        msgJson=wx.GetLastMessage
        msg=msgJson[1]
        print(msg)
        # 回复
        taskList[1]["content"]=getReplay(msg)
        
        if doTask(taskList[1]):
            print("复制文本成功")
            time.sleep(0.1)
            doTask(taskList[2])
            # time.sleep(0.1)
            doTask(taskList[3])
    else:
        print("监测中...")
