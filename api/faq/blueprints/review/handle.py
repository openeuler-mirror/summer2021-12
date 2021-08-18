from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError

from faq import db
from faq.models import EUser, RRoleAttaching, \
    ETag, CAnswerType, CAnswerLevel, ERequest, \
    ESelfAnswer, EQuestion, RQuestionTagging, EAnswer, EQuestionDescription

bp = Blueprint(name='review_handle', import_name=__name__, url_prefix='/review/handle')

REVIEW_STATE = {'WAITING': '1', 'ALLOWED': '2', 'DENIED': '3'}
ANSWER_LEVEL = {'STD': '1', 'GOOD': '2', 'DEPRECATED': '3', 'UNDEFINED': '4', 'DENIED': '5'}


@bp.route('/requests/<user_id>', methods=['POST'])
def handle_request(user_id):
    req_body = request.get_json()
    msg, status = check_request(user_id, req_body)
    if status != 200:
        return jsonify(status=status, msg=msg)

    # no matter what happen, update the review state & comment.
    update_reviewing_status(req_body)
    if status != 200:
        return jsonify(status=status, msg=msg)
    # totally nothing wrong now. you can store it without check.
    persistence(req_body, user_id)

    return jsonify(status=200, msg="acknowledged")


def persistence(req_body, user_id):
    if not req_body['allowed']:
        pass
    elif not req_body['merged']:
        new_q = EQuestion(std_description=req_body['description'])
        db.session.add(new_q)
        db.session.add(EQuestionDescription(description=req_body['description'],
                                            question_id=new_q.id))
        db.session.commit()
        add_taggings(new_q, req_body)
        insert_answers_from_self_ans(new_q, req_body, user_id)
        db.session.commit()
    else:
        std_q = EQuestion.query.get(req_body['merge_q'])
        db.session.add(EQuestionDescription(description=req_body['description'],
                                            question_id=std_q.id))
        insert_answers_from_self_ans(std_q, req_body, user_id)
        for adjusted in req_body['adjusted_answers']:
            level_id = CAnswerLevel.query.filter_by(level=adjusted['level'])
            EAnswer.query.get(adjusted['id']).update({'level_id': level_id})
        if req_body['merging_label']:
            add_taggings(std_q, req_body)
        db.session.commit()


def add_taggings(q, req_body):
    for tag_name in req_body['tags']:
        if ETag.query.filter_by(tag_name=tag_name).first() is None:
            db.session.add(ETag(tag_name=tag_name))
            db.session.commit()
        etag: ETag = ETag.query.filter_by(tag_name=tag_name)
        if RQuestionTagging.query \
                .filter_by(question_id=q.id, tag_id=etag.id) \
                .first() is None:
            db.session.add(RQuestionTagging(question_id=q.id, tag_id=etag.id))


def insert_answers_from_self_ans(q, req_body, user_id):
    for self_ans in req_body['self_answers']:
        if self_ans['allowed']:
            type_id = CAnswerType.query \
                .filter_by(type_name=self_ans['type']).first().id
            level_id = CAnswerLevel.query \
                .filter_by(level_name=self_ans['level']).first().id
            db.session.add(EAnswer(type_id=type_id,
                                   content=self_ans['content'],
                                   summary=self_ans['summary'],
                                   author_id=self_ans['author_id'],
                                   question_id=q.id,
                                   level_id=level_id,
                                   reviewer_id=user_id,
                                   comment=self_ans['comment']))


def update_reviewing_status(req_body):
    e_request: ERequest = ERequest.query.get(req_body['id'])
    e_request.review_status = REVIEW_STATE['ALLOWED'] \
        if req_body['allowed'] else REVIEW_STATE['DENIED']
    e_request.comment = req_body['comment']
    for answer in req_body['self_answers']:
        e_self_ans = ESelfAnswer.query.get(answer['id'])
        if e_self_ans is not None:
            e_self_ans.review_status = REVIEW_STATE['ALLOWED'] \
                if answer['allowed'] and req_body['allowed'] \
                else REVIEW_STATE['DENIED']
            e_self_ans.comment = answer['comment']


