# show api

- [show api](#show-api)
    - [待审核问题(request)展示接口](#待审核问题request展示接口)
    - [获得所有审核通过的问题 (question)](#获得所有审核通过的问题-question)
    - [获得特定已过审问题(question)的所有解答](#获得特定已过审问题question的所有解答)
    - [待审解答(answer-request)展示接口](#待审解答answer-request展示接口)
    - [查看某人所有贡献解答](#查看某人所有贡献解答)
    - [查看某人所有贡献问题](#查看某人所有贡献问题)

### 待审核问题(request)展示接口

- 请求
  - method: `GET`
  - url

    ```
    https://<>/show/requests-to-review/{reviewer_id}
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | reviewer_id     | 20 位 string  | 审核员在数据库中主键 |

  - param

    | param key     | value         | meaning   |
    | --            | --            | --        |
    | page_size     | int           | 分页查询大小, 即返回条数|
    | page          | int           | 分页查询页码 |
    
- 响应
  - response type: `JSON`

    ```json
    {
        "status": 200,
        "body": [
            {
                "id": "",
                "q_description": "", 
                "time": "", // datetime 创作时间
                "author": {
                    "id": "",
                    "username": "",
                    "avatar_url": ""
                },
                "tags": ["label name 1"],
                "self_answers": [
                    {
                        "type": "",
                        "summary": "",
                        "content": ""
                    }
                ]
            }
        ]
    }
    ```

### 获得所有审核通过的问题 (question)

- 描述: 用于选择合并同义问题, 以及其他场景. 屏蔽掉未审核通过的问题
- 请求
  - method: `GET`
  - url

    ```
    https://<>/show/questions
    ```

  - param

    | param key     | value         | meaning   |
    | --            | --            | --        |
    | page_size     | int           | 分页查询大小, 即返回条数|
    | page          | int           | 分页查询页码 |
    
- 响应
  - body: `json`

    ```json
    {
        "status":200,
        "body":[
            {
                "id":"",
                "std_description": "",
                "descriptions": [
                    "aaa"
                ],
                "tags": [
                    "label name"
                ]
            }
        ]
    }
    ```

### 获得特定已过审问题(question)的所有解答

- 请求
  - url

    ```
    https://<>/show/answers-of-q/{question_id}
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | question_id | string(20)      | 对应问题主键 |

- 响应
  - body:`json`

    ```json
    {
        "status":200,
        "body": [
            {
                "id":"",
                "q_id":"",
                "type":"", // 枚举值, 不是序号 id
                "content": "",
                "summary": "",
                "level": "", // 枚举值, 不是序号
                "author": {
                    "id":"",
                    "name":"",
                    "avatar_url": ""
                }
            }
        ]
    }
    ```


### 待审解答(answer-request)展示接口

- 请求
  - method: `GET`
  - url

    ```
    https://<>/show/answer-requests-to-review/{reviewer_id}
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | reviewer_id     | 20 位 string  | 审核员在数据库中主键 |

  - param

    | param key     | value         | meaning   |
    | --            | --            | --        |
    | page_size     | int           | 分页查询大小, 即返回条数|
    | page          | int           | 分页查询页码 |

- 响应
  - body: `json`

    ```json
    {
        "status": 200,
        "body": [
            {
                "id":"",
                "question":{
                    "id":"",
                    "std-description":"",
                    "tags": ["",""]
                },
                "type": "",
                "content": "",
                "summary": "",
                "author": {
                    "id":"",
                    "name": "",
                    "avatar_url": ""
                }
            }
        ]
    }
    ```

### 查看某人所有贡献解答

- 请求
  - method：`get`
  - url

    ```
    https://<>/show/my-answers/{author_id}
    ```

    | path variable | value         | info      |
    | author_id     | string(20)    | 作者的主键    |

  - param

    | param key     | value         | meaning                   |
    | --            | --            | --                        |
    | page_size     | int           | 分页查询大小, 即返回条数      |
    | page          | int           | 分页查询页码              |

- 响应
  - json

    ```json
    {
        "status": 200,
        "body": [
            {
                "id":"",
                "level": "",
                "reviewer": {
                    "id": "",
                    "name": "",
                    "avatar_url": ""
                },
                "question":{
                    "id":"",
                    "std-description":"",
                    "tags": ["",""]
                },
                "type": "",
                "content": "",
                "summary": "",
                "author": {
                    "id":"",
                    "name": "",
                    "avatar_url": ""
                }
            }
        ]
    }
    ```

### 查看某人所有贡献问题

- 请求
  - method: `get`
  - url

    ```
    https: //<>/show/my-requests/{author_id}
    ```
  
  - param

    | param key     | value         | meaning                   |
    | --            | --            | --                        |
    | page_size     | int           | 分页查询大小, 即返回条数    |
    | page          | int           | 分页查询页码               |
    | show_withdrawn| boolean       | 是否显示已被撤销的         |

- 响应
  - json

    ```json
    {
        "status": 200,
        "body": [
            {
                "id": "",
                "reviewer": {///
                    "id": "",
                    "name": "",
                    "avatar_url": ""
                },
                "review_status": "", //
                "q_description": "", 
                "time": "", // datetime 创作时间
                "tags": [],
                "author": {
                    "id": "",
                    "username": "",
                    "avatar_url": ""
                },
                "self_answers": [
                    {
                        "type": "",
                        "summary": "",
                        "content": ""
                    }
                ]
            }
        ]
    }
    ```
