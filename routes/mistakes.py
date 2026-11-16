from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.tutor_service import generate_practice_question_for_mistake
from services.progress_service import award_xp

bp = Blueprint('mistakes', __name__, url_prefix='/mistakes')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    db = get_db()
    
    category_filter = request.args.get('category', '').strip()
    status_filter = request.args.get('status', 'all').strip()  # 'unresolved', 'understood', 'all'
    
    query = "SELECT * FROM mistake_notebook WHERE user_id = ?"
    params = [user_id]
    
    if category_filter:
        query += " AND grammar_category = ?"
        params.append(category_filter)
        
    if status_filter == 'unresolved':
        query += " AND is_understood = 0"
    elif status_filter == 'understood':
        query += " AND is_understood = 1"
        
    query += " ORDER BY is_understood ASC, created_at DESC"
    cur = db.execute(query, params)
    mistakes = cur.fetchall()
    
    # Get distinct grammar categories
    cur_cat = db.execute("SELECT DISTINCT grammar_category FROM mistake_notebook WHERE user_id = ? ORDER BY grammar_category", (user_id,))
    categories = [r['grammar_category'] for r in cur_cat.fetchall()]
    
    # Total counts
    cur_count = db.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN is_understood = 0 THEN 1 ELSE 0 END) as unresolved,
            SUM(CASE WHEN is_understood = 1 THEN 1 ELSE 0 END) as understood
        FROM mistake_notebook WHERE user_id = ?
    """, (user_id,))
    counts = dict(cur_count.fetchone())
    
    return render_template(
        'mistakes.html',
        mistakes=mistakes,
        categories=categories,
        counts=counts,
        selected_category=category_filter,
        selected_status=status_filter
    )

@bp.route('/<int:mistake_id>/understood', methods=('POST',))
@login_required
def toggle_understood(mistake_id):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT is_understood FROM mistake_notebook WHERE id = ? AND user_id = ?", (mistake_id, user_id))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Mistake record not found"}), 404
        
    new_val = 0 if row['is_understood'] == 1 else 1
    db.execute("UPDATE mistake_notebook SET is_understood = ? WHERE id = ? AND user_id = ?", (new_val, mistake_id, user_id))
    
    if new_val == 1:
        award_xp(user_id, 10, "Mastered Mistake Item in Notebook")
        
    db.commit()
    return jsonify({"status": "success", "is_understood": new_val})

@bp.route('/<int:mistake_id>/retry', methods=('POST',))
@login_required
def retry_question(mistake_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    selected = str(data.get('answer', '')).strip()
    
    db = get_db()
    cur = db.execute("SELECT * FROM mistake_notebook WHERE id = ? AND user_id = ?", (mistake_id, user_id))
    m = cur.fetchone()
    if not m:
        return jsonify({"error": "Record not found"}), 404
        
    is_correct = (selected.lower() == m['correct_answer'].lower())
    
    if is_correct:
        db.execute("""
            UPDATE mistake_notebook 
            SET is_understood = 1, retry_count = retry_count + 1 
            WHERE id = ? AND user_id = ?
        """, (mistake_id, user_id))
        award_xp(user_id, 15, f"Retried and Corrected Mistake ({m['grammar_category']})")
        db.commit()
        return jsonify({"is_correct": True, "message": "Excellent work! You answered correctly and marked this error as understood."})
    else:
        db.execute("UPDATE mistake_notebook SET retry_count = retry_count + 1 WHERE id = ? AND user_id = ?", (mistake_id, user_id))
        db.commit()
        return jsonify({
            "is_correct": False,
            "message": f"Not quite. Remember: {m['explanation']}"
        })

@bp.route('/practice-similar/<int:mistake_id>')
@login_required
def practice_similar(mistake_id):
    user_id = session['user_id']
    db = get_db()
    cur = db.execute("SELECT grammar_category FROM mistake_notebook WHERE id = ? AND user_id = ?", (mistake_id, user_id))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
        
    drill = generate_practice_question_for_mistake(row['grammar_category'])
    return jsonify(drill)
