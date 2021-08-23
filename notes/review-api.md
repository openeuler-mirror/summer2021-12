# review API
- [review API](#review-api)
  - [审核界面](#审核界面)
      - [问题审核接口](#问题审核接口)
      - [解答审批接口](#解答审批接口)

## 审核界面

#### 问题审核接口

- 
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
                "allowed": false, // 是否收录, boolean
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

#### 解答审批接口

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