def check_request(user_id, req_body):
    if EUser.query.filter_by(id=user_id).first() is None:
        return '账户不存在', 500
    if RRoleAttaching.query.filter_by(user_id=user_id, role_id='2') \
            .first() is None:
        return '该用户没有审核权限', 500
    if request.is_json:
        handle_request_schema = {
            "title": "handle requests",
            "description": "the body when handling requests",
            "type": "object",
            "properties": {
                "id": {"type": "string", "maxLength": 20},
                "description": {"type": "string", "maxLength": 200},
                "comment": {"type": "string", "maxLength": 200},
                "allowed": {"type": "boolean"},
                "merged": {"type": "boolean"},
                "merge_q": {"type": "string", "maxLength": 20},
                "merging_label": {"type": "boolean"},
                "tags": {
                    "type": "array",
                    "items": {"enum": [tag.tag_name for tag in ETag.query.all()]},
                    "uniqueItems": True
                },
                "self_answers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "maxLength": 20},
                            "allowed": {"type": "boolean", "default": False},
                            "comment": {"type": "string", "maxLength": 200},
                            "type": {"enum": [elem.type_name for elem in CAnswerType.query.all()]},
                            "content": {"type": "string", "maxLength": 200},
                            "summary": {"type": "string", "maxLength": 200},
                            "author_id": {"type": "string", "maxLength": 20},
                            "level": {"enum": [elem.level for elem in CAnswerLevel.query.all()]}
                        },
                        "required": ["id", "allowed", "comment", "author_id",
                                     "type", "content", "summary", "level"]
                    }
                },
                "adjusted_answers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "maxLength": 20},
                            "level": {
                                "enum": [level.level for level in CAnswerLevel.query.all()]}
                        },
                        "required": ["id", "level"]
                    },
                    "uniqueItems": True
                }
            },
            "required": ["id", "description", "comment", "allowed",
                         "merged", "merge_q", "merging_label", "tags",
                         "self_answers", "adjusted_answers"]
        }
        try:
            validate(req_body, handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(".".join([str(i) for i in e.path]), e.message)
            return msg, 500
    else:
        return "请求体必须是JSON格式", 500

    if ERequest.query.get(req_body['id']).first() is None:
        return "该新增问题请求不存在", 500
    if req_body['allowed'] and req_body['merged'] \
            and EQuestion.query.get(req_body['merge_q']).first() is None:
        return "待合并的标准问题不存在", 500
    # every question must have only one std answer.
    if req_body['allowed']:
        if not req_body['merged']:
            if sum([(1 if self_ans.level == 'std' else 0) for self_ans in req_body['self_answers']]) > 1:
                return "只能有一个回答级别为标准回答", 500
        else:
            adjusted: dict = {elem['id']: elem['level'] for elem in req_body['adjusted_answers']}
            n_std: int = 0
            for e_ans in EAnswer.query.all():
                level = e_ans.level if not adjusted.has_key(e_ans.id) else adjusted.get(e_ans.id)
                n_std += 1 if level == ANSWER_LEVEL['STD'] else 0
                if n_std > 1:
                    return "只能有一个标准回答", 500
    return "", 200


@bp.route('/answer-requests/<user_id>', methods=['POST'])
def handle_answer_requests(user_id):
    req_body = request.get_json()
    msg, status = arg_check(user_id, req_body)
    if status != 200:
        return jsonify(status=status, msg=msg)
    type_id = CAnswerType.query.filter_by(type_name=req_body['type']).first()
    level_id = CAnswerLevel.query.filter_by(level_name=req_body['level']).first()
    EAnswer.query.get(req_body['id']).update(
        {
            'question_id': req_body[''],
            'type_id': type_id,
            'summary': req_body['summary'],
            'content': req_body['content'],
            'level_id': level_id,
            'comment': req_body['comment']
        }
    )
    for adjusted in req_body['adjusted_answers']:
        ad_level_id = CAnswerLevel.query.filter_by(level=req_body['level'])
        EAnswer.query.get(adjusted['id']).update({'level_id': ad_level_id})
    return jsonify(status=200, msg='acknowledged')


def arg_check(user_id, req_body):
    if EUser.query.filter_by(id=user_id).first() is None:
        return '账户不存在', 500
    if RRoleAttaching.query.filter_by(user_id=user_id, role_id='2') \
            .first() is None:
        return '该用户没有审核权限', 500
    if request.is_json:
        handle_request_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "type": "object",
            "required": ["id", "q_id", "type", "content", "summary", "level", "comment", "adjusted_answers"],
            "properties": {
                "id": {"maxLength": 20, "type": "string"},
                "q_id": {"maxLength": 20, "type": "string"},
                "type": {
                    "enum": [t.type_name for t in CAnswerType.query.all()],
                    "type": "string"
                },
                "content": {"maxLength": 200, "type": "string"},
                "summary": {"maxLength": 200, "type": "string"},
                "level": {
                    "enum": [ll.level for ll in CAnswerLevel.query.all()],
                    "type": "string"
                },
                "comment": {"maxLength": 200, "type": "string"},
                "adjusted_answers": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "object",
                        "required": ["id", "level"],
                        "properties": {
                            "id": {"maxLength": 20, "type": "string"},
                            "level": {
                                "enum": [ll.level for ll in CAnswerLevel.query.all()],
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
        try:
            validate(req_body, handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(".".join([str(i) for i in e.path]), e.message)
            return msg, 500
    else:
        return "请求体必须是JSON格式", 500

    if EAnswer.query.get(req_body['id']) is None \
            or EAnswer.query.get(req_body['id']).level_id != ANSWER_LEVEL['UNDEFINED']:
        return "该待审核解答不存在", 500
    adjusted = {elem['id']: elem['level'] for elem in req_body['adjusted_answers']}
    n_std = 0
    for ans in EAnswer.query.all():
        level = adjusted[ans.id] if ans.id in adjusted else ans.level.level
        n_std += 1 if level == 'std' else 0
        if n_std > 1:
            return "只能有一个标准回答", 500
    if EQuestion.query.get(req_body['q_id']) is None:
        return "问题不存在", 500
    return "", 200
