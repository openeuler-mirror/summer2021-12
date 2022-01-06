class ElasticConfig:
    ES_CLOUD_ID = "your-deployment:cloud_id"
    ES_USERNAME = "elastic"
    ES_PASSWORD = "password"
    ES_HOST = "localhost"
    ES_PORT = 9200


class DevConfig:
    SECRET_KEY = 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://username:password@host:port/openeuler_faq"


class SMTPConfig:
    SMTP_HOST = "smtp.QQ.com"
    SMTP_USER = "xxx@qq.com"
    SMTP_LICENSE = "license"


class TestConfig:
    USER = "root"
    PASSWORD = "password"
    IP = "127.0.0.1"
    PORT = 3306
    DATABASE = "openeuler_faq"
