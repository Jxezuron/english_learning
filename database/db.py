import sqlite3
import os
import json
from flask import g, current_app

def get_db():
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        # Ensure directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app=None):
    if app:
        with app.app_context():
            _run_init_schema()
    else:
        _run_init_schema()

def _run_init_schema():
    db = get_db()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()

def backup_db_sql():
    """Generates a complete SQL dump of the database."""
    db = get_db()
    lines = []
    for line in db.iterdump():
        lines.append(line)
    return '\n'.join(lines)

def restore_db_sql(sql_script):
    """Restores database from an SQL script."""
    db = get_db()
    db.executescript(sql_script)
    db.commit()
