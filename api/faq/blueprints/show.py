from flask import Blueprint, request, current_app, make_response, jsonify
from flask_sqlalchemy import Pagination

from faq.dto import ErrorBody
from faq.dto.review import RequestEntry, QuestionEntry, AnswerEntry, AnswerRequestEntry
from faq.models import EQuestion, ERequest, EAnswer, EUser, RRoleAttaching, CReviewStatu, CAnswerLevel

bp = Blueprint('show', __name__, url_prefix='/show')

REVIEWER_ROLE_ID = '2'


def __review_status_id(name: str) -> str:
    name = name.lower()
    _id = CReviewStatu.query.filter_by(type=name).first().id
    return _id


def __answer_level_id(name: str) -> str:
    name = name.lower()
    return CAnswerLevel.query.filter_by(level=name).first().id


@bp.route('/requests-to-review/<reviewer_id>', methods=['GET'])
def requests_to_review(reviewer_id):
    page = int(request.args.get('page'))
    per_page = int(request.args.get('page_size'))
    _processed = ("doc_processed" in request.args
                  and request.args.get("doc_processed").lower() != 'false')

    current_app.logger.info("request user id: %s", reviewer_id)

    # reviewer_id == 1 means it is waiting for reviewing.
    requests: Pagination = ERequest.query \
        .filter_by(reviewer_id=reviewer_id) \
        .filter_by(review_status=__review_status_id('waiting')) \
        .order_by(ERequest.time.desc()) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False)
    body = [RequestEntry(rq).process() if _processed
            else RequestEntry(rq)
            for rq in requests.items]
    return make_response(jsonify(body=body, status=200), 200)


@bp.route('/questions', methods=['GET'])
def questions():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('page_size'))
    _processed = ("doc_processed" in request.args
                  and request.args.get("doc_processed").lower() != 'false')

    qs = EQuestion.query \
        .order_by(EQuestion.std_description) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False).items
    q: EQuestion
    body = [QuestionEntry(q).process() if _processed
            else QuestionEntry(q) for q in qs]
    return make_response(jsonify(body), 200)


@bp.route('/answers-of-q/<question_id>', methods=['GET'])
def answers_of_q(question_id):
    page = (request.args.get('page'))
    per_page = (request.args.get('page_size'))
    _processed = ("doc_processed" in request.args
                  and request.args.get("doc_processed").lower() != 'false')

    answers = EAnswer.query \
        .filter_by(question_id=str(question_id)) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False).items
    ans: EAnswer
    body = [AnswerEntry(ans).process() if _processed else AnswerEntry(ans) for ans in answers]
    return make_response(jsonify(body), 200)


@bp.route('/answer-requests-to-review/<reviewer_id>', methods=['GET'])
def show_answer_requests(reviewer_id):
    page = (request.args.get('page'))
    per_page = (request.args.get('page_size'))
    _processed = ("doc_processed" in request.args
                  and request.args.get("doc_processed").lower() != 'false')

    if EUser.query.filter_by(id=reviewer_id).first() is None:
        return make_response(jsonify(ErrorBody(reason='审查员的账户不存在')), 500)
    if RRoleAttaching.query.filter_by(user_id=reviewer_id) \
            .filter(RRoleAttaching.role_id == REVIEWER_ROLE_ID).first() is None:
        return make_response(jsonify(ErrorBody(reason='该用户没有审查权限')), 500)

    ans_reqs = EAnswer.query \
        .filter_by(reviewer_id=reviewer_id) \
        .filter(EAnswer.level_id == __answer_level_id('undetermined')) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False).items
    ans: EAnswer
    body = [AnswerRequestEntry(ans).process() if _processed
            else AnswerRequestEntry(ans)
            for ans in ans_reqs]

    return make_response(jsonify(body), 200)


@bp.route('/my-answers/<author_id>', methods=['GET'])
def my_answers(author_id):
    page = (request.args.get('page'))
    per_page = (request.args.get('page_size'))
    show_withdrawn = request.args.get('show_withdrawn')
    page = int(page) if page else None
    per_page = int(per_page) if per_page else None
    show_withdrawn = bool(show_withdrawn and show_withdrawn.lower() == 'true')
    _processed = ("doc_processed" in request.args
                  and request.args.get("doc_processed").lower() != 'false')

    if EUser.query.filter_by(id=author_id).first() is None:
        return make_response(jsonify(status=500, msg="用户不存在"), 500)

    answers = EAnswer.query \
        .filter_by(author_id=author_id) \
        .paginate(page=page, per_page=per_page, error_out=False).items

    return jsonify(status=200, body=[AnswerEntry(ans).process() if _processed
                                     else AnswerEntry(ans) for ans in answers])


@bp.route('/my-request/<author_id>', methods=['GET'])
def my_request(author_id):
    page = (request.args.get('page'))
    per_page = (request.args.get('page_size'))
    page = int(page) if page else None
    per_page = int(per_page) if per_page else None
    _processed = ("doc_processed" in request.args
                  and request.args.get("doc_processed").lower() != 'false')

    if EUser.query.filter_by(id=author_id).first() is None:
        return make_response(jsonify(status=500, msg="用户不存在"), 500)

    requests = ERequest.query \
        .filter_by(author_id=author_id) \
        .filter(ERequest.review_status != __review_status_id('withdrawn')) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(status=200, body=[RequestEntry(rq).process() if _processed
                                     else RequestEntry(rq) for rq in requests])
