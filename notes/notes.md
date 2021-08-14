# NOTES

- [NOTES](#notes)
  - [API](#api)
    - [用户接口](#用户接口)
      - [提问接口](#提问接口)
      - [贡献问题接口 (提问并回答)](#贡献问题接口-提问并回答)
      - [贡献解答接口](#贡献解答接口)
      - [修改解答接口](#修改解答接口)
      - [问题简答筛选接口](#问题简答筛选接口)
      - [由问题获得对应答案](#由问题获得对应答案)
    - [审核接口](#审核接口)
      - [](#)

## API

### 用户接口

#### 提问接口

  - 描述: 符合置信度的标准问题匹配和相关解答信息, 
  - method: `GET`
  - 参数:
    - param

      | Key               | Value     | Meaning     |
      | --                | --        | --          |
      | `q`               | string    | 问题字面值   |
      | `AnswerLevel`    | string | 解答包含等级, 取值: `STD_ONLY` 仅包含标准答案 (一个), `GOOD_ONLY` 包括标准答案和优秀答案, `ALL` 返回所有提交的答案, 包括被否决或弃用的 |
      | `IncludeUnanswered` | boolean (true/false) | 是否匹配未解答的 问题, (由 `Answer-Level` 控制导致的 解答为空也在此列) |
      | `RelatedQuestionTopN` | Integer | 用于控制响应数据中 相关问题 的个数 (`"related_questions"`), 若该值为 5, 则 `related_questions.length == 4`

  - 返回：
    - json

      ```json
      {
        "status": 200,
        "data": {
          "id": "",  // string 标准问题实体主键
          "std_question": "", // string
          "latest_editor": "",
          "labels": [
            {
              "id": "",
              "value": "",
            }
          ], // list<string>
          "answers": [
            {
              "id": "", // 解答主键
              "level": "", // string, 取值: `std`, `good`, `deprecated`
              "type": "", // string, 媒体类型
              "summary": "", // string
              "resource_url": "", 
              "latest_editor": "",
              "latest_edit_time": "" // datetime
            }
          ], 
          "related_questions": [
            {
              "id": "", // 标准问题实体主键
              "question": "", // 问题题面
            }
          ]
        }
      }
      ```

  - 返回说明：
    - `"std_q"`: 匹配的标准问题 (naive 解使用 sql: like #{} limit 1)
    - `"std_labels"`: 标准问题所有标签
    - `"answers"`: 标准问题对应的标准解答
      - 回答的选优,排序? 
        - `"level"`: 解答分为 3 级: `std`, `good`, `deprecated`
        - 接口设置参数包含哪一层次的解答: answer_level: `STD_ONLY`, `GOOD_ONLY`, `ALL`
        - `"type"` 类别 (视频, 文字简答) 第一排序, 解答的等级第二排序
    - 其他相关内容 (待定):
      - 通过 搜索引擎 原理, 直接对所有解答进行检索的 top n 
      - 相关问题: 依赖 faq 接口的具体实现, 比如特定置信区间 top n 除 标准问题 之外的匹配

#### 贡献问题接口 (提问并回答)

- 描述: 若找不到满意的问题匹配, 可选择添加新问题, 用户可编辑问题字面, 加标签 (选择已有的或自定义, 可以使用带有 推荐功能 的输入框), 添加一个解答, 各个类型解答允许各添加一个. 这个问题将通过 分流器 转发给 相应的 管理人员, 管理人员将选择如何处理该问题 (专门的接口)
- method: `POST`
- 参数:
  - body

    ```json
    {
        "question": "",             // 问题字面值
        "editor": "",               // string, 最新贡献者 id
        "std_labels": [],           // 标准标签, 指已存在数据库中的标签, list of id
        "cus_labels": ["",""],      // 自定义的 label, list of label value
        "answers": [
          {
            "type": "",             // string, 媒体类型
            "summary": "",          // string
            "resource_url": "", 
            "latest_editor": "",
            "latest_edit_time": ""  // datetime
          }
        ],      // 可能的回答
    }
    ```
  
- 返回: 成功或失败
  - 失败: 邮件发送或参数检查不通过, 不符合预定的逻辑

#### 贡献解答接口

- 描述: 选择已有的问题, 仅添加解答
- method: `POST`
- 参数
  - body: json

    ```json
    {
      "q_id": "", // 标准问题 主键
      "editor": "", // 贡献者 id
      "answers": [
        {
          "type": "", // string, 媒体类型
          "summary": "", // string
          "resource_url": "", 
          "latest_editor": "",
        }
      ]
    }
    ```

#### 修改解答接口

- method: `POST`
- 参数
  - body: json

    ```json
    {
      "id": "", // 选择的 解答 主键
      "summary": "",
      "resource_url": "",
      "editor": "", // 修改者
    }
    ```

#### 问题简答筛选接口

  - 描述: 简单的数据查询, 多条件查询, 搜索对象是标准问题, (同义问题应当隐藏在实现中)
  - method: `POST`
  - 参数
    - param

        |  参数     |  取值  | 描述             |
        | ----      |  ---   | ---              |
        | q | string  | 问题字面值, `%#{}%` 模糊搜索     |
        | from_time | datetime  | 最近回答修改时间, 起  |
        | to_time | datetime  | 最近回答修改时间, 止  |
        | editor    | string  | 发起问题的用户, gitee/github user id  |
        | answered  | boolean   | 回答是否为空, 为空则为 true|
        | filtered_with_label| boolean | 是否使用 label 过滤, 为 true 时 body 不得为空|
        | include_unanswered | boolean | 是否包含回答为空的 (由 `answer_level` 控制导致的 解答为空也在此列)|
    - body

      ```json
      {
          "labels": ["example", "labels"]
      }
      ```
    
  - 返回

    ```json
    {
        "status": 200,
        "data": [
          {
            "q_id": "",           // 标准问题 主键
            "q_content": "",      // 标准问题 内容
            "edit_time": "",      // 最晚编辑时间 datetime
            "editor" : "",        // 编辑者 string
            "labels": ["",""],    // 该问题包含的所有标签字面值
          }
        ]
    }
    ```

#### 由问题获得对应答案

- method: `GET`
- 参数
  - param

    | key     | value       | meaning     |
    | --      | --          | --          |
    | q_id    | string      | 问题主键     |
    | answer_level | string | 取值: `STD_ONLY` 仅包含标准解答, `GOOD_ONLY` 包含所有优秀解答, `ALL` 包括所有解答, 包括 deprecated |

- 返回
  - body: json

    ```json
    {
      "status": 200,
      "data": {
        "answers": [
          {
            "id": "",               // 解答主键
            "level": "",            // string, 取值: `std`, `good`, `deprecated`
            "type": "",             // string, 媒体类型
            "summary": "",          // string
            "resource_url": "", 
            "latest_editor": "",
            "latest_edit_time": ""  // datetime
          }
        ]
      }
    }
    ```

### 审核接口

- 何时要审核: 问题的增加, 解答的增加和修改
- 情景: 审核员将接到一封邮件, 包含信息:
  - 问题增加
    - 增加的问题, 问题标签
  - 解答新增
    - 被解答的问题, 问题标签
    - 解答详情
    - 解答人
  - 解答修改
    - 被解答的问题, 问题标签
    - 原解答详情
    - 原解答人
    - 解答详情
    - 解答人

#### 
