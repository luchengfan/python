from email.mime.text import MIMEText
import smtplib
from email.header import Header

from_addr = '287485391@qq.com'
qqCode = '***'
# 输入收件人地址:
to_addrs =  'luchengfan92@163.com'   #'lufan199204@qq.com'
# 输入SMTP服务器地址:
smtp_server = "smtp.qq.com"

#配置服务器
server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, qqCode)

#组装发送内容
message = MIMEText('这是我发送的第一封邮件', 'plain', 'utf-8')   #发送的内容
message['From'] = Header("咫尺天涯", 'utf-8')   #发件人
message['To'] = Header("卧听风雨", 'utf-8')     #收件人
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')  #邮件标题

try:
    server.sendmail(from_addr, [to_addrs], message.as_string())
except Exception as e:
    print('邮件发送失败--' + str(e))

print('邮件发送成功')
server.quit()