-- English Learning Platform Database Schema

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    is_guest INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 1,
    last_active_date TEXT,
    daily_goal_minutes INTEGER DEFAULT 20,
    daily_goal_words INTEGER DEFAULT 10,
    daily_goal_lessons INTEGER DEFAULT 1,
    daily_goal_speaking INTEGER DEFAULT 1,
    voice_speed REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS placement_tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,
    level_assessment TEXT NOT NULL,
    grammar_breakdown TEXT NOT NULL,
    weak_topics TEXT NOT NULL,
    strong_topics TEXT NOT NULL,
    recommended_path TEXT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS grammar_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    cefr_level TEXT NOT NULL,
    order_index INTEGER DEFAULT 0,
    summary TEXT NOT NULL,
    formula TEXT,
    explanation_markdown TEXT NOT NULL,
    examples_json TEXT NOT NULL,
    common_mistakes_json TEXT,
    tips TEXT
);

CREATE TABLE IF NOT EXISTS grammar_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    category TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES grammar_lessons(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lesson_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    selected_answer TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES grammar_lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES grammar_quizzes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS speaking_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_number INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    subtitle TEXT NOT NULL,
    duration_target TEXT DEFAULT '2–3 Minutes',
    overview TEXT NOT NULL,
    structure_json TEXT NOT NULL,
    vocabulary_json TEXT NOT NULL,
    transition_phrases_json TEXT NOT NULL,
    sample_speech TEXT NOT NULL,
    guiding_questions_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS speaking_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    presentation_title TEXT,
    outline_notes TEXT,
    recorded_transcript TEXT,
    duration_seconds INTEGER DEFAULT 0,
    self_rating INTEGER DEFAULT 3,
    feedback_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES speaking_topics(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL,
    part_of_speech TEXT NOT NULL,
    phonetic TEXT NOT NULL,
    definition_en TEXT NOT NULL,
    definition_km TEXT NOT NULL,
    example_sentence TEXT NOT NULL,
    difficulty_level TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vocab_id INTEGER NOT NULL,
    repetition_count INTEGER DEFAULT 0,
    interval_days INTEGER DEFAULT 0,
    ease_factor REAL DEFAULT 2.5,
    next_review_date TEXT NOT NULL,
    last_reviewed_date TEXT,
    history_json TEXT DEFAULT '[]',
    is_favorite INTEGER DEFAULT 0,
    UNIQUE(user_id, vocab_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vocab_id) REFERENCES vocabulary(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pronunciation_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_text TEXT NOT NULL,
    item_type TEXT NOT NULL,
    phonetic TEXT,
    focus_sound TEXT,
    difficulty TEXT NOT NULL,
    tip TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS listening_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    difficulty_level TEXT NOT NULL,
    topic_category TEXT NOT NULL,
    situation_description TEXT NOT NULL,
    audio_script TEXT NOT NULL,
    questions_json TEXT NOT NULL,
    order_index INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS listening_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,
    answers_json TEXT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES listening_exercises(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mistake_notebook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    source_module TEXT NOT NULL,
    question_text TEXT NOT NULL,
    student_answer TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    grammar_category TEXT NOT NULL,
    is_understood INTEGER DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS study_planner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_date TEXT NOT NULL,
    task_type TEXT NOT NULL,
    task_title TEXT NOT NULL,
    target_id INTEGER,
    is_completed INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS writing_drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    prompt_category TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    word_count INTEGER DEFAULT 0,
    sentence_count INTEGER DEFAULT 0,
    analysis_json TEXT,
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    badge_icon TEXT NOT NULL,
    category TEXT NOT NULL,
    requirement_type TEXT NOT NULL,
    target_value INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, achievement_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS learning_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL,
    duration_seconds INTEGER DEFAULT 0,
    xp_earned INTEGER DEFAULT 0,
    notes TEXT,
    log_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_user_vocab_review ON user_vocabulary(user_id, next_review_date);
CREATE INDEX IF NOT EXISTS idx_mistakes_user_cat ON mistake_notebook(user_id, grammar_category, is_understood);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user ON quiz_attempts(user_id, lesson_id);
CREATE INDEX IF NOT EXISTS idx_planner_user_date ON study_planner(user_id, plan_date);
CREATE INDEX IF NOT EXISTS idx_logs_user_date ON learning_logs(user_id, log_date);
