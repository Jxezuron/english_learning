import io
import csv
import json
import os
from datetime import datetime
from flask import Blueprint, render_template, request, Response, redirect, url_for, flash, session, current_app, send_file
from database.db import get_db, backup_db_sql, restore_db_sql
from routes.auth import login_required
from services.progress_service import get_user_dashboard_analytics

bp = Blueprint('backup', __name__, url_prefix='/backup')

@bp.route('')
@bp.route('/')
@login_required
def index():
    return render_template('backup.html')

@bp.route('/export/vocabulary.csv')
@login_required
def export_vocabulary_csv():
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("""
        SELECT v.word, v.part_of_speech, v.phonetic, v.definition_en, v.definition_km, 
               v.example_sentence, v.difficulty_level, v.category,
               COALESCE(uv.repetition_count, 0) as repetitions,
               COALESCE(uv.interval_days, 0) as interval_days,
               COALESCE(uv.ease_factor, 2.5) as ease_factor,
               COALESCE(uv.next_review_date, 'N/A') as next_review_date
        FROM vocabulary v
        LEFT JOIN user_vocabulary uv ON v.id = uv.vocab_id AND uv.user_id = ?
        ORDER BY v.word ASC
    """, (user_id,))
    rows = cur.fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Word", "Part of Speech", "Phonetic", "English Definition", "Khmer Definition", "Example Sentence", "Difficulty", "Category", "Repetitions", "Interval (Days)", "Ease Factor", "Next Review Date"])
    
    for r in rows:
        writer.writerow([r['word'], r['part_of_speech'], r['phonetic'], r['definition_en'], r['definition_km'], r['example_sentence'], r['difficulty_level'], r['category'], r['repetitions'], r['interval_days'], r['ease_factor'], r['next_review_date']])
        
    output.seek(0)
    filename = f"english_vocabulary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@bp.route('/export/mistakes.csv')
@login_required
def export_mistakes_csv():
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("""
        SELECT source_module, question_text, student_answer, correct_answer, 
               explanation, grammar_category, is_understood, retry_count, created_at
        FROM mistake_notebook
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Source Module", "Question", "Your Answer", "Correct Answer", "Grammar Category", "Understood", "Retry Count", "Explanation", "Recorded Date"])
    
    for r in rows:
        writer.writerow([
            r['source_module'], r['question_text'], r['student_answer'],
            r['correct_answer'], r['grammar_category'],
            "Yes" if r['is_understood'] == 1 else "No",
            r['retry_count'], r['explanation'], r['created_at']
        ])
        
    output.seek(0)
    filename = f"english_mistake_notebook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@bp.route('/export/speaking.txt')
@login_required
def export_speaking_txt():
    user_id = session['user_id']
    db = get_db()
    
    cur = db.execute("""
        SELECT ss.*, st.title as topic_title, st.topic_number
        FROM speaking_submissions ss
        JOIN speaking_topics st ON ss.topic_id = st.id
        WHERE ss.user_id = ?
        ORDER BY ss.created_at DESC
    """, (user_id,))
    submissions = cur.fetchall()
    
    output = io.StringIO()
    output.write("====================================================\n")
    output.write("ENGLISH LEARNING PLATFORM - SAVED SPEAKING SPEECHES\n")
    output.write(f"Exported At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("====================================================\n\n")
    
    for s in submissions:
        output.write(f"--- [Topic {s['topic_number']}] {s['topic_title']} ---\n")
        output.write(f"Title: {s['presentation_title'] or 'Untitled Speech'}\n")
        output.write(f"Date: {s['created_at']} | Duration: {s['duration_seconds']} seconds | Self-Rating: {s['self_rating']}/5\n")
        output.write("\nOUTLINE NOTES:\n")
        output.write(f"{s['outline_notes'] or '(No outline notes)'}\n")
        output.write("\nRECORDED / RECOGNIZED TRANSCRIPT:\n")
        output.write(f"{s['recorded_transcript'] or '(No transcript recorded)'}\n")
        output.write("\nTEACHER FEEDBACK:\n")
        output.write(f"{s['feedback_notes'] or 'Keep practicing!'}\n")
        output.write("\n" + "="*50 + "\n\n")
        
    output.seek(0)
    filename = f"speaking_presentations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return Response(
        output.getvalue(),
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@bp.route('/export/progress.json')
@login_required
def export_progress_json():
    user_id = session['user_id']
    analytics = get_user_dashboard_analytics(user_id)
    
    filename = f"learning_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    return Response(
        json.dumps(analytics, indent=2, default=str),
        mimetype="application/json; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@bp.route('/download-db')
@login_required
def download_database_backup():
    """Generates an SQL dump file download of the complete database."""
    sql_dump = backup_db_sql()
    filename = f"english_learning_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    return Response(
        sql_dump,
        mimetype="application/sql; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@bp.route('/restore-db', methods=('POST',))
@login_required
def restore_database():
    """Restores database from an uploaded SQL script file."""
    if 'backup_file' not in request.files:
        flash("No file was selected for restoration.", "warning")
        return redirect(url_for('backup.index'))
        
    uploaded = request.files['backup_file']
    if not uploaded.filename.endswith('.sql'):
        flash("Invalid file format. Please upload an .sql database backup file.", "danger")
        return redirect(url_for('backup.index'))
        
    try:
        content = uploaded.read().decode('utf-8')
        restore_db_sql(content)
        flash("Database restored successfully!", "success")
    except Exception as e:
        flash(f"Restoration failed: {str(e)}", "danger")
        
    return redirect(url_for('backup.index'))
