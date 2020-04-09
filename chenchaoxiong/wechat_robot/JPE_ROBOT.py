#coding=utf-8
from jira import JIRA 
import requests
import sys
jira = JIRA('https://jira.cvte.com/', auth=('chenchaoxiong', 'Cvte0409ccx'))

issues = jira.search_issues('project in (TVS, OCS_JIRA) AND status in (新建, 处理中, 重新打开) AND assignee in (luchengfan, chenchaoxiong) ORDER BY cf[11110] ASC',maxResults=-1)
issues2 = ""
for iss in issues :
    issues2 = issues2 + iss.key + iss.fields.summary + "\n"

issues3 = "以下JIRA需要梳理：" + "\n" + issues2
headers = {"Content-Type": "text/plain"}
robot = sys.argv[1]
if robot == "下推订单":
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=54a2ea2c-942f-4adb-98ee-966d92694879"
    cmd = "大家下推订单啦，超过12点就超时了！"
elif robot == "收集情报":
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=842afd3c-6b7d-41fc-a2bf-5ee54fc33309"
    cmd = "更新情报啦，12点前完成：https://doc.weixin.qq.com/txdoc/excel?scode=AKEAkwcCAA42Vq6300AC4A3wZXAPg&docid=e2_AC4A3wZXAPgzwTQulDRTUWdJXPV3J&type=1"
elif robot == "梳理JIRA":
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5f4ba177-7032-41dd-ab47-26d600cb61ea"
    cmd = issues3
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