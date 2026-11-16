# Advanced English Learning Platform 🎓
### Complete Personal Language-Learning System Powered by Python & Flask

An educational, modular personal English learning platform designed to help students **understand English, think in English, construct precise sentences, improve listening comprehension, practice pronunciation, and confidently deliver 2–3-minute oral presentations**.

---

## 🌟 Key Functional Modules

1. **English Placement Diagnostic**
   - Calibrates proficiency across 11 core competencies: *Present Simple, Present Continuous, Past Simple, Present Perfect, Comparative & Superlative, Be Going To, Should, Linking Words, Vocabulary, Sentence Construction, and Reading Comprehension*.
   - Diagnoses strong vs. weak topics and generates a personalized learning path.
   - Retakeable at any time with complete historical tracking.
   - Includes transparent educational guidance notice.

2. **Pronunciation Laboratory**
   - Native audio playback using browser Speech Synthesis (normal and 0.7x slow rate).
   - Voice microphone recording & speech comparison using the HTML5 Web Speech API.
   - Word-level match breakdown and similarity percentages.
   - Contrast minimal pairs (/θ/ vs /s/, /r/ vs /l/), past tense -ed endings (/t/, /d/, /ɪd/), silent letters, and sentence rhythm.
   - Clear browser compatibility notes.

3. **Speaking Presentation Studio (4 Core Topics)**
   - Topic 1: *Personal Background, Daily Routine & Passions*
   - Topic 2: *Hometown, Cultural Heritage & Community Life*
   - Topic 3: *Educational Aspirations, Career Goals & Technology*
   - Topic 4: *A Memorable Experience, Travel & Life Lessons*
   - Interactive presentation stopwatch with 30-second prep countdown and 2–3 minute presentation pacing indicators.
   - Integrated speech recognition pad, outline notes builder, self-rating, and automated pedagogical teacher feedback.

4. **Smart Spaced Repetition Vocabulary (SuperMemo SM-2)**
   - Flashcards with English definitions, **Khmer translations**, IPA phonetics, part of speech, and contextual example sentences.
   - Four recall grades: *Again (1), Hard (2), Good (3), Easy (4)* with keyboard shortcuts.
   - Persistent scheduling in SQLite calculating exact review dates and retention rates.
   - Searchable, filterable word bank with CSV export.

5. **Listening Comprehension Center (3 Tiers)**
   - **Beginner**: Short everyday conversations, classroom exchanges, introductions, and daily routines.
   - **Intermediate**: Dialogues on healthy living, education, describing people, and friendship.
   - **Upper-Intermediate**: Debates, short stories, opinions, and everyday situations.
   - Interactive multi-format questions: Multiple Choice, True/False, and Fill-in-the-Blank.
   - Collapsible official dialogue transcript revealed after submission with detailed explanations.

6. **Interactive Writing Workshop**
   - Practice sentence construction, short paragraphs, descriptive writing, opinion essays, and speech drafts.
   - Real-time word and sentence counters with average sentence length balance.
   - Mechanical and grammar checklist (capitalization, sentence endings, standalone "I", length).
   - Common ESL mistake pattern detector.
   - Linking word classifier and discourse connector suggestions across 5 categories.
   - Vocabulary synonym upgrades for overused basic words.
   - Draft portfolio saving and editing.

7. **Personal Mistake Notebook**
   - Automatically aggregates errors from placement tests, grammar quizzes, and listening exercises.
   - Categorized by grammar topic with student answer, correct answer, and explanation.
   - In-app interactive retry modal and dynamic similar practice question generator.
   - "Mark as Understood" tracking to systematically eliminate recurring errors.

8. **Personal Study Planner**
   - Daily learning targets: study minutes, vocabulary cards, grammar lessons, and speaking speeches.
   - Weekly calendar view (Monday to Sunday) with task scheduling and completion checkboxes.
   - Consecutive daily study streak tracker.

9. **Gamification & Learning Analytics**
   - XP point reward system for all activities.
   - 12 milestone achievement badges (e.g. *First Steps, Word Collector, Confident Speaker, Consistency*).
   - Zero-CDN, lightweight HTML5 Canvas charts: Weekly Activity XP chart, Vocabulary Retention Donut, and Grammar Category Accuracy bars.

10. **Data Sovereignty, Export & Backup**
    - Export Vocabulary Dictionary as **CSV**.
    - Export Personal Mistake Notebook as **CSV**.
    - Export Saved Speaking Speeches as **TXT**.
    - Export Learning Progress & Analytics as **JSON**.
    - One-click SQLite database SQL dump download and restoration from file upload.

---

## 🛠️ Architecture & Technologies

- **Backend**: Python 3, Flask 3.1, Werkzeug, Jinja2.
- **Database**: SQLite with parameterized queries and foreign key constraints.
- **Frontend**: Semantic HTML5, modern CSS3 design system, Vanilla JavaScript (ES6+).
- **APIs**: HTML5 Web Speech API (`SpeechSynthesis` and `SpeechRecognition`), Canvas API.
- **Security**: Password hashing (`werkzeug.security`), CSRF tokens on forms and AJAX headers, `HttpOnly` sessions, input sanitization.

### Project Structure

