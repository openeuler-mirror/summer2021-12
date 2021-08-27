from flask import Blueprint, request, make_response, jsonify
from jsonschema import validate, ValidationError
from sqlalchemy.sql.functions import now

from faq import db
from faq.models import CAnswerBrowseType, EAnswerBrowseLog, CQuestionBrowseType, EQuestioningLog

bp = Blueprint('log', __name__, url_prefix='/log')


@bp.route('/answer-browsing', methods=['GET'])
def answer_browsing():
    if request.is_json:
        handle_request_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "type": "object",
            "required": [
                "user_id",
                "answer_id",
                "type"
            ],
            "properties": {
                "user_id": {
                    "maxLength": 32,
                    "type": "string"
                },
                "answer_id": {
                    "maxLength": 32,
                    "type": "string"
                },
                "type": {
                    "enum": [tt.type for tt in CAnswerBrowseType.query.all()],
                    "type": "string"
                }
            }
        }
        try:
            validate(request.get_json(), handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(".".join([str(i) for i in e.path]), e.message)
            return make_response(jsonify(msg=msg, status=500), 500)
    else:
        return make_response(jsonify(msg="请求体必须是JSON格式", status=500), 500)
    req_body = request.get_json()
    type_id = CAnswerBrowseType.query.filter_by(type=req_body['type'])
    db.session.add(EAnswerBrowseLog(user_id=req_body['user_id'],
                                    answer_id=req_body['answer_id'],
                                    type_id=type_id,
                                    time=now()))
    db.session.commit()
    return make_response(jsonify(status=200, msg='acknowledged'))


@bp.route('/questioning', methods=['GET'])
def questioning():
    if request.is_json:
        handle_request_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "type": "object",
            "required": [
                "user_q",
                "user_id",
                "matched_q_id",
                "type"
            ],
            "properties": {
                "user_q": {
                    "maxLength": 200,
                    "type": "string"
                },
                "user_id": {
                    "maxLength": 32,
                    "type": "string"
                },
                "matched_q_id": {
                    "maxLength": 32,
                    "type": "string"
                },
                "type": {
                    "enum": [],
                    "type": "string"
                }
            }
        }
        try:
            validate(request.get_json(), handle_request_schema)
        except ValidationError as e:
            msg = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(".".join([str(i) for i in e.path]), e.message)
            return make_response(jsonify(msg=msg, status=500), 500)
    else:
        return make_response(jsonify(msg="请求体必须是JSON格式", status=500), 500)
    req_body = request.get_json()
    type_id = CQuestionBrowseType.query.filter_by(type=req_body['type'])
    db.session.add(EQuestioningLog(user_question=req_body['user_q'],
                                   user_id=req_body['user_id'],
                                   matched_question_id=req_body['matched_q_id'],
                                   type_id=type_id,
                                   op_time=now()))
    db.session.commit()
    return make_response(jsonify(status=200, msg='acknowledged'))
