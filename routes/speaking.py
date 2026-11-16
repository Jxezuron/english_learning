import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.progress_service import award_xp

bp = Blueprint('speaking', __name__, url_prefix='/speaking')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("""
        SELECT st.*,
               (SELECT COUNT(*) FROM speaking_submissions ss WHERE ss.topic_id = st.id AND ss.user_id = ?) as submission_count,
               (SELECT MAX(duration_seconds) FROM speaking_submissions ss WHERE ss.topic_id = st.id AND ss.user_id = ?) as best_duration
        FROM speaking_topics st
        ORDER BY st.topic_number ASC
    """, (user_id, user_id))
    topics = cur.fetchall()
    
    # Recent submissions
    cur2 = db.execute("""
        SELECT ss.*, st.title as topic_title
        FROM speaking_submissions ss
        JOIN speaking_topics st ON ss.topic_id = st.id
        WHERE ss.user_id = ?
        ORDER BY ss.created_at DESC LIMIT 5
    """, (user_id,))
    recent_submissions = cur2.fetchall()
    
    return render_template('speaking.html', topics=topics, recent_submissions=recent_submissions)

@bp.route('/topic/<int:topic_number>')
@login_required
def topic_detail(topic_number):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT * FROM speaking_topics WHERE topic_number = ?", (topic_number,))
    topic = cur.fetchone()
    if not topic:
        flash("Speaking topic not found.", "warning")
        return redirect(url_for('speaking.index'))
        
    t_dict = dict(topic)
    t_dict['structure'] = json.loads(t_dict['structure_json'])
    t_dict['vocabulary'] = json.loads(t_dict['vocabulary_json'])
    t_dict['transitions'] = json.loads(t_dict['transition_phrases_json'])
    t_dict['guiding_questions'] = json.loads(t_dict['guiding_questions_json'])
    
    # User's previous attempts for this topic
    cur_sub = db.execute("""
        SELECT * FROM speaking_submissions 
        WHERE user_id = ? AND topic_id = ?
        ORDER BY created_at DESC
    """, (user_id, topic['id']))
    submissions = cur_sub.fetchall()
    
    return render_template('speaking_topic.html', topic=t_dict, submissions=submissions)

@bp.route('/topic/<int:topic_number>/submit', methods=('POST',))
@login_required
def submit_presentation(topic_number):
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("SELECT id FROM speaking_topics WHERE topic_number = ?", (topic_number,))
    topic = cur.fetchone()
    if not topic:
        flash("Speaking topic not found.", "warning")
        return redirect(url_for('speaking.index'))
        
    title = request.form.get('presentation_title', f'Presentation on Topic {topic_number}').strip()
    outline = request.form.get('outline_notes', '').strip()
    transcript = request.form.get('recorded_transcript', '').strip()
    duration = int(request.form.get('duration_seconds', 0))
    self_rating = int(request.form.get('self_rating', 3))
    
    # Automated pedagogical teacher feedback based on speech duration and structure
    feedback_points = []
    if duration < 90:
        feedback_points.append("Your speech was under 1.5 minutes. In formal ESL speaking exams, aim for 2–3 minutes by expanding each body point with concrete examples.")
    elif 120 <= duration <= 180:
        feedback_points.append("Outstanding pacing! Your presentation fell precisely within the targeted 2–3 minute benchmark.")
    elif duration > 180:
        feedback_points.append("You spoke for over 3 minutes. Your fluency is strong; practice summarizing your conclusion concisely to stay within time constraints.")
        
    word_count = len(transcript.split()) if transcript else 0
    if word_count > 0:
        wpm = round((word_count / (max(duration, 30) / 60)))
        feedback_points.append(f"Speech volume: ~{word_count} words recorded. Speaking rate was approximately {wpm} words per minute (target: 120–150 WPM).")
        
    teacher_feedback = " ".join(feedback_points)
    
    db.execute("""
        INSERT INTO speaking_submissions (user_id, topic_id, presentation_title, outline_notes, recorded_transcript, duration_seconds, self_rating, feedback_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, topic['id'], title, outline, transcript, duration, self_rating, teacher_feedback))
    
    # Award 40 XP for a completed speaking presentation
    award_xp(user_id, 40, f"Delivered Speaking Presentation - Topic {topic_number}")
    db.commit()
    
    flash("Congratulations! Your speaking presentation and transcript have been safely saved.", "success")
    return redirect(url_for('speaking.topic_detail', topic_number=topic_number))
