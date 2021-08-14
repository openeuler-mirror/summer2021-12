# review API
- [review API](#review-api)
  - [审核界面](#审核界面)
      - [待审核问题展示接口](#待审核问题展示接口)
      - [获得所有审核通过的标准问题及详细信息](#获得所有审核通过的标准问题及详细信息)
      - [获得特定问题的所有解答](#获得特定问题的所有解答)
      - [问题审核接口](#问题审核接口)
      - [待审解答展示接口](#待审解答展示接口)
      - [解答审批接口](#解答审批接口)

## 审核界面

#### 待审核问题展示接口

- 请求
  - method: `GET`
  - url

    ```
    https://<>/review/{user_id}/show/requests
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | user_id     | 20 位 string  | 审核员在数据库中主键 |

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

#### 获得所有审核通过的标准问题及详细信息

- 描述: 用于选择合并同义问题
- 请求
  - method: `GET`
  - url

    ```
    https://<>/review/{user_id}/show/questions
    ```

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

#### 获得特定问题的所有解答

- 请求
  - url

    ```
    https://<>/review/{user_id}/show/answers/{question_id}
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | user_id     | 20 位 string  | 审核员在数据库中主键 |
    | question_id | string(20)      | 对应问题主键|

- 响应
  - body:`json`

    ```json
    {
        "status":200,
        "body": [
            {
                "id":"",
                "q_id":"",
                "type":"",
                "content": "",
                "summary": "",
                "level": ""
            }
        ]
    }
    ```


#### 问题审核接口

- 请求
  - method: `POST`
  - url

    ```
    https://<>/review/{user_id}/handle/question
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | user_id     | 20 位 string  | 审核员在数据库中主键 |

  - body: `json`

    ```json
    {
        "id": "",   // string(20)
        "description": "",  // string(200)
        "comment": "", // 审核意见
        "allowed": true, // 若此处为 false, 则 self_answer.allowed 取 true 无效, 同时 merged 取 true 无效
        "merged": false, // 是否合并为同义问题, 若 false 则 merge_q 字段无效
        "merge_q": "", // 同义问题 id
        "merging_label": false, // 若合并同义问题, 是否合并标签 (取并集), 否则将舍弃 "tags" 字段
        "tags": [
            "label name"  // string(100)
        ],
        "self_answers": [
            {
                "id": "",
                "allowed": false, // 是否收录, boolean
                "comment": "", // 审核意见 string(200)
                "type": "",
                "content": "",
                "summary": "",
                "level": "" // string 解答的等级
            }
        ],
        "adjusted_answer": [ // 调整过解答等级的解答. 为了添加新解答, 可能需要调整一些解答的等级.
            {
                "id": "",
                "level": ""
            }
        ]
    }
    ```

- 响应

  ```json
  {
      "status": 200,
      "body": {}
  }
  ```
  ```json
  {
      "status": 500, // 错误
      "body": {
          "reason":"",
          "details": ""
      }
  }
  ```

#### 待审解答展示接口

- 请求
  - method: `GET`
  - url

    ```
    https://<>/review/{user_id}/show/answer-requests
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | user_id     | 20 位 string  | 审核员在数据库中主键 |

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

#### 解答审批接口

- 请求:
  - method: `POST`
  - url

    ```
    https://<>/review/{user_id}/handle/answer-requests
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | user_id     | 20 位 string  | 审核员在数据库中主键 |

  - body: `json`

    ```json
    {
        "status":200,
        "body":{
            "id":"",
            "allowed":false,
            "q_id":"",
            "type":"",
            "content":"",
            "summary":"",
            "level":"",
            "comment":"",
            "adjusted_answers":[
                {
                    "id":"",
                    "level":""
                }
            ]
        }
    }
    ```