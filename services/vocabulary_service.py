import json
from datetime import datetime, date, timedelta
from database.db import get_db

def ensure_user_vocab_initialized(user_id):
    """
    Ensures the user has active review records for platform vocabulary.
    Adds new vocabulary items to user_vocabulary if not already tracked.
    """
    db = get_db()
    today_str = date.today().isoformat()
    
    db.execute("""
        INSERT OR IGNORE INTO user_vocabulary (user_id, vocab_id, repetition_count, interval_days, ease_factor, next_review_date, last_reviewed_date, history_json, is_favorite)
        SELECT ?, v.id, 0, 0, 2.5, ?, NULL, '[]', 0
        FROM vocabulary v
        WHERE NOT EXISTS (
            SELECT 1 FROM user_vocabulary uv WHERE uv.user_id = ? AND uv.vocab_id = v.id
        )
    """, (user_id, today_str, user_id))
    db.commit()

def get_due_vocabulary(user_id, limit=20):
    """
    Fetches vocabulary words due for review on or before today.
    """
    ensure_user_vocab_initialized(user_id)
    db = get_db()
    today_str = date.today().isoformat()
    
    cur = db.execute("""
        SELECT uv.id as user_vocab_id, uv.repetition_count, uv.interval_days, uv.ease_factor,
               uv.next_review_date, uv.is_favorite,
               v.id as vocab_id, v.word, v.part_of_speech, v.phonetic,
               v.definition_en, v.definition_km, v.example_sentence,
               v.difficulty_level, v.category
        FROM user_vocabulary uv
        JOIN vocabulary v ON uv.vocab_id = v.id
        WHERE uv.user_id = ? AND uv.next_review_date <= ?
        ORDER BY uv.interval_days ASC, uv.next_review_date ASC
        LIMIT ?
    """, (user_id, today_str, limit))
    return [dict(row) for row in cur.fetchall()]

def get_all_vocabulary_for_user(user_id, search="", category="", difficulty=""):
    """
    Retrieves full dictionary with user-specific SRS status and favorites.
    """
    ensure_user_vocab_initialized(user_id)
    db = get_db()
    
    query = """
        SELECT v.*, uv.repetition_count, uv.interval_days, uv.ease_factor,
               uv.next_review_date, uv.last_reviewed_date, uv.is_favorite
        FROM vocabulary v
        LEFT JOIN user_vocabulary uv ON v.id = uv.vocab_id AND uv.user_id = ?
        WHERE 1=1
    """
    params = [user_id]
    
    if search:
        query += " AND (v.word LIKE ? OR v.definition_en LIKE ? OR v.definition_km LIKE ?)"
        term = f"%{search.strip()}%"
        params.extend([term, term, term])
        
    if category:
        query += " AND v.category = ?"
        params.append(category)
        
    if difficulty:
        query += " AND v.difficulty_level = ?"
        params.append(difficulty)
        
    query += " ORDER BY v.word ASC"
    cur = db.execute(query, params)
    return [dict(row) for row in cur.fetchall()]

