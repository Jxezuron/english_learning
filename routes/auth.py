import functools
import secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """View decorator that redirects anonymous users to login."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in or continue as guest to access this section.", "info")
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters for security.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
            
        if error is None:
            cur = db.execute("SELECT id FROM users WHERE username = ? OR (email IS NOT NULL AND email != '' AND email = ?)", (username, email))
            if cur.fetchone():
                error = 'That username or email is already registered.'
            else:
                pw_hash = generate_password_hash(password)
                cursor = db.execute("""
                    INSERT INTO users (username, email, password_hash, is_guest)
                    VALUES (?, ?, ?, 0)
                """, (username, email or None, pw_hash))
                db.commit()
                
                # Auto log in
                user_id = cursor.lastrowid
                session.clear()
                session['user_id'] = user_id
                flash(f"Welcome to your English Learning Platform, {username}!", "success")
                return redirect(url_for('dashboard.index'))
                
        flash(error, "danger")
        
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        next_url = request.form.get('next') or request.args.get('next')
        
        db = get_db()
        error = None
        cur = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        
        if user is None or not check_password_hash(user['password_hash'], password):
            error = 'Invalid username or password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash(f"Welcome back, {user['username']}!", "success")
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('dashboard.index'))
            
        flash(error, "danger")
        
    return render_template('auth/login.html')

@bp.route('/guest', methods=('GET', 'POST'))
def guest_login():
    """Instantly logs in a visitor as a guest with full platform capabilities."""
    db = get_db()
    guest_suffix = secrets.token_hex(3)
    username = f"Learner_{guest_suffix}"
    pw_hash = generate_password_hash(secrets.token_urlsafe(12))
    
    cursor = db.execute("""
        INSERT INTO users (username, email, password_hash, is_guest)
        VALUES (?, NULL, ?, 1)
    """, (username, pw_hash))
    user_id = cursor.lastrowid
    db.commit()
    
    session.clear()
    session['user_id'] = user_id
    flash(f"Welcome! You are studying in Guest Mode as {username}.", "info")
    return redirect(url_for('dashboard.index'))

@bp.route('/logout')
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('dashboard.landing'))

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    db = get_db()
    user_id = session['user_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_goals':
            daily_mins = int(request.form.get('daily_goal_minutes', 20))
            daily_words = int(request.form.get('daily_goal_words', 10))
            daily_lessons = int(request.form.get('daily_goal_lessons', 1))
            daily_speaking = int(request.form.get('daily_goal_speaking', 1))
            voice_speed = float(request.form.get('voice_speed', 1.0))
            
            db.execute("""
                UPDATE users 
                SET daily_goal_minutes = ?, daily_goal_words = ?, 
                    daily_goal_lessons = ?, daily_goal_speaking = ?,
                    voice_speed = ?
                WHERE id = ?
            """, (daily_mins, daily_words, daily_lessons, daily_speaking, voice_speed, user_id))
            db.commit()
            flash("Personal learning goals and settings updated successfully!", "success")
            
        elif action == 'change_password':
            old_pw = request.form.get('old_password', '')
            new_pw = request.form.get('new_password', '')
            confirm_pw = request.form.get('confirm_password', '')
            
            cur = db.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
            u = cur.fetchone()
            
            if not check_password_hash(u['password_hash'], old_pw):
                flash("Current password was incorrect.", "danger")
            elif len(new_pw) < 6:
                flash("New password must be at least 6 characters.", "danger")
            elif new_pw != confirm_pw:
                flash("New passwords do not match.", "danger")
            else:
                db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (generate_password_hash(new_pw), user_id))
                db.commit()
                flash("Password changed successfully!", "success")
                
        return redirect(url_for('auth.profile'))
        
    cur = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    return render_template('auth/profile.html', user=user)
