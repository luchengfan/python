import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fa8f77c0-c1a5-4e80-89ae-8a8c10f09128"
headers = {"Content-Type": "text/plain"}
s = "What do you want to say? "
data = {
      "msgtype": "text",
      "text": {
         "content": s,
      }
   }
r = requests.post(url, headers=headers, json=data)
print(r.text)