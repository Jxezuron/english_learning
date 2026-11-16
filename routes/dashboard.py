from flask import Blueprint, render_template, redirect, url_for, g, session
from database.db import get_db
from routes.auth import login_required
from services.progress_service import get_user_dashboard_analytics, update_study_streak

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def landing():
    if g.user:
        return redirect(url_for('dashboard.index'))
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def index():
    user_id = session['user_id']
    update_study_streak(user_id)
    analytics = get_user_dashboard_analytics(user_id)
    
    db = get_db()
    # Check if placement test has been taken
    cur = db.execute("SELECT * FROM placement_tests WHERE user_id = ? ORDER BY completed_at DESC LIMIT 1", (user_id,))
    latest_placement = cur.fetchone()
    
    # Check mistakes count
    cur = db.execute("SELECT COUNT(*) as count FROM mistake_notebook WHERE user_id = ? AND is_understood = 0", (user_id,))
    unresolved_mistakes = cur.fetchone()['count']
    
    # Check today's study planner tasks
    from datetime import date
    today_str = date.today().isoformat()
    cur = db.execute("SELECT * FROM study_planner WHERE user_id = ? AND plan_date = ? ORDER BY is_completed ASC, id ASC", (user_id, today_str))
    planner_tasks = cur.fetchall()
    
    # Calculate daily goals progress
    # 1. Vocab reviewed today
    cur = db.execute("""
        SELECT COUNT(*) as count FROM user_vocabulary 
        WHERE user_id = ? AND last_reviewed_date = ?
    """, (user_id, today_str))
    vocab_done_today = cur.fetchone()['count']
    
    # 2. Quizzes done today
    cur = db.execute("""
        SELECT COUNT(DISTINCT lesson_id) as count FROM quiz_attempts
        WHERE user_id = ? AND DATE(created_at) = ?
    """, (user_id, today_str))
    lessons_done_today = cur.fetchone()['count']
    
    # 3. Speaking done today
    cur = db.execute("""
        SELECT COUNT(*) as count FROM speaking_submissions
        WHERE user_id = ? AND DATE(created_at) = ?
    """, (user_id, today_str))
    speaking_done_today = cur.fetchone()['count']
    
    daily_goals = {
        "words_target": analytics['user']['daily_goal_words'],
        "words_actual": vocab_done_today,
        "words_pct": min(100, int((vocab_done_today / max(1, analytics['user']['daily_goal_words'])) * 100)),
        
        "lessons_target": analytics['user']['daily_goal_lessons'],
        "lessons_actual": lessons_done_today,
        "lessons_pct": min(100, int((lessons_done_today / max(1, analytics['user']['daily_goal_lessons'])) * 100)),
        
        "speaking_target": analytics['user']['daily_goal_speaking'],
        "speaking_actual": speaking_done_today,
        "speaking_pct": min(100, int((speaking_done_today / max(1, analytics['user']['daily_goal_speaking'])) * 100))
    }
    
    return render_template(
        'dashboard.html',
        analytics=analytics,
        latest_placement=latest_placement,
        unresolved_mistakes=unresolved_mistakes,
        planner_tasks=planner_tasks,
        daily_goals=daily_goals
    )
