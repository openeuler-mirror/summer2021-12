# 日志

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
