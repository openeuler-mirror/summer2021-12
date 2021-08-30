# form init api

- [form init api](#form-init-api)
    - [解答等级枚举](#解答等级枚举)
    - [解答类型枚举](#解答类型枚举)
    - [审核状态枚举](#审核状态枚举)
    - [标签的检索, 推荐](#标签的检索-推荐)

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

