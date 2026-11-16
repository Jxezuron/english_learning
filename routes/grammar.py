import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.quiz_service import evaluate_lesson_quiz

bp = Blueprint('grammar', __name__, url_prefix='/grammar')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    db = get_db()
    
    category_filter = request.args.get('category', '').strip()
    cefr_filter = request.args.get('level', '').strip()
    
    query = """
        SELECT gl.*,
               (SELECT COUNT(*) FROM grammar_quizzes gq WHERE gq.lesson_id = gl.id) as quiz_count,
               (SELECT COUNT(DISTINCT qa.quiz_id) FROM quiz_attempts qa WHERE qa.lesson_id = gl.id AND qa.user_id = ? AND qa.is_correct = 1) as mastered_quizzes
        FROM grammar_lessons gl
        WHERE 1=1
    """
    params = [user_id]
    
    if category_filter:
        query += " AND gl.category = ?"
        params.append(category_filter)
    if cefr_filter:
        query += " AND gl.cefr_level = ?"
        params.append(cefr_filter)
        
    query += " ORDER BY gl.order_index ASC"
    
    cur = db.execute(query, params)
    lessons = cur.fetchall()
    
    # Get distinct categories & CEFR levels
    cur2 = db.execute("SELECT DISTINCT category FROM grammar_lessons ORDER BY category")
    categories = [r['category'] for r in cur2.fetchall()]
    
    return render_template(
        'grammar.html',
        lessons=lessons,
        categories=categories,
        selected_category=category_filter,
        selected_level=cefr_filter
    )

@bp.route('/<slug>')
@login_required
def lesson_detail(slug):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT * FROM grammar_lessons WHERE slug = ?", (slug,))
    lesson = cur.fetchone()
    if not lesson:
        flash("Grammar lesson not found.", "warning")
        return redirect(url_for('grammar.index'))
        
    lesson_dict = dict(lesson)
    lesson_dict['examples'] = json.loads(lesson_dict['examples_json'] or '[]')
    lesson_dict['common_mistakes'] = json.loads(lesson_dict['common_mistakes_json'] or '[]')
    
    # Quizzes
    cur_q = db.execute("SELECT * FROM grammar_quizzes WHERE lesson_id = ? ORDER BY id ASC", (lesson['id'],))
    quizzes = []
    for q in cur_q.fetchall():
        q_dict = dict(q)
        q_dict['options'] = json.loads(q_dict['options_json'])
        quizzes.append(q_dict)
        
    # Past attempts
    cur_att = db.execute("""
        SELECT * FROM quiz_attempts 
        WHERE user_id = ? AND lesson_id = ? 
        ORDER BY created_at DESC LIMIT 5
    """, (user_id, lesson['id']))
    attempts = cur_att.fetchall()
    
    return render_template(
        'grammar_lesson.html',
        lesson=lesson_dict,
        quizzes=quizzes,
        attempts=attempts
    )

@bp.route('/<int:lesson_id>/quiz', methods=('POST',))
@login_required
def submit_quiz(lesson_id):
    user_id = session['user_id']
    
    # Handle both JSON API and form post
    if request.is_json:
        answers = request.get_json()
    else:
        answers = {}
        for k, v in request.form.items():
            if k.startswith('q_'):
                answers[k.replace('q_', '')] = v
                
    result = evaluate_lesson_quiz(user_id, lesson_id, answers)
    
    if request.is_json:
        return jsonify(result)
        
    flash(f"Quiz completed! You scored {result['correct']} / {result['total']} ({result['percentage']}%) and earned {result['xp_earned']} XP!", "success")
    
    db = get_db()
    cur = db.execute("SELECT slug FROM grammar_lessons WHERE id = ?", (lesson_id,))
    lesson = cur.fetchone()
    return redirect(url_for('grammar.lesson_detail', slug=lesson['slug']))
