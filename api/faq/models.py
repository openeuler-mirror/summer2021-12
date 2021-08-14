# coding: utf-8
from faq import db


class CAnswerBrowseType(db.Model):
    __tablename__ = 'c_answer_browse_type'

    id = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String(100))


class CAnswerLevel(db.Model):
    __tablename__ = 'c_answer_level'

    id = db.Column(db.String(20), primary_key=True)
    level = db.Column(db.String(100), nullable=False)


class CAnswerType(db.Model):
    __tablename__ = 'c_answer_type'

    id = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String(100), nullable=False)


class CQuestionBrowseType(db.Model):
    __tablename__ = 'c_question_browse_type'

    id = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String(100))


class CReviewStatu(db.Model):
    __tablename__ = 'c_review_status'

    id = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String(100), nullable=False)


class CUserRole(db.Model):
    __tablename__ = 'c_user_role'

    id = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String(100), nullable=False)


class EAnswer(db.Model):
    __tablename__ = 'e_answer'

    id = db.Column(db.String(20), primary_key=True)
    type_id = db.Column(db.ForeignKey('c_answer_type.id'), index=True)
    content = db.Column(db.String(200))
    author_id = db.Column(db.ForeignKey('e_user.id'), index=True)
    question_id = db.Column(db.ForeignKey('e_question.id'), index=True)
    level_id = db.Column(db.ForeignKey('c_answer_level.id'), index=True)
    comment = db.Column(db.String(200))

    author = db.relationship('EUser', primaryjoin='EAnswer.author_id == EUser.id', backref='e_answers')
    level = db.relationship('CAnswerLevel', primaryjoin='EAnswer.level_id == CAnswerLevel.id', backref='e_answers')
    question = db.relationship('EQuestion', primaryjoin='EAnswer.question_id == EQuestion.id', backref='e_answers')
    type = db.relationship('CAnswerType', primaryjoin='EAnswer.type_id == CAnswerType.id', backref='e_answers')


class EAnswerBrowseLog(db.Model):
    __tablename__ = 'e_answer_browse_log'

    id = db.Column(db.String(20), primary_key=True)
    time = db.Column(db.DateTime)
    type_id = db.Column(db.ForeignKey('c_answer_browse_type.id'), index=True)
    answer_id = db.Column(db.ForeignKey('e_answer.id'), index=True)
    user_id = db.Column(db.ForeignKey('e_user.id'), index=True)

    answer = db.relationship('EAnswer', primaryjoin='EAnswerBrowseLog.answer_id == EAnswer.id',
                             backref='e_answer_browse_logs')
    type = db.relationship('CAnswerBrowseType', primaryjoin='EAnswerBrowseLog.type_id == CAnswerBrowseType.id',
                           backref='e_answer_browse_logs')
    user = db.relationship('EUser', primaryjoin='EAnswerBrowseLog.user_id == EUser.id', backref='e_answer_browse_logs')


class EQuestion(db.Model):
    __tablename__ = 'e_question'

    id = db.Column(db.String(20), primary_key=True)
    std_description = db.Column(db.String(250), unique=True)


class EQuestionDescription(db.Model):
    __tablename__ = 'e_question_description'

    id = db.Column(db.String(20), primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.ForeignKey('e_question.id'), index=True)

    question = db.relationship('EQuestion', primaryjoin='EQuestionDescription.question_id == EQuestion.id',
                               backref='e_question_descriptions')


class EQuestioningLog(db.Model):
    __tablename__ = 'e_questioning_log'

    id = db.Column(db.String(20), primary_key=True)
    type_id = db.Column(db.ForeignKey('c_question_browse_type.id'), index=True)
    op_time = db.Column(db.DateTime)
    matched_question_id = db.Column(db.ForeignKey('e_question.id'), index=True)
    user_id = db.Column(db.ForeignKey('e_user.id'), index=True)
    user_question = db.Column(db.String(100))

    matched_question = db.relationship('EQuestion', primaryjoin='EQuestioningLog.matched_question_id == EQuestion.id',
                                       backref='e_questioning_logs')
    type = db.relationship('CQuestionBrowseType', primaryjoin='EQuestioningLog.type_id == CQuestionBrowseType.id',
                           backref='e_questioning_logs')
    user = db.relationship('EUser', primaryjoin='EQuestioningLog.user_id == EUser.id', backref='e_questioning_logs')


