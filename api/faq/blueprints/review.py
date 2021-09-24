from flask import Blueprint, jsonify, request, make_response
from jsonschema import validate, ValidationError

from faq import db
from faq.es_handler import sync_es
from faq.models import EUser, RRoleAttaching, \
    ETag, CAnswerType, CAnswerLevel, ERequest, \
    ESelfAnswer, EQuestion, RQuestionTagging, EAnswer, \
    EQuestionDescription, CReviewStatu, RRequestTagging

bp = Blueprint(name='review', import_name=__name__, url_prefix='/review')


def __review_status_id(name: str) -> str:
    name = name.lower()
    return CReviewStatu.query.filter_by(type=name).first().id


def __answer_level_id(name: str) -> str:
    name = name.lower()
    return CAnswerLevel.query.filter_by(level=name).first().id


@bp.route('/requests/<reviewer_id>', methods=['POST'])
def handle_request(reviewer_id):
    req_body = request.get_json()
    msg, status = check_request(reviewer_id, req_body)
    if status != 200:
        return make_response(jsonify(status=status, msg=msg), status)

    # no matter what happen, update the review state & comment.
    update_reviewing_status(req_body)
    # totally nothing wrong now. you can store it without check.
    persistence(req_body, reviewer_id)

    return make_response(jsonify(status=200, msg="acknowledged"))


def persistence(req_body, user_id):
    e_request = ERequest.query.get(req_body['id'])
    description = req_body['description'] \
        if 'description' in req_body \
        else e_request.description
    if not req_body['allowed']:
        return
    if not req_body['merged']:
        new_q = EQuestion(std_description=description)
        db.session.add(new_q)
        db.session.commit()
        db.session.add(EQuestionDescription(description=description,
                                            question_id=new_q.id))
        db.session.commit()
        add_taggings(new_q, req_body)
        insert_answers_from_self_ans(new_q, req_body, user_id)
        db.session.commit()
    else:
        std_q = EQuestion.query.get(req_body['merge_q'])
        db.session.add(EQuestionDescription(description=description,
                                            question_id=std_q.id))
        insert_answers_from_self_ans(std_q, req_body, user_id)
        for adjusted in req_body['adjusted_answers']:
            level_id = CAnswerLevel.query.filter_by(level=adjusted['level']).first().id
            adjusted_ans = EAnswer.query.get(adjusted['id'])
            adjusted_ans.level_id = level_id
        if req_body['merging_label']:
            add_taggings(std_q, req_body)
        db.session.commit()

    sync_es()  # naive solution for now
    # # todo: in whatever situation, add a new document in elasticsearch.
    # if req_body['merged'] and req_body['merging_label']:
    #     # todo: update all the doc of the same std question.
    #     pass


def add_taggings(q, req_body):
    if 'tags' in req_body:
        for tag_name in req_body['tags']:
            if ETag.query.filter_by(tag_name=tag_name).first() is None:
                db.session.add(ETag(tag_name=tag_name))
                db.session.commit()
            etag: ETag = ETag.query.filter_by(tag_name=tag_name).first()
            if RQuestionTagging.query \
                    .filter_by(question_id=q.id, tag_id=etag.id) \
                    .first() is None:
                db.session.add(RQuestionTagging(question_id=q.id,
                                                tag_id=etag.id))
    else:
        for tagging in RRequestTagging.query \
                .filter_by(request_id=req_body['id']):
            if RQuestionTagging \
                    .query.filter_by(question_id=q.id,
                                     tag_id=tagging.id) \
                    .first() is None:
                db.session.add(RQuestionTagging(question_id=q.id,
                                                tag_id=tagging.id))


