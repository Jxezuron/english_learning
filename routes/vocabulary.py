from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db import get_db
from routes.auth import login_required
from services.vocabulary_service import (
    get_due_vocabulary, get_all_vocabulary_for_user,
    record_srs_review, toggle_vocab_favorite, get_vocab_statistics
)

bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')

@bp.route('')
@bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    due_cards = get_due_vocabulary(user_id, limit=30)
    stats = get_vocab_statistics(user_id)
    return render_template('vocabulary.html', due_cards=due_cards, stats=stats)

@bp.route('/dictionary')
@login_required
def dictionary():
    user_id = session['user_id']
    search = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    difficulty = request.args.get('difficulty', '').strip()
    
    words = get_all_vocabulary_for_user(user_id, search=search, category=category, difficulty=difficulty)
    stats = get_vocab_statistics(user_id)
    
    db = get_db()
    cur = db.execute("SELECT DISTINCT category FROM vocabulary ORDER BY category")
    categories = [r['category'] for r in cur.fetchall()]
    
    return render_template(
        'vocabulary_dictionary.html',
        words=words,
        stats=stats,
        categories=categories,
        search=search,
        selected_category=category,
        selected_difficulty=difficulty
    )

@bp.route('/review', methods=('POST',))
@login_required
def review_card():
    user_id = session['user_id']
    data = request.get_json() if request.is_json else request.form
    
    vocab_id = int(data.get('vocab_id'))
    rating = data.get('rating')  # 'again', 'hard', 'good', 'easy'
    
    if rating not in ('again', 'hard', 'good', 'easy'):
        return jsonify({"error": "Invalid rating"}), 400
        
    result = record_srs_review(user_id, vocab_id, rating)
    return jsonify(result)

@bp.route('/favorite/<int:vocab_id>', methods=('POST',))
@login_required
def favorite_toggle(vocab_id):
    user_id = session['user_id']
    new_status = toggle_vocab_favorite(user_id, vocab_id)
    return jsonify({"vocab_id": vocab_id, "is_favorite": new_status})
