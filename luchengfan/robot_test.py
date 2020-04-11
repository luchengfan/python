import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=427d3131-7b47-44ae-adfa-1d06f8e8df0b"

headers = {"Content-Type": "news/plain"}
s = "胖熊"
data = {
      "msgtype": "news",
      "news": {
         "articles" :[
            {
               "title" : "糟了,是心动的感觉",
               "description" : "糟了,是心动的感觉",
               "url" : "URL",
               "picurl" : "http://wx4.sinaimg.cn/mw690/006HJgYYgy1fsdgpmy0ldg30dc0dc0vy.gif"
            }
         ]
      }
   }
r = requests.post(url, headers=headers, json=data)
print(r.text)

#python E:\python\wechat\robot_test.py