```text
english_learning/
├── app.py                      # Application factory & runner
├── config.py                   # Environment configuration & security settings
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows one-click startup script
├── run.ps1                     # Windows PowerShell startup script
├── run.sh                      # Linux/macOS startup script
│
├── database/
│   ├── db.py                   # Connection helpers, backup/restore functions
│   ├── schema.sql              # Normalized SQLite schema
│   └── seed_data.py            # Comprehensive curriculum, vocabulary & quiz seed data
│
├── routes/
│   ├── auth.py                 # User authentication, profiles & guest access
│   ├── dashboard.py            # Personal student dashboard & daily goals
│   ├── placement.py            # 25-question placement diagnostic
│   ├── grammar.py              # Grammar lessons & interactive quizzes
│   ├── speaking.py             # 4 speaking topics & presentation studio
│   ├── vocabulary.py           # Spaced repetition flashcards & word bank
│   ├── listening.py            # 3-tier listening comprehension center
│   ├── pronunciation.py        # Web Speech pronunciation laboratory
│   ├── writing.py              # Interactive writing workshop & assistant
│   ├── mistakes.py             # Personal mistake notebook & practice generator
│   ├── planner.py              # Daily & weekly study planner
│   ├── progress.py             # Analytics dashboard & achievement badges
│   └── backup.py               # Multi-format exports & database backups
│
├── services/
│   ├── quiz_service.py         # Diagnostic scoring, CEFR mapping & recommendations
│   ├── vocabulary_service.py   # SuperMemo SM-2 spaced repetition scheduler
│   ├── progress_service.py     # XP, streaks, level calculation & analytics
│   └── tutor_service.py        # Writing linguistic analysis & drill generation
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom educational design system
│   └── js/
│       ├── app.js              # Speech synthesis helper, CSRF & toasts
│       ├── speaking.js         # 2-3 minute presentation timer & voice transcription
│       ├── quiz.js             # Interactive quiz feedback engine
│       ├── vocabulary.js       # SRS flashcards & keyboard controls
│       ├── pronunciation.js    # Speech recognition comparison algorithm
│       ├── writing.js          # Live writing assistant & counters
│       └── charts.js           # Zero-dependency HTML5 Canvas charts
│
├── templates/
│   ├── base.html               # Global responsive layout & navigation
│   ├── index.html              # Landing page
│   ├── dashboard.html          # Student dashboard
│   ├── placement.html          # Placement diagnostic
│   ├── placement_result.html   # Diagnostic report & personalized path
│   ├── placement_history.html  # Past placement attempts
│   ├── grammar.html            # Grammar lessons catalog
│   ├── grammar_lesson.html     # Grammar lesson & quiz
│   ├── speaking.html           # 4 speaking topics catalog
│   ├── speaking_topic.html     # Speaking workstation & timer
│   ├── vocabulary.html         # Spaced repetition deck
│   ├── vocabulary_dictionary.html # Searchable vocabulary bank
│   ├── listening.html          # Listening comprehension catalog
│   ├── listening_exercise.html # Audio player, quiz & transcript
│   ├── pronunciation.html      # Pronunciation laboratory
│   ├── writing.html            # Writing workshop
│   ├── mistakes.html           # Personal mistake notebook
│   ├── planner.html            # Study planner & weekly calendar
│   ├── progress.html           # Analytics & achievement badges
│   ├── backup.html             # Data export & database restore
│   ├── 404.html                # Friendly 404 error page
│   ├── 500.html                # Friendly 500 error page
│   └── auth/
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
└── tests/
    └── test_platform.py        # Automated test suite (11 unit tests)
```

---

## 💻 Beginner-Friendly Setup Instructions for Windows

Follow these simple steps to run the platform on Windows:

### Step 1: Install Python 3
1. Download Python 3 (version 3.10, 3.11, 3.12, or 3.13) from [python.org](https://www.python.org/downloads/).
2. **Important**: In the installer, check the box that says **"Add python.exe to PATH"** before clicking Install.

### Step 2: Open Command Prompt or PowerShell
1. Press `Windows Key + R`, type `cmd`, and press `Enter`.
2. Navigate to the project directory:
   ```cmd
   cd path\to\english_learning
   ```

### Step 3: Option A — One-Click Automatic Start (Recommended)
Simply double-click `run.bat` (or in PowerShell run `.\run.ps1`).  
The script will automatically:
- Create a Python virtual environment (`venv`).
- Install all necessary packages.
- Initialize and seed the SQLite database.
- Start the development server at `http://localhost:5000`.

### Step 3: Option B — Manual Step-by-Step Setup

1. **Create a virtual environment:**
   ```cmd
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - In Command Prompt (`cmd`):
     ```cmd
     venv\Scripts\activate
     ```
   - In PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Initialize and seed the database:**
   ```cmd
   flask init-db
   ```
   *(Or run: `python -c "from app import create_app; from database.db import init_db, get_db; from database.seed_data import seed_all_data; app = create_app(); app.app_context().push(); init_db(app); seed_all_data(get_db()); print('Ready!')"`)*

5. **Start the Flask development server:**
   ```cmd
   python app.py
   ```

6. **Open your browser:**
   Go to: **`http://localhost:5000`**  
   Click **"Instant Guest Start"** to explore immediately, or register a free student account.

---

## 🐧 Setup Instructions for Linux / macOS

```bash
cd english_learning
chmod +x run.sh
./run.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
Visit `http://localhost:5000` in your web browser.

---

## 🧪 Running Automated Unit Tests

To run the complete test suite verifying database operations, authentication, SM-2 spaced repetition, placement diagnostics, quiz scoring, writing analysis, and exports:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

All 11 integration tests will execute and confirm platform integrity.
