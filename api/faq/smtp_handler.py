import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr

from faq.models import ERequest, EAnswer


def get_config():
    _conf = dict()
    from faq.setting import SMTPConfig
    _conf['host'] = SMTPConfig.SMTP_HOST
    _conf['smtp_user'] = SMTPConfig.SMTP_USER
    _conf['smtp_license'] = SMTPConfig.SMTP_LICENSE
    return _conf


def send(target, content):
    conf = get_config()
    # 第三方 SMTP 服务
    mail_host = conf['host']  # 设置服务器
    mail_user = conf['smtp_user']  # 用户名
    mail_pass = conf['smtp_license']  # 口令

    sender = conf['smtp_user']

    message = MIMEText(content, 'plain', 'utf-8')
    name, addr = parseaddr("openEuler FAQ Server <{}>".format(sender))
    message['From'] = formataddr((Header(name, 'utf-8').encode(), addr))
    message['To'] = Header(",".join(sender), 'utf-8')
    message['Subject'] = Header("openEuler FAQ 审核通知", 'utf-8')

    try:
        smtp_obj = smtplib.SMTP()
    except smtplib.SMTPException:
        print("Error: SMTP initialization failed")
        return

    try:
        smtp_obj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtp_obj.login(mail_user, mail_pass)
        smtp_obj.sendmail(sender, [target, ], message.as_string())
        print("success: from {}, to {}".format(sender, target))
    except smtplib.SMTPException:
        print("Error: send failed")
    finally:
        smtp_obj.quit()


def parse_request(request: ERequest):
    return "您有新的问题待审核。请登录网站查询。"


def parse_answer_request(answer: EAnswer):
    return "您有新提交的答案待审核。请登录网站查询。"
