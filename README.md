# Summer2021-No.12 为openEuler社区提供一个FAQ的web服务

## Intro

https://gitee.com/openeuler-competition/summer-2021/issues/I3DV2B

## Link

项目过程中用于练习和尝试的仓库：https://gitee.com/YoungY620/open-source-summer-casual-space

## usage

clone repo

```shell
$ git clone https://gitee.com/openeuler-competition/summer2021-12.git
```

add a config file (required)

```shell
$ cd summer2021-12/api && touch faq_secret.ini
```

example content in `/api/faq_secret.ini`:

```
[elastic]
cloud_id = your-deployment:kjbfvb576fvjgv4e6cuvbkb9...
user = elastic
password = <password>

[mysql]
username = root
password = 
ip = 127.0.0.1
port = 3306

[smtp]
host = "smtp.QQ.com"
smtp_user = "xxx@qq.com"
smtp_license = <smtp 服务授权码>
```