import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.progress_service import award_xp

bp = Blueprint('listening', __name__, url_prefix='/listening')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("""
        SELECT le.*,
               (SELECT MAX(ls.score * 100 / ls.max_score) FROM listening_submissions ls WHERE ls.exercise_id = le.id AND ls.user_id = ?) as best_score,
               (SELECT COUNT(*) FROM listening_submissions ls WHERE ls.exercise_id = le.id AND ls.user_id = ?) as attempts_count
        FROM listening_exercises le
        ORDER BY le.order_index ASC, le.id ASC
    """, (user_id, user_id))
    exercises = cur.fetchall()
    
    # Group by level
    grouped = {
        "Beginner": [],
        "Intermediate": [],
        "Upper-intermediate": []
    }
    for ex in exercises:
        lvl = ex['difficulty_level']
        if lvl in grouped:
            grouped[lvl].append(dict(ex))
        else:
            grouped.setdefault(lvl, []).append(dict(ex))
            
    return render_template('listening.html', grouped=grouped)

@bp.route('/<int:exercise_id>')
@login_required
def exercise_detail(exercise_id):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT * FROM listening_exercises WHERE id = ?", (exercise_id,))
    exercise = cur.fetchone()
    if not exercise:
        flash("Listening exercise not found.", "warning")
        return redirect(url_for('listening.index'))
        
    ex_dict = dict(exercise)
    ex_dict['questions'] = json.loads(ex_dict['questions_json'])
    
    # User's previous attempts
    cur_sub = db.execute("""
        SELECT * FROM listening_submissions 
        WHERE user_id = ? AND exercise_id = ? 
        ORDER BY completed_at DESC LIMIT 3
    """, (user_id, exercise_id))
    attempts = cur_sub.fetchall()
    
    return render_template('listening_exercise.html', exercise=ex_dict, attempts=attempts)

@bp.route('/<int:exercise_id>/submit', methods=('POST',))
@login_required
def submit_exercise(exercise_id):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT * FROM listening_exercises WHERE id = ?", (exercise_id,))
    exercise = cur.fetchone()
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
        
    questions = json.loads(exercise['questions_json'])
    submitted_data = request.get_json() if request.is_json else request.form
    
    total = len(questions)
    correct_count = 0
    feedback_list = []
    
    for idx, q in enumerate(questions):
        user_ans = str(submitted_data.get(f"q_{idx}", submitted_data.get(str(idx), ""))).strip().lower()
        correct_ans = str(q['correct_answer']).strip().lower()
        
        # Check matching (including array of accepted spellings for fill_blank)
        is_correct = False
        if q['type'] == 'fill_blank' and 'options' in q and isinstance(q['options'], list):
            accepted = [str(opt).strip().lower() for opt in q['options']]
            is_correct = (user_ans in accepted)
        else:
            is_correct = (user_ans == correct_ans)
            
        if is_correct:
            correct_count += 1
        else:
            # Save into Mistake Notebook
            db.execute("""
                INSERT INTO mistake_notebook (user_id, source_module, question_text, student_answer, correct_answer, explanation, grammar_category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, 'listening', q['question'], user_ans or '(No answer)', q['correct_answer'], q['explanation'], f"Listening: {exercise['topic_category']}"))
            
        feedback_list.append({
            "question_index": idx,
            "question": q['question'],
            "user_answer": user_ans,
            "correct_answer": q['correct_answer'],
            "is_correct": is_correct,
            "explanation": q['explanation']
        })

    score_pct = round((correct_count / total) * 100) if total > 0 else 0
    
    # Save submission
    db.execute("""
        INSERT INTO listening_submissions (user_id, exercise_id, score, max_score, answers_json)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, exercise_id, correct_count, total, json.dumps(feedback_list)))
    
    # Award XP
    xp_earned = correct_count * 10
    award_xp(user_id, xp_earned, f"Listening Exercise: {exercise['title']}")
    db.commit()
    
    result = {
        "score": correct_count,
        "max_score": total,
        "percentage": score_pct,
        "xp_earned": xp_earned,
        "feedback": feedback_list,
        "audio_script": exercise['audio_script']
    }
    
    if request.is_json:
        return jsonify(result)
        
    flash(f"Listening exercise complete! You scored {correct_count} / {total} ({score_pct}%). Transcript is now revealed below.", "success")
    return render_template('listening_exercise.html', exercise=dict(exercise, questions=questions), attempts=[], result=result)
