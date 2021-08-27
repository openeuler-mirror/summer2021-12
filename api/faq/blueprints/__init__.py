from flask import Blueprint

from faq.blueprints import review, show, user, log, form

bp = Blueprint('base', __name__)
bp.register_blueprint(review.bp)
bp.register_blueprint(show.bp)
bp.register_blueprint(user.bp)
bp.register_blueprint(log.bp)
bp.register_blueprint(form.bp)
