class ElasticConfig:
    CLOUD_ID = "your-deployment:cloud_id"
    USERNAME = "elastic"
    PASSWORD = "password"


class DevConfig:
    SECRET_KEY = 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://username:password@host:port/openeuler_faq"


class SMTPConfig:
    HOST = "smtp.QQ.com"
    USER = "xxx@qq.com"
    LICENSE = "license"


class TestConfig:
    USER = "root"
    PASSWORD = "password"
    IP = "127.0.0.1"
    PORT = 3306
    DATABASE = "openeuler_faq"
