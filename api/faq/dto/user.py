from dataclasses import dataclass

from faq.content_handler import process_document
from faq.dto import Processable
from faq.dto.review import UserField
from faq.models import EAnswer, EQuestion


@dataclass
class AnswerEntry(Processable):
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

    def process(self):
        self.reviewer = self.reviewer.process()
        self.content = process_document(self.content)
        self.summary = process_document(self.summary)
        self.author = self.author.process()
        return self


@dataclass
class QuestionEntry(Processable):
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

    def process(self):
        self.std_description = process_document(self.std_description)
        self.descriptions = [des for des in self.descriptions]
        ans: AnswerEntry
        self.answers = [ans.process() for ans in self.answers]
        return self
