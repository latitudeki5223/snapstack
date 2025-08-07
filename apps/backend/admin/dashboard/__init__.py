"""
Dashboard Blueprint - Main admin dashboard
"""
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from . import views