# Summer2021-No.12 为openEuler社区提供一个FAQ的web服务

## Intro

https://gitee.com/openeuler-competition/summer-2021/issues/I3DV2B

## Link

项目过程中用于练习和尝试的仓库：https://gitee.com/YoungY620/open-source-summer-casual-space

## Usage

克隆仓库

```shell
$ git clone https://gitee.com/openeuler-competition/summer2021-12.git
```

创建配置文件: `api/faq/setting.py` (required)

`api/faq/setting.example.py` 是一个用于说明配置文件格式的例子。直接将其复制并按需要修改即可。

```shell
$ cd summer2021-12 && cat api/faq/setting.example.py > api/faq/setting.py
```

`api/tests/test_faq.py` 中有一个全流程的测试, 用于回归测试及说明系统的使用方法和流程.
