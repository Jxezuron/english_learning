from flask import Blueprint, render_template, request, jsonify, session
from database.db import get_db
from routes.auth import login_required
from services.progress_service import award_xp

bp = Blueprint('pronunciation', __name__, url_prefix='/pronunciation')

@bp.route('')
@bp.route('/')
@login_required
def index():
    db = get_db()
    difficulty = request.args.get('difficulty', '').strip()
    item_type = request.args.get('type', '').strip()
    
    query = "SELECT * FROM pronunciation_items WHERE 1=1"
    params = []
    
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)
    if item_type:
        query += " AND item_type = ?"
        params.append(item_type)
        
    query += " ORDER BY id ASC"
    cur = db.execute(query, params)
    items = cur.fetchall()
    
    return render_template('pronunciation.html', items=items, selected_difficulty=difficulty, selected_type=item_type)

@bp.route('/award-xp', methods=('POST',))
@login_required
def award_pronunciation_xp():
    user_id = session['user_id']
    data = request.get_json() or {}
    similarity = float(data.get('similarity', 0))
    target = data.get('target', 'Pronunciation Drill')
    
    xp = 10 if similarity >= 80 else 5
    award_xp(user_id, xp, f"Pronunciation Lab ({int(similarity)}% match)")
    return jsonify({"status": "success", "xp_earned": xp})
