from flask import Blueprint, render_template, session
from database.db import get_db
from routes.auth import login_required
from services.progress_service import get_user_dashboard_analytics

bp = Blueprint('progress', __name__, url_prefix='/progress')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    analytics = get_user_dashboard_analytics(user_id)
    return render_template('progress.html', analytics=analytics)
