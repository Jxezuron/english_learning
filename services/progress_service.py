import json
from datetime import datetime, date, timedelta
from database.db import get_db

def award_xp(user_id, amount, reason="Study Activity"):
    """Adds XP to the user and logs learning activity."""
    if amount <= 0:
        return
    db = get_db()
    today_str = date.today().isoformat()
    
    # Update user XP
    db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (amount, user_id))
    
    # Log session
    db.execute("""
        INSERT INTO learning_logs (user_id, activity_type, duration_seconds, xp_earned, notes, log_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, reason, 60, amount, reason, today_str))
    
    db.commit()
    update_study_streak(user_id)
    check_and_unlock_achievements(user_id)

def update_study_streak(user_id):
    """Maintains consecutive daily study streaks."""
    db = get_db()
    cur = db.execute("SELECT streak_days, last_active_date FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        return
        
    today = date.today()
    today_str = today.isoformat()
    last_active_str = user['last_active_date']
    streak = user['streak_days'] or 0
    
    if not last_active_str:
        streak = 1
    else:
        try:
            last_date = date.fromisoformat(last_active_str)
            delta = (today - last_date).days
            if delta == 0:
                # Already active today
                pass
            elif delta == 1:
                # Active yesterday, streak continues!
                streak += 1
            else:
                # Missed a day, streak resets
                streak = 1
        except Exception:
            streak = 1
            
    db.execute("UPDATE users SET streak_days = ?, last_active_date = ? WHERE id = ?", (streak, today_str, user_id))
    db.commit()

def check_and_unlock_achievements(user_id):
    """
    Evaluates all system achievements against the user's progress
    and unlocks new badges.
    """
    db = get_db()
    # 1. Fetch user counts
    cur = db.execute("SELECT xp, streak_days FROM users WHERE id = ?", (user_id,))
    user_row = cur.fetchone()
    if not user_row:
        return []
        
    streak = user_row['streak_days'] or 0
    
    # Grammar lessons completed
    cur = db.execute("""
        SELECT COUNT(DISTINCT lesson_id) as count 
        FROM quiz_attempts 
        WHERE user_id = ? AND is_correct = 1
    """, (user_id,))
    grammar_completed = cur.fetchone()['count']
    
    # Vocabulary reviewed count
    cur = db.execute("""
        SELECT COUNT(*) as count 
        FROM user_vocabulary 
        WHERE user_id = ? AND repetition_count > 0
    """, (user_id,))
    vocab_reviewed = cur.fetchone()['count']
    
    # Speaking topics completed
    cur = db.execute("""
        SELECT COUNT(DISTINCT topic_id) as count 
        FROM speaking_submissions 
        WHERE user_id = ?
    """, (user_id,))
    speaking_topics_completed = cur.fetchone()['count']
    
    # Speaking submissions total
    cur = db.execute("""
        SELECT COUNT(*) as count 
        FROM speaking_submissions 
        WHERE user_id = ?
    """, (user_id,))
    speaking_submissions_total = cur.fetchone()['count']
    
    # Listening completed
    cur = db.execute("""
        SELECT COUNT(DISTINCT exercise_id) as count 
        FROM listening_submissions 
        WHERE user_id = ?
    """, (user_id,))
    listening_completed = cur.fetchone()['count']
    
    # Mistakes understood
    cur = db.execute("""
        SELECT COUNT(*) as count 
        FROM mistake_notebook 
        WHERE user_id = ? AND is_understood = 1
    """, (user_id,))
    mistakes_understood = cur.fetchone()['count']
    
    # Writing drafts total
    cur = db.execute("""
        SELECT COUNT(*) as count 
        FROM writing_drafts 
        WHERE user_id = ?
    """, (user_id,))
    writing_drafts_total = cur.fetchone()['count']
    
    # Placement test completed
    cur = db.execute("""
        SELECT COUNT(*) as count 
        FROM placement_tests 
        WHERE user_id = ?
    """, (user_id,))
    placement_completed = cur.fetchone()['count']
    
    metrics = {
        "grammar_lessons_completed": grammar_completed,
        "vocab_reviewed": vocab_reviewed,
        "speaking_topics_completed": speaking_topics_completed,
        "speaking_submissions_total": speaking_submissions_total,
        "listening_completed": listening_completed,
        "mistakes_understood": mistakes_understood,
        "writing_drafts_total": writing_drafts_total,
        "streak_days": streak,
        "placement_test_completed": placement_completed
    }
    
    # Check against achievements table
    cur = db.execute("SELECT * FROM achievements")
    achievements = cur.fetchall()
    
    newly_unlocked = []
    for ach in achievements:
        req_type = ach['requirement_type']
        target = ach['target_value']
        current_val = metrics.get(req_type, 0)
        
        if current_val >= target:
            # Check if already unlocked
            cur2 = db.execute("SELECT id FROM user_achievements WHERE user_id = ? AND achievement_id = ?", (user_id, ach['id']))
            if not cur2.fetchone():
                db.execute("INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)", (user_id, ach['id']))
                newly_unlocked.append(ach['title'])
                
    if newly_unlocked:
        db.commit()
    return newly_unlocked

def get_user_dashboard_analytics(user_id):
    """
    Computes all analytical metrics for the student's dashboard and analytics page.
    """
    db = get_db()
    
    # User info
    cur = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = dict(cur.fetchone())
    
    # Total time spent (estimated in minutes based on logs and activities)
    cur = db.execute("""
        SELECT COALESCE(SUM(duration_seconds), 0) / 60 as total_mins
        FROM learning_logs
        WHERE user_id = ?
    """, (user_id,))
    total_learning_mins = max(10, cur.fetchone()['total_mins'])
    
    # Grammar accuracy
    cur = db.execute("""
        SELECT 
            COUNT(*) as total_attempts,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_attempts
        FROM quiz_attempts
        WHERE user_id = ?
    """, (user_id,))
    q_stats = cur.fetchone()
    total_att = q_stats['total_attempts'] or 0
    correct_att = q_stats['correct_attempts'] or 0
    grammar_accuracy = round((correct_att / total_att) * 100, 1) if total_att > 0 else 0
    
    # Category weakness / strength breakdown
    cur = db.execute("""
        SELECT category,
               COUNT(*) as total,
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
        FROM quiz_attempts
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,))
    category_performance = []
    for row in cur.fetchall():
        pct = round((row['correct'] / row['total']) * 100) if row['total'] > 0 else 0
        category_performance.append({
            "category": row['category'],
            "total": row['total'],
            "correct": row['correct'],
            "percentage": pct
        })
        
    # Sort categories: weakest first
    category_performance.sort(key=lambda x: x['percentage'])
    
    # Speaking practice frequency
    cur = db.execute("""
        SELECT COUNT(*) as count, COALESCE(SUM(duration_seconds), 0) as total_duration
        FROM speaking_submissions
        WHERE user_id = ?
    """, (user_id,))
    speaking_row = cur.fetchone()
    
    # Listening stats
    cur = db.execute("""
        SELECT COUNT(*) as count, COALESCE(AVG(score * 100.0 / max_score), 0) as avg_score
        FROM listening_submissions
        WHERE user_id = ?
    """, (user_id,))
    listening_row = cur.fetchone()
    
    # Weekly learning activity (last 7 days)
    today = date.today()
    weekly_activity = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.isoformat()
        day_label = day.strftime("%a (%b %d)")
        
        cur = db.execute("""
            SELECT COALESCE(SUM(xp_earned), 0) as xp, COUNT(*) as actions
            FROM learning_logs
            WHERE user_id = ? AND log_date = ?
        """, (user_id, day_str))
        log_res = cur.fetchone()
        weekly_activity.append({
            "date": day_str,
            "label": day_label,
            "xp": log_res['xp'],
            "actions": log_res['actions']
        })

    # Vocabulary stats
    from services.vocabulary_service import get_vocab_statistics
    vocab_stats = get_vocab_statistics(user_id)
    
    # Achievements list with unlocked flag
    cur = db.execute("""
        SELECT a.*, ua.unlocked_at
        FROM achievements a
        LEFT JOIN user_achievements ua ON a.id = ua.achievement_id AND ua.user_id = ?
        ORDER BY ua.unlocked_at DESC NULLS LAST, a.id ASC
    """, (user_id,))
    all_achievements = [dict(r) for r in cur.fetchall()]
    unlocked_count = sum(1 for a in all_achievements if a.get('unlocked_at'))

    # Calculate User Level / Rank
    xp = user['xp']
    if xp < 100:
        rank_title = "Language Apprentice"
        next_level_xp = 100
        level_num = 1
    elif xp < 300:
        rank_title = "Grammar Explorer"
        next_level_xp = 300
        level_num = 2
    elif xp < 700:
        rank_title = "Conversationalist"
        next_level_xp = 700
        level_num = 3
    elif xp < 1500:
        rank_title = "Fluent Communicator"
        next_level_xp = 1500
        level_num = 4
    else:
        rank_title = "Master English Scholar"
        next_level_xp = 3000
        level_num = 5

    # Recommendations based on actual performance
    recommendations = []
    if not category_performance or total_att < 5:
        recommendations.append({
            "title": "Take the English Placement Diagnostic",
            "desc": "Calibrate your starting CEFR level and pinpoint grammar priorities.",
            "link": "/placement",
            "icon": "fas fa-clipboard-check",
            "color": "primary"
        })
    elif category_performance[0]['percentage'] < 70:
        weakest = category_performance[0]['category']
        recommendations.append({
            "title": f"Revise {weakest}",
            "desc": f"Your accuracy in {weakest} is currently {category_performance[0]['percentage']}%. Review lessons and clear mistake items.",
            "link": "/grammar",
            "icon": "fas fa-exclamation-triangle",
            "color": "warning"
        })
        
    if vocab_stats['due_today'] > 0:
        recommendations.append({
            "title": f"Review {vocab_stats['due_today']} Spaced Repetition Cards",
            "desc": "Keep newly learned vocabulary active in long-term memory.",
            "link": "/vocabulary",
            "icon": "fas fa-layer-group",
            "color": "info"
        })
        
    if speaking_row['count'] < 4:
        recommendations.append({
            "title": "Deliver a 2–3 Minute Speaking Presentation",
            "desc": "Practice structuring your speech with transitions and timing.",
            "link": "/speaking",
            "icon": "fas fa-microphone-alt",
            "color": "success"
        })

    return {
        "user": user,
        "level_num": level_num,
        "rank_title": rank_title,
        "next_level_xp": next_level_xp,
        "total_learning_mins": total_learning_mins,
        "grammar_accuracy": grammar_accuracy,
        "total_quiz_attempts": total_att,
        "category_performance": category_performance,
        "speaking_count": speaking_row['count'],
        "speaking_total_duration": speaking_row['total_duration'],
        "listening_count": listening_row['count'],
        "listening_avg_score": round(listening_row['avg_score'], 1),
        "vocab_stats": vocab_stats,
        "weekly_activity": weekly_activity,
        "achievements": all_achievements,
        "unlocked_achievements_count": unlocked_count,
        "total_achievements": len(all_achievements),
        "recommendations": recommendations
    }
