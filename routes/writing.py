import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.tutor_service import analyze_writing_text, LINKING_WORDS_TAXONOMY
from services.progress_service import award_xp

bp = Blueprint('writing', __name__, url_prefix='/writing')

WRITING_PROMPTS = [
    {
        "category": "personal_introduction",
        "title": "Craft Your 100-Word Personal Introduction",
        "description": "Introduce your name, your background, what motivates your English learning journey, and one personal aspiration."
    },
    {
        "category": "short_paragraph",
        "title": "My Ideal Daily Morning Routine",
        "description": "Describe your morning habits using Present Simple tense and adverbs of frequency (always, usually, rarely)."
    },
    {
        "category": "opinion_paragraph",
        "title": "Can Technology Replace Human Language Teachers?",
        "description": "Express your viewpoint using contrast linking words (However, Although, On the other hand) and cause connectors (Therefore, Because)."
    },
    {
        "category": "descriptive_writing",
        "title": "The Sights and Sounds of My Hometown",
        "description": "Paint a sensory picture of your favorite place in Cambodia or your city using rich adjectives instead of basic words."
    },
    {
        "category": "speaking_draft",
        "title": "2–3 Minute Speech Outline: An Unforgettable Life Lesson",
        "description": "Draft your narrative speech script using past narrative tenses (Past Simple and Past Continuous) with transitions."
    }
]

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    db = get_db()
    
    # Load user's saved drafts
    cur = db.execute("SELECT * FROM writing_drafts WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
    drafts = cur.fetchall()
    
    selected_draft_id = request.args.get('draft_id')
    active_draft = None
    if selected_draft_id:
        cur = db.execute("SELECT * FROM writing_drafts WHERE id = ? AND user_id = ?", (selected_draft_id, user_id))
        active_draft = cur.fetchone()
        
    return render_template(
        'writing.html',
        prompts=WRITING_PROMPTS,
        drafts=drafts,
        active_draft=active_draft,
        linking_taxonomy=LINKING_WORDS_TAXONOMY
    )

@bp.route('/analyze', methods=('POST',))
@login_required
def analyze_text():
    data = request.get_json() or {}
    text = data.get('content', '')
    analysis = analyze_writing_text(text)
    return jsonify(analysis)

@bp.route('/save', methods=('POST',))
@login_required
def save_draft():
    user_id = session['user_id']
    db = get_db()
    
    draft_id = request.form.get('draft_id')
    title = request.form.get('title', 'Untitled Writing Practice').strip()
    category = request.form.get('prompt_category', 'general').strip()
    content = request.form.get('content', '').strip()
    
    analysis = analyze_writing_text(content)
    analysis_json = json.dumps(analysis)
    
    if draft_id and draft_id.isdigit() and int(draft_id) > 0:
        db.execute("""
            UPDATE writing_drafts
            SET title = ?, prompt_category = ?, content = ?, word_count = ?,
                sentence_count = ?, analysis_json = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (title, category, content, analysis['word_count'], analysis['sentence_count'], analysis_json, draft_id, user_id))
        saved_id = draft_id
        flash("Draft updated successfully!", "success")
    else:
        cursor = db.execute("""
            INSERT INTO writing_drafts (user_id, prompt_category, title, content, word_count, sentence_count, analysis_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, category, title, content, analysis['word_count'], analysis['sentence_count'], analysis_json))
        saved_id = cursor.lastrowid
        award_xp(user_id, 25, f"Saved Written Draft: {title}")
        flash("New writing draft saved to your portfolio! Earned 25 XP.", "success")
        
    db.commit()
    return redirect(url_for('writing.index', draft_id=saved_id))
