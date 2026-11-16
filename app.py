import os
import secrets
from flask import Flask, render_template, g, session
from config import config
from database.db import get_db, close_db, init_db
from database.seed_data import seed_all_data

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # Ensure the instance directory exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Database teardown registration
    app.teardown_appcontext(close_db)

    # CLI commands
    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        init_db(app)
        db = get_db()
        seed_all_data(db)
        print("Initialized and seeded the database successfully.")

    @app.cli.command('seed-db')
    def seed_db_command():
        """Seed foundational educational data."""
        with app.app_context():
            db = get_db()
            seed_all_data(db)
            print("Seeded educational lessons, vocabulary, and exercises.")

    # Context processors and user loader
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            db = get_db()
            cur = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            g.user = cur.fetchone()

        # Simple session CSRF token for forms
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(16)
        g.csrf_token = session['csrf_token']

    @app.context_processor
    def inject_global_template_vars():
        return {
            "current_user": g.user,
            "csrf_token": session.get('csrf_token', '')
        }

    # Custom Jinja filters
    @app.template_filter('format_seconds')
    def format_seconds(seconds):
        if not seconds:
            return "0:00"
        m = seconds // 60
        s = seconds % 60
        return f"{m}:{s:02d}"

    # Register Blueprints
    from routes import (
        auth, dashboard, placement, grammar,
        speaking, vocabulary, listening,
        pronunciation, writing, mistakes,
        planner, progress, backup
    )

    app.register_blueprint(dashboard.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(placement.bp)
    app.register_blueprint(grammar.bp)
    app.register_blueprint(speaking.bp)
    app.register_blueprint(vocabulary.bp)
    app.register_blueprint(listening.bp)
    app.register_blueprint(pronunciation.bp)
    app.register_blueprint(writing.bp)
    app.register_blueprint(mistakes.bp)
    app.register_blueprint(planner.bp)
    app.register_blueprint(progress.bp)
    app.register_blueprint(backup.bp)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html', error=str(e)), 500

    return app

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        init_db(app)
        db = get_db()
        seed_all_data(db)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
