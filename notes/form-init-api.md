# form init api

- [form init api](#form-init-api)
  - [enum](#enum)
  - [标签的检索, 推荐?](#标签的检索-推荐)

## enum

## 标签的检索, 推荐?

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

