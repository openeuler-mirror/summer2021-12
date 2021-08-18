from flask import Blueprint

from faq.blueprints.review import show, handle

bp = Blueprint('review', __name__)

# bp.register_blueprint(show.bp)
bp.register_blueprint(handle.bp)