def insert_answers_from_self_ans(q, req_body, user_id):
    for self_ans in req_body['self_answers']:
        if self_ans['allowed']:
            type_id = CAnswerType.query \
                .filter_by(type_name=self_ans['type']).first().id
            level_id = CAnswerLevel.query \
                .filter_by(level=self_ans['level']).first().id
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
    e_request.review_status = __review_status_id('ALLOWED') \
        if req_body['allowed'] else __review_status_id('DENIED')
    e_request.comment = req_body['comment']
    for answer in req_body['self_answers']:
        e_self_ans = ESelfAnswer.query.get(answer['id'])
        if e_self_ans is not None:
            e_self_ans.review_status = __review_status_id('allowed') \
                if answer['allowed'] and req_body['allowed'] \
                else __review_status_id('denied')
            e_self_ans.comment = answer['comment']
    for answer in e_request.e_self_answers:
        if answer.review_status == __review_status_id('waiting'):
            answer.review_status = __review_status_id('denied')
    db.session.commit()


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
                "id": {"type": "string", "maxLength": 32},
                "description": {"type": "string", "maxLength": 200},
                "comment": {"type": "string", "maxLength": 200},
                "allowed": {"type": "boolean"},
                "merged": {"type": "boolean"},
                "merge_q": {"type": "string", "maxLength": 32},
                "merging_label": {"type": "boolean"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                },
                "self_answers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "maxLength": 32},
                            "allowed": {"type": "boolean", "default": False},
                            "comment": {"type": "string", "maxLength": 200},
                            "type": {"enum": [elem.type_name for elem in CAnswerType.query.all()]},
                            "content": {"type": "string", "maxLength": 200},
                            "summary": {"type": "string", "maxLength": 200},
                            "author_id": {"type": "string", "maxLength": 32},
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
                            "id": {"type": "string", "maxLength": 32},
                            "level": {
                                "enum": [level.level for level in CAnswerLevel.query.all()]}
                        },
                        "required": ["id", "level"]
                    },
                    "uniqueItems": True
                }
            },
            "required": ["id", "comment", "allowed",
                         "merged", "merge_q", "merging_label",
                         "self_answers", "adjusted_answers"]
        }
        try:
            validate(req_body, handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}" \
                .format(".".join([str(i) for i in e.path]), e.message)
            return msg, 500
    else:
        return "请求体必须是JSON格式", 500

    if ERequest.query.get(req_body['id']) is None:
        return "该新增问题请求不存在", 500
    if ERequest.query.get(req_body['id']).reviewer_id != user_id:
        return "并不属于该审核员的请求.", 500
    if req_body['allowed'] and req_body['merged'] \
            and EQuestion.query.get(req_body['merge_q']) is None:
        return "待合并的标准问题不存在", 500
    # every question must have only one std answer.
    if req_body['allowed']:
        if not req_body['merged']:
            if sum([(1 if self_ans['level'] == CAnswerLevel.query.get(__answer_level_id('STD')) else 0)
                    for self_ans in req_body['self_answers']]) > 1:
                return "只能有一个回答级别为标准回答", 500
        else:
            adjusted: dict = {elem['id']: elem['level'] for elem in req_body['adjusted_answers']}
            n_std: int = 0
            for e_ans in EAnswer.query.filter_by(question_id=req_body['id']):
                level = e_ans.level if e_ans.id not in adjusted \
                    else adjusted.get(e_ans.id)
                n_std += 1 if level == __answer_level_id('STD') else 0
                if n_std > 1:
                    return "只能有一个标准回答", 500
    return "", 200


@bp.route('/answer-requests/<user_id>', methods=['POST'])
def handle_answer_requests(user_id):
    req_body = request.get_json()
    msg, status = arg_check(user_id, req_body)
    if status != 200:
        return make_response(jsonify(status=status, msg=msg), status)
    answer_persistence(req_body)
    # todo: if add answer search in the future, sync es here.
    # sync_es()
    return make_response(jsonify(status=200, msg='acknowledged'))


def answer_persistence(req_body):
    e_answer = EAnswer.query.get(req_body['id'])
    summary = req_body['summary'] if 'summary' in req_body else e_answer.summary
    content = req_body['content'] if 'content' in req_body else e_answer.content
    q_id = req_body['qid'] if 'qid' in req_body else e_answer.question_id
    type_id = CAnswerType.query.filter_by(type_name=req_body['type']).first().id \
        if 'type' in req_body else e_answer.type_id
    level_id = CAnswerLevel.query.filter_by(level=req_body['level']).first().id
    upd_ans = EAnswer.query.get(req_body['id'])
    upd_ans.question_id = q_id
    upd_ans.type_id = type_id
    upd_ans.summary = summary
    upd_ans.content = content
    upd_ans.level_id = level_id
    upd_ans.comment = req_body['comment']
    db.session.commit()
    for adjusted in req_body['adjusted_answers']:
        ad_level_id = CAnswerLevel.query.filter_by(level=adjusted['level']).first().id
        EAnswer.query.get(adjusted['id']).level_id = ad_level_id
    db.session.commit()


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
            "required": ["id", "level", "comment", "adjusted_answers"],
            "properties": {
                "id": {"maxLength": 32, "type": "string"},
                "q_id": {"maxLength": 32, "type": "string"},
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
                            "id": {"maxLength": 32, "type": "string"},
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
            or EAnswer.query.get(req_body['id']).level_id != __answer_level_id('undetermined'):
        return "该待审核解答不存在", 500
    adjusted = {elem['id']: elem['level'] for elem in req_body['adjusted_answers']}

    n_std = 1 if req_body['level'] == 'std' else 0
    for ans in EAnswer.query.filter_by(question_id=req_body['id']):
        level = adjusted[ans.id] if ans.id in adjusted else ans.level.level
        n_std += 1 if level == CAnswerLevel.query.get(__answer_level_id('std')) else 0
        if n_std > 1:
            return "只能有一个标准回答", 500
    if 'q_id' in req_body and EQuestion.query.get(req_body['q_id']) is None:
        return "问题不存在", 500
    return "", 200
