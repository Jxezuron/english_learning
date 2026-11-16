import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.db import get_db
from routes.auth import login_required
from services.quiz_service import get_placement_questions, evaluate_placement_test

bp = Blueprint('placement', __name__, url_prefix='/placement')

@bp.route('', methods=('GET',))
@bp.route('/', methods=('GET',))
@login_required
def index():
    user_id = session['user_id']
    questions = get_placement_questions()
    
    db = get_db()
    cur = db.execute("SELECT * FROM placement_tests WHERE user_id = ? ORDER BY completed_at DESC LIMIT 1", (user_id,))
    previous_attempt = cur.fetchone()
    
    return render_template('placement.html', questions=questions, previous_attempt=previous_attempt)

@bp.route('/submit', methods=('POST',))
@login_required
def submit():
    user_id = session['user_id']
    answers = {}
    for key, value in request.form.items():
        if key.startswith('q_'):
            q_idx = key.replace('q_', '')
            answers[q_idx] = value
            
    result = evaluate_placement_test(user_id, answers)
    flash(f"Placement Assessment complete! Your estimated proficiency level is {result['level']}.", "success")
    return render_template('placement_result.html', result=result)

@bp.route('/history')
@login_required
def history():
    user_id = session['user_id']
    db = get_db()
    cur = db.execute("SELECT * FROM placement_tests WHERE user_id = ? ORDER BY completed_at DESC", (user_id,))
    attempts = cur.fetchall()
    
    formatted_attempts = []
    for att in attempts:
        row = dict(att)
        row['breakdown'] = json.loads(row['grammar_breakdown'])
        row['weak'] = json.loads(row['weak_topics'])
        row['strong'] = json.loads(row['strong_topics'])
        row['path'] = json.loads(row['recommended_path'])
        formatted_attempts.append(row)
        
    return render_template('placement_history.html', attempts=formatted_attempts)
