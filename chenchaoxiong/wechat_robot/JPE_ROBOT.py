import requests
import sys

headers = {"Content-Type": "text/plain"}
robot = sys.argv[1]
if robot == "下推订单":
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=54a2ea2c-942f-4adb-98ee-966d92694879"
    cmd = "大家下推订单啦，超过12点就超时了！"
else:
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5f4ba177-7032-41dd-ab47-26d600cb61ea"
    cmd = "执行报错啦,帅雄还不赶紧看下~"
data = {
      "msgtype": "text",
      "text": {
         "content": cmd,
         "mentioned_list":["@all"],
      }
   }
r = requests.post(url, headers=headers, json=data)
print(r.text)