class ERequest(db.Model):
    __tablename__ = 'e_request'

    id = db.Column(db.String(20), primary_key=True)
    description = db.Column(db.String(200))
    author_id = db.Column(db.ForeignKey('e_user.id'), index=True)
    time = db.Column(db.DateTime)
    review_status = db.Column(db.ForeignKey('c_review_status.id'), nullable=False, index=True)
    comment = db.Column(db.String(200))

    author = db.relationship('EUser', primaryjoin='ERequest.author_id == EUser.id', backref='e_requests')
    c_review_statu = db.relationship('CReviewStatu', primaryjoin='ERequest.review_status == CReviewStatu.id',
                                     backref='e_requests')


class ESelfAnswer(db.Model):
    __tablename__ = 'e_self_answer'

    id = db.Column(db.String(20), primary_key=True)
    type_id = db.Column(db.ForeignKey('c_answer_type.id'), index=True)
    content = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.ForeignKey('e_user.id'), index=True)
    request_id = db.Column(db.ForeignKey('e_request.id'), index=True)
    comment = db.Column(db.String(200))

    author = db.relationship('EUser', primaryjoin='ESelfAnswer.author_id == EUser.id', backref='e_self_answers')
    request = db.relationship('ERequest', primaryjoin='ESelfAnswer.request_id == ERequest.id', backref='e_self_answers')
    type = db.relationship('CAnswerType', primaryjoin='ESelfAnswer.type_id == CAnswerType.id', backref='e_self_answers')


class ETag(db.Model):
    __tablename__ = 'e_tag'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class EUser(db.Model):
    __tablename__ = 'e_user'

    id = db.Column(db.String(20), primary_key=True)
    gitee_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    avatar_url = db.Column(db.String(200))
    email = db.Column(db.String(200))
    role_id = db.Column(db.ForeignKey('c_user_role.id'), index=True)
    html_url = db.Column(db.String(200))

    role = db.relationship('CUserRole', primaryjoin='EUser.role_id == CUserRole.id', backref='e_users')


class RQuestionTagging(db.Model):
    __tablename__ = 'r_question_tagging'

    id = db.Column(db.String(20), primary_key=True)
    question_id = db.Column(db.ForeignKey('e_question.id'), index=True)
    tag_id = db.Column(db.ForeignKey('e_tag.id'), index=True)

    question = db.relationship('EQuestion', primaryjoin='RQuestionTagging.question_id == EQuestion.id',
                               backref='r_question_taggings')
    tag = db.relationship('ETag', primaryjoin='RQuestionTagging.tag_id == ETag.id', backref='r_question_taggings')


class RRequestTagging(db.Model):
    __tablename__ = 'r_request_tagging'

    id = db.Column(db.String(20), primary_key=True)
    tag_id = db.Column(db.ForeignKey('e_tag.id'), nullable=False, index=True)
    request_id = db.Column(db.ForeignKey('e_request.id'), nullable=False, index=True)

    request = db.relationship('ERequest', primaryjoin='RRequestTagging.request_id == ERequest.id',
                              backref='r_request_taggings')
    tag = db.relationship('ETag', primaryjoin='RRequestTagging.tag_id == ETag.id', backref='r_request_taggings')


class RRoleAttaching(db.Model):
    __tablename__ = 'r_role_attaching'

    id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.ForeignKey('e_user.id'), index=True)
    role_id = db.Column(db.ForeignKey('c_user_role.id'), index=True)

    role = db.relationship('CUserRole', primaryjoin='RRoleAttaching.role_id == CUserRole.id',
                           backref='r_role_attachings')
    user = db.relationship('EUser', primaryjoin='RRoleAttaching.user_id == EUser.id', backref='r_role_attachings')
