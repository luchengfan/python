from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart

from_addr = '287485391@qq.com'
qqCode = '***'
# 输入收件人地址:
to_addrs =  ['luchengfan92@163.com','lufan199204@qq.com']
# 输入SMTP服务器地址:
smtp_server = "smtp.qq.com"

#配置服务器
server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, qqCode)

#创建一个带附件的实例
message = MIMEMultipart()
#邮件正文内容
message.attach(MIMEText('这是卢成帆自学Python 邮件发送测试……', 'plain', 'utf-8'))
message['From'] = Header("咫尺天涯", 'utf-8')   #发件人
message['To'] = ','.join(to_addrs)       #这里必须要把多个邮箱按照逗号拼接为字符串
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')  #邮件标题

# 构造附件1，传送当前目录下的 readme.txt 文件
att1 = MIMEText(open('readme.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="readme.txt"'
message.attach(att1)

try:
    server.sendmail(from_addr, to_addrs, message.as_string())
    print('邮件发送成功')
except Exception as e:
    print('邮件发送失败--' + str(e))

server.quit()