import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

# 配置信息（需要根据实际情况修改）
CONFIG = {
    # "checkmk_url": "https://checkmk.integration-eu.signintra.com/integration/check_mk/index.py?start_url=%2Fintegration%2Fcheck_mk%2Fdashboard.py",
    "checkmk_url": "https://checkmk.integration-eu-np.signintra.com/integration_np/check_mk/index.py?start_url=%2Fintegration_np%2Fcheck_mk%2Fdashboard.py",
    "auth": ("support", "support123**"),  # CheckMK登录凭证
    "check_interval": 300,  # 检查间隔（秒）
    "smtp": {
        "server": "smtp.example.com",
        "port": 587,
        "user": "your_email@example.com",
        "password": "email_password",
        "recipient": "alert@example.com"
    }
}


def check_status():
    """访问CheckMK页面并检查报警状态"""
    try:
        # 创建会话保持登录状态
        session = requests.Session()

        # 访问登录页面获取可能的会话cookie
        session.get(CONFIG['checkmk_url'], auth=CONFIG['auth'])

        # 获取监控仪表盘页面
        response = session.get(CONFIG['checkmk_url'], auth=CONFIG['auth'])
        response.raise_for_status()

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找Critical报警（需要根据实际页面结构调整选择器）
        # 示例：假设Critical状态用红色显示且包含"critical"类
        critical_alerts = soup.select('.state_critical')

        return len(critical_alerts) > 0

    except Exception as e:
        print(f"检查失败: {str(e)}")
        return False


def send_alert():
    """发送邮件通知"""
    msg = MIMEText("CheckMK 检测到 Critical 级别报警！请立即查看！")
    msg['Subject'] = '[紧急] CheckMK 报警通知'
    msg['From'] = CONFIG['smtp']['user']
    msg['To'] = CONFIG['smtp']['recipient']

    with smtplib.SMTP(CONFIG['smtp']['server'], CONFIG['smtp']['port']) as server:
        server.starttls()
        server.login(CONFIG['smtp']['user'], CONFIG['smtp']['password'])
        server.send_message(msg)


def main():
    while True:
        if check_status():
            print("检测到报警，发送通知...")
            send_alert()
        else:
            print("状态正常")

        time.sleep(CONFIG['check_interval'])


if __name__ == "__main__":
    main()