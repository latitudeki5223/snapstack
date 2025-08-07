"""
Parser Studio Blueprint - Interactive parser testing
"""
from flask import Blueprint

parser_studio_bp = Blueprint('parser_studio', __name__, url_prefix='/parser')

from . import views