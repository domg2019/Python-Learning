import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG = {
    "base_url": "https://checkmk.integration-eu-np.signintra.com",
    "login_url": "https://checkmk.integration-eu-np.signintra.com/integration_np/check_mk/login.py",  # 登录表单URL
    "dashboard_url": "https://checkmk.integration-eu-np.signintra.com/integration_np/check_mk/dashboard.py",  # 仪表盘URL
    "auth": {"_username": "support", "_password": "support123**"},  # 表单登录参数
    "check_interval": 300,
    "smtp": {  # 配置你的SMTP信息
        "server": "smtp.example.com",
        "port": 587,
        "user": "your_email@example.com",
        "password": "email_password",
        "recipient": "alert@example.com"
    }
}


def check_status():
    """访问CheckMK并检查CRIT报警"""
    try:
        session = requests.Session()

        # Step 1: 提交登录表单
        login_response = session.post(
            CONFIG["login_url"],
            data=CONFIG["auth"],
            headers={"Referer": CONFIG["login_url"]},
        )
        login_response.raise_for_status()

        # Step 2: 访问仪表盘页面
        dashboard_response = session.get(CONFIG["dashboard_url"])
        dashboard_response.raise_for_status()

        # 调试：保存HTML用于分析
        with open("debug_dashboard.html", "w", encoding="utf-8") as f:
            f.write(dashboard_response.text)

        # Step 3: 解析HTML
        soup = BeautifulSoup(dashboard_response.text, 'html.parser')

        # 方案1：通过文本内容匹配（更可靠）
        crit_elements = soup.find_all(text=lambda t: "CRIT" in str(t).strip())

        # 方案2：通过类名或ID匹配（需根据实际HTML调整）
        # crit_elements = soup.select('.state_crit, .critical-alert')  # 示例类名

        logging.info(f"找到 {len(crit_elements)} 个CRIT元素")
        return len(crit_elements) > 0

    except Exception as e:
        logging.error(f"检查失败: {str(e)}")
        return False


def send_alert():
    """发送邮件通知（示例需配置SMTP）"""
    msg = MIMEText("检测到CheckMK CRIT报警！详情请查看仪表盘。")
    msg['Subject'] = '[紧急] CheckMK报警通知'
    msg['From'] = CONFIG['smtp']['user']
    msg['To'] = CONFIG['smtp']['recipient']

    try:
        with smtplib.SMTP(CONFIG['smtp']['server'], CONFIG['smtp']['port']) as server:
            server.starttls()
            server.login(CONFIG['smtp']['user'], CONFIG['smtp']['password'])
            server.send_message(msg)
            logging.info("报警邮件已发送")
    except Exception as e:
        logging.error(f"邮件发送失败: {str(e)}")


def main():
    logging.info("启动监控脚本...")
    while True:
        if check_status():
            logging.warning("检测到CRIT报警！")
            send_alert()
        else:
            logging.info("状态正常")
        time.sleep(CONFIG['check_interval'])


if __name__ == "__main__":
    main()