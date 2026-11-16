from datetime import date, datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.progress_service import award_xp

bp = Blueprint('planner', __name__, url_prefix='/planner')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    db = get_db()
    
    # Load user's profile goals
    cur = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    
    # Current date & weekly calendar (Monday to Sunday)
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    
    week_days = []
    for i in range(7):
        current_day = start_of_week + timedelta(days=i)
        day_str = current_day.isoformat()
        
        # Fetch tasks for this day
        cur_t = db.execute("""
            SELECT * FROM study_planner 
            WHERE user_id = ? AND plan_date = ?
            ORDER BY is_completed ASC, id ASC
        """, (user_id, day_str))
        tasks = cur_t.fetchall()
        
        week_days.append({
            "date": day_str,
            "day_name": current_day.strftime("%A"),
            "date_formatted": current_day.strftime("%b %d"),
            "is_today": (current_day == today),
            "is_past": (current_day < today),
            "tasks": tasks
        })

    # Available grammar lessons & speaking topics for quick-schedule dropdown
    cur_g = db.execute("SELECT id, title FROM grammar_lessons ORDER BY order_index ASC")
    lessons = cur_g.fetchall()
    
    cur_s = db.execute("SELECT id, topic_number, title FROM speaking_topics ORDER BY topic_number ASC")
    topics = cur_s.fetchall()
    
    return render_template(
        'planner.html',
        user=user,
        week_days=week_days,
        today_str=today.isoformat(),
        lessons=lessons,
        topics=topics
    )

@bp.route('/add', methods=('POST',))
@login_required
def add_task():
    user_id = session['user_id']
    db = get_db()
    
    plan_date = request.form.get('plan_date', date.today().isoformat())
    task_type = request.form.get('task_type', 'grammar')
    task_title = request.form.get('task_title', '').strip()
    target_id = request.form.get('target_id')
    
    if not task_title:
        flash("Please provide a title for your study task.", "warning")
        return redirect(url_for('planner.index'))
        
    db.execute("""
        INSERT INTO study_planner (user_id, plan_date, task_type, task_title, target_id)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, plan_date, task_type, task_title, target_id if target_id and target_id.isdigit() else None))
    db.commit()
    
    flash("Study task scheduled on your planner calendar!", "success")
    return redirect(url_for('planner.index'))

@bp.route('/toggle/<int:task_id>', methods=('POST',))
@login_required
def toggle_task(task_id):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT is_completed FROM study_planner WHERE id = ? AND user_id = ?", (task_id, user_id))
    task = cur.fetchone()
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    new_state = 0 if task['is_completed'] == 1 else 1
    completed_time = datetime.now().isoformat() if new_state == 1 else None
    
    db.execute("""
        UPDATE study_planner 
        SET is_completed = ?, completed_at = ?
        WHERE id = ? AND user_id = ?
    """, (new_state, completed_time, task_id, user_id))
    
    if new_state == 1:
        award_xp(user_id, 15, "Completed Study Planner Task")
        
    db.commit()
    return jsonify({"status": "success", "is_completed": new_state})

@bp.route('/update-goals', methods=('POST',))
@login_required
def update_goals():
    user_id = session['user_id']
    db = get_db()
    
    daily_mins = int(request.form.get('daily_goal_minutes', 20))
    daily_words = int(request.form.get('daily_goal_words', 10))
    daily_lessons = int(request.form.get('daily_goal_lessons', 1))
    daily_speaking = int(request.form.get('daily_goal_speaking', 1))
    
    db.execute("""
        UPDATE users 
        SET daily_goal_minutes = ?, daily_goal_words = ?, daily_goal_lessons = ?, daily_goal_speaking = ?
        WHERE id = ?
    """, (daily_mins, daily_words, daily_lessons, daily_speaking, user_id))
    db.commit()
    
    flash("Daily study targets updated!", "success")
    return redirect(url_for('planner.index'))
