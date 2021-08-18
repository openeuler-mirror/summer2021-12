from dataclasses import dataclass
from datetime import datetime

from faq.models import EUser, ESelfAnswer, ERequest, \
    RRequestTagging, EQuestion, EQuestionDescription, EAnswer


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
        self.type = self_answer.type.type
        self.summary = self_answer.summary
        self.content = self_answer.content


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
        t: RRequestTagging
        self.tags = [t.tag.tag_name for t in request.r_request_taggings]
        self_answer: ESelfAnswer
        self.self_answers = [
            SelfAnswerEntry(self_answer)
            for self_answer in request.e_self_answers
        ]


@dataclass
class QuestionEntry:
    id: str
    std_description: str
    descriptions: list
    tags: list

    def __init__(self, question: EQuestion) -> None:
        self.id = question.id
        self.std_description = question.std_description
        t: RRequestTagging
        self.tags = [t.tag.tag_name for t in question.r_question_taggings]
        des: EQuestionDescription
        self.descriptions = [des.description for des in question.e_question_descriptions]


@dataclass
class AnswerEntry:
    id: str
    q_id: str
    type: str
    content: str
    summary: str
    level: str

    def __init__(self, answer: EAnswer) -> None:
        self.id = answer.id
        self.q_id = answer.question_id
        self.type = answer.type.type_name
        self.content = answer.content
        self.summary = answer.summary
        self.level = answer.level.level




@dataclass
class AnswerRequestEntry:
    id: str
    question: QuestionEntry
    type: str
    content: str
    summary: str
    author: AuthorField

    def __init__(self, answer: EAnswer) -> None:
        self.id = answer.id
        self.question = QuestionEntry(answer.question)
        self.type = answer.type.type_name
        self.content = answer.content
        self.summary = answer.summary
        self.author = AuthorField(answer.author)


