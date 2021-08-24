import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr

from faq.models import ERequest, EAnswer


def get_config(config_path='faq_secret.ini'):
    import configparser
    _conf = configparser.ConfigParser()
    _conf.read(config_path)
    assert "smtp" in _conf
    assert "host" in _conf['smtp']
    assert "smtp_user" in _conf['smtp']
    assert "smtp_license" in _conf['smtp']
    return _conf['smtp']


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
    message['To'] = Header(",".join(target), 'utf-8')
    message['Subject'] = Header("openEuler FAQ 审核通知", 'utf-8')

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtp_obj.login(mail_user, mail_pass)
        smtp_obj.sendmail(sender, [target, ], message.as_string())
        print("success")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def parse_request(request: ERequest):
    return "您有新的问题待审核。请登录网站查询。"


def parse_answer_request(answer: EAnswer):
    return "您有新提交的答案待审核。请登录网站查询。"
