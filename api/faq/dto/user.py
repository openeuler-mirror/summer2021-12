from dataclasses import dataclass

from faq.dto.review import UserField
from faq.models import EAnswer, EQuestion


@dataclass
class AnswerEntry:
    id: str
    level: str
    reviewer: UserField
    type: str
    content: str
    summary: str
    author: UserField

    def __init__(self, answer: EAnswer):
        self.id = answer.id
        self.reviewer = UserField(answer.reviewer)
        self.type = answer.type.type_name
        self.content = answer.content
        self.summary = answer.summary
        self.level = answer.level.level
        self.author = UserField(answer.author)


@dataclass
class QuestionEntry:
    id: str
    std_description: str
    descriptions: list
    tags: list
    answers: list

    def __init__(self, question: EQuestion):
        self.id = question.id
        self.std_description = question.std_description
        self.descriptions = [des.description for des in question.e_question_descriptions]
        self.tags = [tagging.tag.tag_name for tagging in question.r_question_taggings]
        self.answers = []


