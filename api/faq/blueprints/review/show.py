from flask import Blueprint, jsonify, current_app, request, make_response
from flask_sqlalchemy import Pagination

from faq.dto import ErrorBody
from faq.dto.review.show import RequestEntry, QuestionEntry, AnswerEntry, AnswerRequestEntry
from faq.models import ERequest, EQuestion, EAnswer, EUser, RRoleAttaching

bp = Blueprint('review_show', __name__, url_prefix='/review/show')


@bp.route('/requests/<user_id>', methods=['GET'])
def show_requests(user_id):
    page = int(request.args.get('page'))
    per_page = int(request.args.get('page_size'))

    current_app.logger.info("request user id: %s", user_id)

    # reviewer_id == 1 means it is waiting for reviewing.
    requests: Pagination = ERequest.query \
        .filter_by(reviewer_id=user_id) \
        .filter(ERequest.review_status == '1') \
        .order_by(ERequest.time.desc()) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False)
    body = [RequestEntry(rq) for rq in requests.items]
    return make_response(jsonify(body), 200)


@bp.route('/questions', methods=['GET'])
def show_questions():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('page_size'))

    questions = EQuestion.query \
        .order_by(EQuestion.std_description) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False) \
        .items
    q: EQuestion
    body = [QuestionEntry(q) for q in questions]
    return make_response(jsonify(body), 200)


@bp.route('/answers/<question_id>', methods=['GET'])
def get_answers(question_id):
    page = (request.args.get('page'))
    per_page = (request.args.get('page_size'))

    # level_id == '4' '5' means that
    # the answer is not denied and has been reviewed
    answers = EAnswer.query.filter(EAnswer.level_id not in ['4', '5']) \
        .filter_by(question_id=str(question_id)) \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False).items
    ans: EAnswer
    body = [AnswerEntry(ans) for ans in answers]
    return make_response(jsonify(body), 200)


@bp.route('/answer-requests/<user_id>', methods=['GET'])
def show_answer_requests(user_id=None):
    page = (request.args.get('page'))
    per_page = (request.args.get('page_size'))

    if user_id is None:
        return make_response(jsonify(ErrorBody(reason='未指定账户 id')), 500)
    if EUser.query.filter_by(id=user_id).first() is None:
        return make_response(jsonify(ErrorBody(reason='审查员的账户不存在')), 500)
    if RRoleAttaching.query.filter_by(user_id=user_id) \
            .filter(RRoleAttaching.role_id == '2').first() is None:  # '2' means reviewers
        return make_response(jsonify(ErrorBody(reason='该用户没有审查权限')), 500)

    ans_reqs = EAnswer.query \
        .filter_by(reviewer_id=user_id) \
        .filter(EAnswer.level_id == '4') \
        .paginate(page=int(page) if page else None,
                  per_page=int(per_page) if per_page else None,
                  error_out=False).items
    ans: EAnswer
    body = [AnswerRequestEntry(ans) for ans in ans_reqs]

    return make_response(jsonify(body), 500)
