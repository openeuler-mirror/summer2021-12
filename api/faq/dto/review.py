from dataclasses import dataclass
from datetime import datetime

from faq.content_handler import process_document
from faq.dto import Processable
from faq.models import EUser, ESelfAnswer, ERequest, \
    RRequestTagging, EQuestion, EQuestionDescription, EAnswer


@dataclass
class UserField(Processable):
    id: str
    username: str
    avatar_url: str

    def __init__(self, author: EUser):
        self.id = author.id
        self.username = author.username
        self.avatar_url = author.avatar_url

    def process(self):
        self.username = process_document(self.username)
        return self


@dataclass
class SelfAnswerEntry(Processable):
    id: str
    type: str
    summary: str
    content: str

    def __init__(self, self_answer: ESelfAnswer):
        self.id = self_answer.id
        self.type = self_answer.type.type_name
        self.summary = self_answer.summary
        self.content = self_answer.content

    def process(self):
        self.summary = process_document(self.summary)
        self.content = process_document(self.content)
        return self


@dataclass
class RequestEntry(Processable):
    id: str
    q_description: str
    time: datetime
    author: UserField
    tags: list
    self_answers: list
    reviewer: UserField
    review_status: str

    def __init__(self, request: ERequest):
        self.id = request.id
        self.q_description = request.description
        self.time = request.time
        self.author = UserField(request.author)
        t: RRequestTagging
        self.tags = [t.tag.tag_name for t in request.r_request_taggings]
        self_answer: ESelfAnswer
        self.self_answers = [
            SelfAnswerEntry(self_answer)
            for self_answer in request.e_self_answers
        ]
        self.reviewer = UserField(request.reviewer)
        self.review_status = request.c_review_statu.type

    def process(self):
        self.q_description = process_document(self.q_description)
        self.author = self.author.process()
        self.tags = [process_document(t) for t in self.tags]
        self.self_answers = [
            self_answer.process()
            for self_answer in self.self_answers
        ]
        self.reviewer = self.reviewer.process()
        return self


@dataclass
class QuestionEntry(Processable):
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

    def process(self):
        self.std_description = process_document(self.std_description)
        self.descriptions = [process_document(des)
                             for des in self.descriptions]
        self.tags = [process_document(t) for t in self.tags]
        return self


@dataclass
class AnswerRequestEntry(Processable):
    id: str
    question: QuestionEntry
    type: str
    content: str
    summary: str
    author: UserField

    def __init__(self, answer: EAnswer) -> None:
        self.id = answer.id
        self.question = QuestionEntry(answer.question)
        self.type = answer.type.type_name
        self.content = answer.content
        self.summary = answer.summary
        self.author = UserField(answer.author)

    def process(self):
        self.question = self.question.process()
        self.content = process_document(self.content)
        self.summary = process_document(self.summary)
        self.author = self.author.process()


@dataclass
class AnswerEntry(Processable):
    id: str
    level: str
    reviewer: UserField
    question: QuestionEntry
    type: str
    content: str
    summary: str
    author: UserField

    def __init__(self, answer: EAnswer) -> None:
        self.id = answer.id
        self.reviewer = UserField(answer.reviewer)
        self.question = QuestionEntry(answer.question)
        self.type = answer.type.type_name
        self.content = answer.content
        self.summary = answer.summary
        self.level = answer.level.level
        self.author = UserField(answer.author)

    def process(self):
        self.reviewer = self.reviewer.process()
        self.question = self.question.process()
        self.content = process_document(self.content)
        self.summary = process_document(self.summary)
        self.author = self.author.process()
