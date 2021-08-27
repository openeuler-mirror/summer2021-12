import pprint
import unittest

from tqdm import tqdm

from faq import create_app
from faq.models import EUser, RRoleAttaching, CUserRole


def init_database() -> bool:
    import pymysql
    msg = True
    try:
        from faq.setting import TestConfig
        db = pymysql.connect(user=TestConfig.USER,
                             password=TestConfig.PASSWORD,
                             host=TestConfig.IP,
                             port=TestConfig.PORT)
        c = db.cursor()
        with open('test.sql', encoding='utf-8', mode='r') as f:
            # 读取整个sql文件，以分号切割。[:-1]删除最后一个元素，也就是空字符串
            sql_list = f.read().split(';')[:-1]
            for x in tqdm(sql_list):
                # 判断包含空行的
                if '\n' in x:
                    # 替换空行为1个空格
                    x = x.replace('\n', ' ')
                # sql语句添加分号结尾
                sql_item = x + ';'
                # print(sql_item)
                c.execute(sql_item)
                # print("执行成功sql: %s" % sql_item)
    except Exception as e:
        print(e)
        print('执行失败sql: %s' % sql_item)
        msg = False
    finally:
        # 关闭mysql连接
        c.close()
        db.commit()
        db.close()
    return msg


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app({
            'TESTING': True
        })
        self.client = self.app.test_client()

        assert init_database()

    def test_full_flow(self):
        print('---- 发起一个 request')
        author, new_request, rv = self.raise_request()

        print("---- 查看待审 requests")
        json_body, reviewer = self.view_request_to_handle(author, new_request, rv)

        print("---- 审核、修改并通过 requests")
        self.review_requests(author, json_body, reviewer, allowed=True)

        print('---- 再发起一个 request')
        author, new_request, rv = self.raise_request()

        print("---- 再次查看待审 requests")
        json_body, reviewer = self.view_request_to_handle(author, new_request, rv)

        print("---- 审核、修改并通过 requests, 合并到已有的 question 中")
        q_id = self.review_requests_again(author, json_body, reviewer)

        print('---- 提出新 answer')
        self.raise_new_answer(q_id)

        print('---- 查看待审 answers')
        json_body, reviewer = self.view_answers_to_review(json_body, reviewer)

        print('---- 审核、修改并通过解答')
        self.review_answers(json_body, q_id, reviewer)

        print('---- 提问')
        rv = self.client.get('/user/questioning?answered_only&answer_level=std&top_k=5&q=how to install openeuler?')
        pprint.pprint(rv.get_json())
        rv = self.client.get('/user/questioning?answered_only&answer_level=deprecated&top_k=5&q=how to install '
                             'openeuler?')
        pprint.pprint(rv.get_json())

    def review_answers(self, json_body, q_id, reviewer):
        rv = self.client.get('/show/answers-of-q/{}'.format(q_id))
        # pprint.pprint(rv.get_json())
        adjusted_answers = []
        for entry in rv.get_json():
            if entry['level'] == 'std':
                adjusted_answers.append({'id': entry['id'], 'level': "deprecated"})
                break
        new_answer_handle = {
            "id": json_body[0]['id'],
            "level": "std",
            "comment": "good answer",
            "adjusted_answers": adjusted_answers
        }
        rv = self.client.post('/review/answer-requests/{}'.format(reviewer.id), json=new_answer_handle)
        assert rv.get_json() == {"msg": "acknowledged", "status": 200}

    def view_answers_to_review(self, json_body, reviewer):
        reviewer = None
        with self.app.app_context():
            reviewer_ids = list(set(
                attachment.user_id for attachment
                in RRoleAttaching.query.filter_by(
                    role_id=CUserRole.query.filter_by(type='reviewer').first().id
                )
            ))
            for reviewer_id in reviewer_ids:
                rv = self.client.get('/show/answer-requests-to-review/{}?page_size=200&page=1'.format(reviewer_id))
                json_body = rv.get_json()
                if len(json_body) != 0:
                    reviewer = EUser.query.get(reviewer_id)
                    break
        assert reviewer is not None
        return json_body, reviewer

    def raise_new_answer(self, q_id):
        with self.app.app_context():
            author = EUser.query.get('5')
        new_answer = {
            "author_id": author.id,
            "q_id": q_id,
            "type": "website",
            "content": "https://www.google.com",
            "summary": "you cannot"
        }
        rv = self.client.post('/user/answer-request', json=new_answer)
        assert rv.get_json() == {
            "msg": "acknowledged",
            "stauts": 200
        }

    def review_requests_again(self, author, json_body, reviewer):
        rv = self.client.get('/show/questions?page_size=100&page=1')
        assert rv.get_json() == [
            {
                "descriptions": [
                    "how to install openEuler on linux centos?"
                ],
                "id": rv.get_json()[0]['id'],
                "std_description": "how to install openEuler on linux centos?",
                "tags": [
                    "postman"
                ]
            }
        ]
        merge_q = rv.get_json()[0]['id']
        rv = self.client.get('/show/answers-of-q/{}'.format(merge_q))
        # pprint.pprint(rv.get_json())
        adjusted_answers = [
            {"id": rv.get_json()[0]['id'], 'level': 'good'},
            {"id": rv.get_json()[1]['id'], 'level': 'good'}
        ]
        self.review_requests(author, json_body, reviewer,
                             allowed=True, merged=True,
                             merge_q=merge_q,
                             merging_label=True,
                             tags=['apple', 'macos'],
                             adjusted_answers=adjusted_answers)
        return merge_q

    def review_requests(self, author, json_body, reviewer,
                        allowed=False, merged=False, merge_q="",
                        merging_label=False, adjusted_answers=None, tags=None):
        if adjusted_answers is None:
            adjusted_answers = []
        if tags is None:
            tags = ['postman']
        request_id = json_body['body'][0]['id']
        request_handle_body = {
            "id": request_id,
            "description": "how to install openEuler on linux centos?",
            "comment": "good question",
            "allowed": allowed,
            "merged": merged,
            "merge_q": merge_q,
            "merging_label": merging_label,
            "tags": tags,
            "self_answers": [
                {
                    'id': json_body['body'][0]['self_answers'][0]['id'],
                    'allowed': True,
                    'comment': 'good answer',
                    'type': 'text',
                    'content': 'you cannot install openEuler on centos.',
                    'summary': 'you cannot install openEuler on centos.',
                    'author_id': author.id,
                    'level': 'std'
                },
                {
                    'id': "",
                    'allowed': True,
                    'comment': 'i think it is a good answer',
                    'type': 'text',
                    'content': 'you cannot install openEuler on windows.',
                    'summary': 'you cannot install openEuler on windows.',
                    'author_id': reviewer.id,  # 允许审核者自己加一个解答
                    'level': 'good'
                }
            ],
            "adjusted_answers": adjusted_answers
        }
        # pprint.pprint(request_handle_body)
        rv = self.client.post('/review/requests/{}'.format(reviewer.id),
                              json=request_handle_body)
        print(rv.get_json())
        assert rv.get_json() == {'msg': 'acknowledged', 'status': 200}

    def view_request_to_handle(self, author, new_request, rv):
        reviewer = None
        with self.app.app_context():
            reviewer_ids = list(set(
                attachment.user_id for attachment
                in RRoleAttaching.query.filter_by(
                    role_id=CUserRole.query.filter_by(type='reviewer').first().id
                )
            ))
            for reviewer_id in reviewer_ids:
                rv = self.client.get('/show/requests-to-review/{}?page_size=100&page=1'.format(reviewer_id))
                json_body = rv.get_json()
                assert 'status' in json_body
                assert 'body' in json_body
                assert json_body['status'] == 200
                if len(json_body['body']) != 0:
                    reviewer = EUser.query.get(reviewer_id)
                    break
        assert reviewer is not None
        assert json_body == {
            'body': [
                {
                    'author': {
                        'avatar_url': author.avatar_url,
                        'id': author.id,
                        'username': author.username,
                    },
                    'id': json_body['body'][0]['id'],
                    'q_description': new_request['description'],
                    'review_status': 'waiting',
                    'reviewer': {
                        'avatar_url': reviewer.avatar_url,
                        'id': reviewer.id,
                        'username': reviewer.username
                    },
                    'self_answers': [
                        {
                            'content': 'you cannot install openEuler on linux.',
                            'id': json_body['body'][0]['self_answers'][0]['id'],
                            'summary': 'you cannot install openEuler on linux.',
                            'type': 'text'
                        },
                        {
                            'content': 'https://www.baidu.com',
                            'id': json_body['body'][0]['self_answers'][1]['id'],
                            'summary': 'you cannot install openEuler on linux.',
                            'type': 'website'
                        }
                    ],
                    'tags': new_request['tags'],
                    'time': json_body['body'][0]['time']
                }
            ],
            'status': 200
        }
        print(rv)
        return json_body, reviewer

    def raise_request(self):
        with self.app.app_context():
            author = EUser.query.get("4")
        new_request = {
            "author_id": author.id,
            "description": "how to install openEuler on windows 11?",
            "tags": ["linux", "installation"],
            "answers": [
                {
                    "type": "text",
                    "summary": "you cannot install openEuler on linux.",
                    "content": "you cannot install openEuler on linux."
                },
                {
                    "type": "website",
                    "summary": "you cannot install openEuler on linux.",
                    "content": "https://www.baidu.com"
                }
            ]
        }
        rv = self.client.post('/user/request', json=new_request)
        print(rv)
        assert rv.get_json() == {
            "msg": "acknowledged",
            "stauts": 200
        }
        return author, new_request, rv


if __name__ == '__main__':
    unittest.main()
