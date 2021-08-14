from datetime import datetime

from flask import Blueprint, jsonify, current_app
from faq.models import (
    ERequest, EUser, ETag, ESelfAnswer
)
from dataclasses import dataclass

bp = Blueprint('review', __name__, url_prefix='/review')


@dataclass
class AuthorField:
    id: str
    username: str
    avatar_url: str

    def __init__(self, author: EUser):
        self.id = author.id
        self.username = author.username
        self.avatar_url = author.avatar_url


@dataclass
class SelfAnswerEntry:
    id: str
    type: str
    summary: str
    content: str

    def __init__(self, self_answer: ESelfAnswer):
        self.id = self_answer.id
        self.type = sel


@dataclass
class RequestEntry:
    id: str
    q_description: str
    time: datetime
    author: AuthorField
    tags: list
    self_answers: list

    def __init__(self, request: ERequest):
        self.id = request.id
        self.q_description = request.description
        self.time = request.time
        self.author = AuthorField(request.author)
        t: ETag
        self.tags = [t.name for t in request.r_request_taggings]

        self.self_answers = []


@bp.route('/<user_id>/show/requests', methods=['GET'])
def show_requests(user_id):
    current_app.logger.info("request user id: %s", user_id)

    res = []
    requests = ERequest.query.all()
    for rq in requests:
        entry = RequestEntry()
    return jsonify(requests)
