from flask import Blueprint, request, make_response, jsonify

from faq.models import ETag, CAnswerLevel, CAnswerType, CReviewStatu

bp = Blueprint('form', __name__, url_prefix='/form')


@bp.route('/tags', methods=['GET'])
def tags():
    if 'like' in request.args:
        return make_response(
            jsonify(status=200, data=ETag.query.filter(
                ETag.tag_name.like("%{}%".format(request.args['like']))
            ).all()), 200
        )
    else:
        return make_response(jsonify(status=200, data=ETag.query.all()))


@bp.route('/enum/answer-level', methods=['GET'])
def enum_answer_level():
    return make_response(jsonify(status=200, data=CAnswerLevel.query.all()))


@bp.route('/enum/answer-type', methods=['GET'])
def enum_answer_type():
    return make_response(jsonify(status=200, data=CAnswerType.query.all()))


@bp.route('/enum/review-status', methods=['GET'])
def enum_review_status():
    return make_response(jsonify(status=200, data=CReviewStatu.query.all()))