def record_srs_review(user_id, vocab_id, rating):
    """
    Updates the spaced repetition schedule according to SM-2 algorithm.
    Rating options:
      - 'again': Complete blackout (interval reset to 1 day, rep count reset)
      - 'hard': Recalled with effort (slight interval increase, ease factor decreases)
      - 'good': Standard successful recall (normal interval progression)
      - 'easy': Effortless recall (accelerated interval, ease factor increases)
    """
    db = get_db()
    cur = db.execute("""
        SELECT * FROM user_vocabulary WHERE user_id = ? AND vocab_id = ?
    """, (user_id, vocab_id))
    record = cur.fetchone()
    
    if not record:
        ensure_user_vocab_initialized(user_id)
        cur = db.execute("SELECT * FROM user_vocabulary WHERE user_id = ? AND vocab_id = ?", (user_id, vocab_id))
        record = cur.fetchone()

    reps = record['repetition_count']
    interval = record['interval_days']
    ease = record['ease_factor']
    history = json.loads(record['history_json'] or '[]')
    
    today = date.today()
    today_str = today.isoformat()
    
    if rating == 'again':
        reps = 0
        interval = 1
        ease = max(1.3, ease - 0.2)
    elif rating == 'hard':
        if reps == 0:
            interval = 1
        else:
            interval = max(1, int(interval * 1.2))
        ease = max(1.3, ease - 0.15)
        reps += 1
    elif rating == 'good':
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        else:
            interval = int(interval * ease)
        reps += 1
    elif rating == 'easy':
        if reps == 0:
            interval = 2
        elif reps == 1:
            interval = 5
        else:
            interval = int(interval * ease * 1.3)
        reps += 1
        ease = min(3.0, ease + 0.15)
    else:
        # Default fallback
        interval = 1

    next_date = today + timedelta(days=interval)
    next_date_str = next_date.isoformat()
    
    history.append({
        "date": today_str,
        "rating": rating,
        "new_interval": interval,
        "ease_factor": round(ease, 2)
    })
    
    db.execute("""
        UPDATE user_vocabulary
        SET repetition_count = ?, interval_days = ?, ease_factor = ?,
            next_review_date = ?, last_reviewed_date = ?, history_json = ?
        WHERE user_id = ? AND vocab_id = ?
    """, (reps, interval, ease, next_date_str, today_str, json.dumps(history), user_id, vocab_id))
    
    # Award XP for vocabulary review
    xp = 15 if rating in ('good', 'easy') else 5
    from services.progress_service import award_xp
    award_xp(user_id, xp, f"SRS Vocabulary Review ({rating})")
    
    db.commit()
    
    return {
        "status": "success",
        "rating": rating,
        "new_interval": interval,
        "next_review_date": next_date_str,
        "reps": reps
    }

def toggle_vocab_favorite(user_id, vocab_id):
    """Toggles favorite bookmark for a word."""
    db = get_db()
    ensure_user_vocab_initialized(user_id)
    cur = db.execute("SELECT is_favorite FROM user_vocabulary WHERE user_id = ? AND vocab_id = ?", (user_id, vocab_id))
    row = cur.fetchone()
    new_fav = 0 if (row and row['is_favorite']) else 1
    
    db.execute("UPDATE user_vocabulary SET is_favorite = ? WHERE user_id = ? AND vocab_id = ?", (new_fav, user_id, vocab_id))
    db.commit()
    return new_fav

def get_vocab_statistics(user_id):
    """Calculates overall SRS retention, words mastered, and words learning."""
    ensure_user_vocab_initialized(user_id)
    db = get_db()
    
    cur = db.execute("""
        SELECT 
            COUNT(*) as total_words,
            SUM(CASE WHEN repetition_count >= 5 AND interval_days >= 21 THEN 1 ELSE 0 END) as mastered_words,
            SUM(CASE WHEN repetition_count BETWEEN 1 AND 4 THEN 1 ELSE 0 END) as learning_words,
            SUM(CASE WHEN repetition_count = 0 THEN 1 ELSE 0 END) as new_words,
            SUM(CASE WHEN next_review_date <= date('now') THEN 1 ELSE 0 END) as due_today,
            SUM(CASE WHEN is_favorite = 1 THEN 1 ELSE 0 END) as favorites_count
        FROM user_vocabulary
        WHERE user_id = ?
    """, (user_id,))
    stats = dict(cur.fetchone())
    
    # Calculate retention rate from historical ratings
    cur2 = db.execute("SELECT history_json FROM user_vocabulary WHERE user_id = ? AND history_json != '[]'", (user_id,))
    all_reviews = []
    for r in cur2.fetchall():
        reviews = json.loads(r['history_json'] or '[]')
        all_reviews.extend(reviews)
        
    total_reviews = len(all_reviews)
    successful_reviews = sum(1 for rv in all_reviews if rv.get('rating') in ('good', 'easy'))
    retention_rate = round((successful_reviews / total_reviews) * 100) if total_reviews > 0 else 100
    
    stats['total_reviews'] = total_reviews
    stats['retention_rate'] = retention_rate
    return stats
