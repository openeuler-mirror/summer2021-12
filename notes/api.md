## 审核接口

### 问题审核接口

- 请求
  - method: `POST`
  - url

    ```
    https://<>/review/requests/{user_id}
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
            "label name"  // string(100) 最终有且仅有这些 tag 会挂在 这个新建的问题上
        ],
        "self_answers": [ // 若不加申明则为 denied
            {
                "id": "", // 若为管理员自己新加的解答(数据库中没有), 则同样添加为新解答
                "allowed": false, // 是否收录, boolean, 若不加到 `self_answers` 则默认为被否决
                "comment": "", // 审核意见 string(200)
                "type": "",
                "content": "",
                "summary": "",
                "author_id":"",
                "level": "" // string 解答的等级
            }
        ],
        "adjusted_answers": [ // 调整过解答等级的解答. 为了添加新解答, 可能需要调整一些解答的等级.
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

### 解答审批接口

- 请求:
  - method: `POST`
  - url

    ```
    https://<>/review/handle/answer-requests/{user_id}
    ```

    | path variable | value         | meaning   |
    | ---           | ---           | ---       |
    | user_id     | 20 位 string  | 审核员在数据库中主键 |

  - body: `json`

    ```json
    {
        "id":"",
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
    
    ```

## 用户接口

### 提问接口

- 描述: 就是首页的巨大的搜索框
- 请求
  - method: `get`
  - url

    ```
    https://<>/user/questioning?answered_only&answer_level=std&top_k=5&q=who is bob
    ```

  - param

    | param name    | value     | info      |
    | ---           | ---       | ---       |
    | answered_only | boolean   | 是否只看有答案的, 匹配到没有答案的问题将显示为失配. 有没有答案也受答案等级选择的影响 |
    | answer_level  | string    | 返回答案的等级. 目前取值为 (等级从高到低) `std` `good` `deprecate` `undetermined` `denied`. 选择某一等级后将显示高于这一等级的解答， 默认 std|
    | top_k         | integer   | 返回最相关的前几个问题, 默认 1 |
    | q             | string    | 用户在搜索框中输入的内容  |

- 响应
  - json

    ```json
    {
        "status": 200,
        "body": [
          {
            "id": "", // 问题的主键
            "std_description": "",
            "descriptions": [],
            "tags": [],
            "answers": [
              {
                "id": "", // 解答的主键
                "type": "",
                "level": "",
                "author": {
                  "id": "",
                  "name": "",
                  "avatar_url": ""
                },
                "content": "",
                "summary": "",
                "reviewer": {
                  "id": "",
                  "name": "",
                  "author": ""
                }
              }
            ]
          }
        ]
    }
    ```

### 贡献问题

- 请求
  - method: `post`
  - url

    ```
    https://<>/user/request
    ```

  - body: json

    ```json
    {
      "author_id": "", 
      "description": "",
      "tags": [""],
      "answers": [
        {
          "type": "",
          "summary": "",
          "content": ""
        }
      ]
    }
    ```

- 响应
  - body: json

    ```json
    {
      "status": 200,
      "msg": "acknowledged"
    }
    ```

### 贡献解答

- 请求
  - method: `get`
  - url

    ```
    https://<>/user/answer-request
    ```

  - body: json

    ```
    {
      "author_id": "",
      "q_id": "",
      "type": "",
      "content": "",
      "summary": ""
    }
    ```

- 响应
  - body: json

    ```json
    {
      "status": 200,
      "msg": "acknowledged"
    }
    ```

### 撤回解答

- 请求
  - methods： get
  - url：https://<>/user/withdraw-answer
  - param

    | param key   | value       | info         |
    | a_id        | string(20)  | 要撤回的answer  |

### 撤回问题

- 请求
  - method: get
  - https://<>/user/withdraw-request
  - param

    | param key   | value       | info         |
    | q_id        | string(20)  | 要撤回的问题  |

- 响应

  ```json
  {
    "status": 200,
    ""
  }
  ```

## 展示接口(查询接口)

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

## 用于表单填写的数据(下拉表单项, 填写辅助等)

### 解答等级枚举

- 请求
  - method: `get`
  - url

    ```
    https://<>/form/enum/answer-level
    ```

- 返回
  - body: json

    ```json
    {
        "data": [
            {
                "id": "1",
                "level": "std"
            },
            {
                "id": "2",
                "level": "good"
            },
            {
                "id": "3",
                "level": "deprecated"
            },
            {
                "id": "4",
                "level": "undetermined"
            },
            {
                "id": "5",
                "level": "denied"
            }
        ],
        "status": 200
    }
    ```

### 解答类型枚举

- 请求
  - method: `get`
  - url

    ```
    https://<>/form/enum/answer-type
    ```

- 返回
  - body

    ```json
    {
        "data": [
            {
                "id": "1",
                "type_name": "text"
            },
            {
                "id": "2",
                "type_name": "video"
            },
            {
                "id": "3",
                "type_name": "website"
            }
        ],
        "status": 200
    }
    ```

### 审核状态枚举

- 请求
  - method: `get`
  - url

    ```
    https://<>/form/enum/review-status
    ```
  
- 返回
  - body: json

    ```json
    {
        "data": [
            {
                "id": "1",
                "type": "waiting"
            },
            {
                "id": "2",
                "type": "allowed"
            },
            {
                "id": "3",
                "type": "denied"
            },
            {
                "id": "4",
                "type": "withdrawn"
            }
        ],
        "status": 200
    }
    ```

### 标签的检索, 推荐

- 描述：在填写表单时，需要标签的模糊搜索以便于选择
- 请求
  - method: `get`
  - url

    ```
    https: //<>/user/tag
    ```

  - param

    | param key | value     | info      |
    | match     | string    | 匹配标签    |
    | top_k      | integer   | 给出最匹配的几个 label |
  
- 响应
  - json

    ```json
    {
      "status": 200,
      "body": ["a","b"]
    }
    ```

## 日志接口

贡献日志自动存在 request 表中, 其他的日志需要手动记录

### 解答浏览日志

- 请求
  - method: `post`
  - url
    
    ```
    https://<>/log/answer-browsing
    ```

  - body

    ```json
    {
        "user_id": "",
        "answer_id": "",
        "type": ""
    }
    ```

### 提问日志

- 请求
  - method: `post`
  - url

    ```
    https://<>/log/questioning
    ```

  - body

    ```json
    {
        "user_q": "", //用户输入到搜索框中的文字
        "user_id": "",
        "matched_q_id": "", // 匹配到的标准问题 id
        "type": "dislike" // 日志类型
    }
    ```
