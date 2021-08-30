import random
from datetime import datetime

from flask import Blueprint, jsonify, request, make_response
from jsonschema import validate, ValidationError
from sqlalchemy.sql.functions import now

from faq import db
from faq.dto.user import QuestionEntry, AnswerEntry
from faq.es_handler import init_es
from faq.models import EQuestion, CAnswerLevel, ETag, CAnswerType, EUser, ERequest, CReviewStatu, RRequestTagging, \
    ESelfAnswer, EAnswer, RRoleAttaching, CUserRole
from faq.smtp_handler import send, parse_request, parse_answer_request

bp = Blueprint('user', __name__, url_prefix='/user')


def __review_status_id(name: str) -> str:
    name = name.lower()
    return CReviewStatu.query.filter_by(type=name).first().id


def __answer_level_id(name: str) -> str:
    name = name.lower()
    return CAnswerLevel.query.filter_by(level=name).first().id


@bp.route('/questioning', methods=['GET'])
def questioning():
    answered_only: bool = 'answered_only' in request.args
    answer_level: str = request.args.get('answer_level') \
        if 'answer_level' in request.args else 'std'
    top_k = int(request.args.get('top_k')) \
        if 'top_k' in request.args \
           and request.args.get('top_k').isdigit() else 1

    if request.args.get('q') is None:
        return make_response(jsonify(status=500, msg="param 'q' is required."), 500)
    else:
        with init_es() as es:
            res = es.search(index='question', body={
                "query": {
                    "multi_match": {
                        "query": request.args.get('q'),
                        "fields": ['description', 'labels']
                    }
                }
            })['hits']['hits']
    q_ids = list(set(r['_source']['qid'] for r in res))
    body = []
    for qid in q_ids:
        if len(body) > top_k:
            break
        question = EQuestion.query.get(qid)
        entry = QuestionEntry(question)
        entry.answers = []
        for ans in question.e_answers:
            if int(ans.level_id) <= int(__answer_level_id(answer_level)):
                entry.answers.append(AnswerEntry(ans))
        if len(entry.answers) != 0 or not answered_only:
            body.append(entry)

    return make_response(jsonify(body), 200)


@bp.route('/request', methods=['POST'])
def propose_request():
    if request.is_json:
        handle_request_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "type": "object",
            "required": ["author_id", "description", "tags", "answers"],
            "properties": {
                "author_id": {"maximum": 20, "type": "string"},
                "description": {"maxLength": 200, "type": "string"},
                "tags": {
                    "type": "array", "uniqueItems": True,
                    "items": {"type": "string"}
                },
                "answers": {
                    "type": "array", "uniqueItems": True,
                    "items": {
                        "type": "object",
                        "required": ["type", "summary", "content"],
                        "properties": {
                            "type": {"uniqueItems": True, "enum": [t.type_name for t in CAnswerType.query.all()],
                                     "type": "string"},
                            "summary": {"maxLength": 200, "type": "string"},
                            "content": {"maxLength": 200, "type": "string"}
                        }
                    }
                }
            }
        }
        try:
            validate(request.get_json(), handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(".".join([str(i) for i in e.path]), e.message)
            return make_response(jsonify(status=500, msg=msg), 500)
    else:
        return make_response(jsonify(msg="请求体必须是JSON格式", status=500), 500)

    req_body = request.get_json()
    if EUser.query.get(req_body['author_id']) is None:
        return make_response(jsonify(status=500, msg="用户不存在"), 500)

    reviewer_id = dispatch_request(req_body['tags'], req_body['description'], now())

    new_request = request_persistence(req_body, reviewer_id)
    send(EUser.query.get(reviewer_id).email, parse_request(new_request))
    return jsonify(stauts=200, msg="acknowledged")


def request_persistence(req_body, reviewer_id):
    for tag_name in req_body['tags']:
        if ETag.query.filter_by(tag_name=tag_name).first() is None:
            db.session.add(ETag(tag_name=tag_name))
    db.session.commit()
    new_request = ERequest(author_id=req_body['author_id'],
                           description=req_body['description'],
                           reviewer_id=reviewer_id,
                           time=now(),
                           review_status=__review_status_id('waiting'))
    db.session.add(new_request)
    db.session.commit()
    for tag_name in req_body['tags']:
        tag_id = ETag.query.filter_by(tag_name=tag_name).first().id
        db.session.add(RRequestTagging(request_id=new_request.id, tag_id=tag_id))

    for ans_entry in req_body['answers']:
        type_id = CAnswerType.query.filter_by(type_name=ans_entry['type']).first().id
        db.session.add(ESelfAnswer(review_status=__review_status_id('waiting'),
                                   request_id=new_request.id,
                                   content=ans_entry['content'],
                                   summary=ans_entry['summary'],
                                   type_id=type_id))
    db.session.commit()
    return new_request


def dispatch_request(tags: list, description: str, time: datetime) -> str:
    return random.choice(
        list(set(
            attachment.user_id for attachment
            in RRoleAttaching.query.filter_by(
                role_id=CUserRole.query.filter_by(type='reviewer').first().id
            )
        ))
    )


@bp.route('/answer-request', methods=['POST'])
def propose_answer_request():
    if request.is_json:
        handle_request_schema = {
            "$schema": "http://json-schema.org/draft-07/schema", "type": "object",
            "required": ["author_id", "q_id", "type", "content", "summary"],
            "properties": {
                "author_id": {"maxLength": 32, "type": "string"},
                "q_id": {"maxLength": 32, "type": "string"},
                "type": {"enum": [t.type_name for t in CAnswerType.query.all()], "type": "string"},
                "content": {"maxLength": 200, "type": "string"},
                "summary": {"maxLength": 200, "type": "string"}
            }
        }
        try:
            validate(request.get_json(), handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(".".join([str(i) for i in e.path]), e.message)
            return make_response(jsonify(status=500, msg=msg), 500)
    else:
        return make_response(jsonify(msg="请求体必须是JSON格式", status=500), 500)
    req_body = request.get_json()
    if EUser.query.filter_by(id=req_body['author_id']).first() is None:
        return make_response(jsonify(status=200, msg="用户不存在：{}".format(req_body['author_id'])), 500)
    if EQuestion.query.filter_by(id=req_body['q_id']).first() is None:
        return make_response(jsonify(status=200, msg="问题不存在：{}".format(req_body['q_id'])), 500)

    reviewer_id = dispatch_answer(req_body['q_id'], req_body['author_id'],
                                  req_body['content'], req_body['summary'],
                                  CAnswerType.query.filter_by(type_name=req_body['type']))
    new_answer = answer_persistence(req_body, reviewer_id)
    send(EUser.query.get(reviewer_id).email, parse_answer_request(new_answer))
    return jsonify(stauts=200, msg="acknowledged")


def answer_persistence(req_body, reviewer_id):
    type_id = CAnswerType.query.filter_by(type_name=req_body['type']).first().id
    new_answer = EAnswer(reviewer_id=reviewer_id,
                         level_id=__answer_level_id('undetermined'),
                         question_id=req_body['q_id'],
                         author_id=req_body['author_id'],
                         content=req_body['content'],
                         summary=req_body['summary'],
                         type_id=type_id)
    db.session.add(new_answer)
    db.session.commit()
    return new_answer


def dispatch_answer(q_id, author_id, content, summary, type_id):
    return random.choice(
        list(set(
            attachment.user_id for attachment
            in RRoleAttaching.query.filter_by(
                role_id=CUserRole.query.filter_by(type='reviewer').first().id
            )
        ))
    )
