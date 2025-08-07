"""
Admin Blueprint - Backend management interface
"""
from flask import Blueprint

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Import and register sub-blueprints
from .dashboard import dashboard_bp
from .parser_studio import parser_studio_bp

admin_bp.register_blueprint(dashboard_bp)
admin_bp.register_blueprint(parser_studio_bp)