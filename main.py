import smtplib
import time
import requests
from email.header import Header
from email.mime.text import MIMEText

def send_email(subject, content):
    server = None
    sender = ''
    receiver = ''

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('实习生定时签到任务', 'utf-8')
    message['To'] = Header('Allen', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    smtp_server = ''
    smtp_port = 465
    smtp_username = ''
    smtp_authorization_code = ''

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)  # 使用SSL加密并设置超时
        server.login(smtp_username, smtp_authorization_code)
        server.sendmail(sender, [receiver], message.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败', e)
    finally:
        if server is not None:
            server.quit()


# 需要请求的url链接
login_url = "https://dgsxwx.getc.net.cn/intern/account!toLogin.action"
single_login_url = "https://dgsxwx.getc.net.cn/intern/account!toSingleLogin.action"
attend_url = "https://dgsxwx.getc.net.cn/intern/attende!save.action"
# 统一header
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; V2232A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260117 MMWEBSDK/20240501 MMWEBID/2977 MicroMessenger/8.0.50.2701(0x2800325A) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}
# 用户list
users = {
    'login_params': {
        'openid': '',
        'studentno': '',
        'time': ''
    },
    'body_params': {
        'address': '',
        'locationX': '',
        'locationY': ''
    }
}


if __name__ == '__main__':
    # 遍历用户信息
    for user in users:
        # 从用户list中取到需要用的参数
        login_params = users[user]['login_params']
        body_params = users[user]['body_params']
        login_params['time'] = str(int(time.time()))

        # 第一步: 发送GET请求以获取登录时所需的token(cookie)
        response = requests.get(login_url, params=login_params, headers=headers, allow_redirects=False)
        cookies = response.cookies

        # 第二步: 使用获取到的token(cookie)值发送登录请求，登录成功后才能进行签到
        response = requests.get(single_login_url, headers=headers, cookies=cookies)
        # 检查响应状态码
        if response.status_code != 200:
            print(f'{user} 登录失败，状态码：{response.status_code}, 请尝试手动签到')
            continue

        # 第三步: 使用POST请求进行签到
        response = requests.post(attend_url, headers=headers, data=body_params, cookies=cookies)
        # 检查是否签到成功
        if response.status_code == 200:
            print(f'{user} 签到成功')
        else:
            print(f'{user} 签到失败，状态码：{response.status_code}, 请尝试手动签到')

