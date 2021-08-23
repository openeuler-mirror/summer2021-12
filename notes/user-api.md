# API

- [API](#api)
    - [提问接口](#提问接口)
    - [贡献问题](#贡献问题)
    - [贡献解答](#贡献解答)
    - [撤回解答](#撤回解答)
    - [撤回问题](#撤回问题)

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
