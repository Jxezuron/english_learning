import unittest
import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database.db import get_db, init_db
from database.seed_data import seed_all_data
from services.vocabulary_service import record_srs_review, get_due_vocabulary, get_vocab_statistics
from services.quiz_service import evaluate_placement_test, evaluate_lesson_quiz
from services.tutor_service import analyze_writing_text, generate_practice_question_for_mistake
from services.progress_service import award_xp, check_and_unlock_achievements, get_user_dashboard_analytics

class EnglishPlatformTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app('default')
        self.app.config['DATABASE'] = self.db_path
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test-secret-key-1234'
        self.client = self.app.test_client()

        with self.app.app_context():
            init_db(self.app)
            db = get_db()
            seed_all_data(db)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # 1. Database & Seed Verification
    def test_database_seeded_properly(self):
        with self.app.app_context():
            db = get_db()
            lessons = db.execute("SELECT COUNT(*) as count FROM grammar_lessons").fetchone()['count']
            self.assertGreaterEqual(lessons, 10, "Should have at least 10 grammar lessons seeded.")

            topics = db.execute("SELECT COUNT(*) as count FROM speaking_topics").fetchone()['count']
            self.assertEqual(topics, 4, "Should have exactly 4 speaking topics seeded.")

            vocab = db.execute("SELECT COUNT(*) as count FROM vocabulary").fetchone()['count']
            self.assertGreaterEqual(vocab, 35, "Should have comprehensive vocabulary seeded.")

            listening = db.execute("SELECT COUNT(*) as count FROM listening_exercises").fetchone()['count']
            self.assertGreaterEqual(listening, 4, "Should have listening exercises seeded.")

            achievements = db.execute("SELECT COUNT(*) as count FROM achievements").fetchone()['count']
            self.assertGreaterEqual(achievements, 10, "Should have gamification achievements seeded.")

    # 2. Authentication & Guest Access
    def test_auth_registration_and_login(self):
        # Register
        res = self.client.post('/auth/register', data={
            'username': 'student_visal',
            'email': 'visal@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Welcome to your English Learning Platform', res.data)

        # Check DB password hash
        with self.app.app_context():
            db = get_db()
            u = db.execute("SELECT * FROM users WHERE username = 'student_visal'").fetchone()
            self.assertIsNotNone(u)
            self.assertNotEqual(u['password_hash'], 'password123', "Passwords must never be stored in plain text!")

        # Logout
        res_logout = self.client.get('/auth/logout', follow_redirects=True)
        self.assertIn(b'logged out', res_logout.data)

        # Login
        res_login = self.client.post('/auth/login', data={
            'username': 'student_visal',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Welcome back, student_visal', res_login.data)

    def test_guest_mode(self):
        res = self.client.get('/auth/guest', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Guest Mode', res.data)
        # Dashboard should load without error
        res_dash = self.client.get('/dashboard')
        self.assertEqual(res_dash.status_code, 200)

    # 3. Placement Test Diagnostic
    def test_placement_test_evaluation(self):
        # Register user first
        self.client.get('/auth/guest', follow_redirects=True)
        with self.app.app_context():
            db = get_db()
            u = db.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = u['id']

            # Evaluate with sample answers (some correct, some incorrect)
            sample_answers = {
                "0": "goes",              # Present Simple (correct)
                "1": "don't",             # Present Simple (correct)
                "2": "Does",              # Present Simple (correct)
                "3": "analyses",          # Present Continuous (wrong)
                "4": "do you wear",       # Present Continuous (wrong)
                "5": "organised",         # Past Simple (correct)
            }
            res = evaluate_placement_test(user_id, sample_answers)
            self.assertIn("score", res)
            self.assertIn("level", res)
            self.assertIn("weak_topics", res)
            self.assertIn("strong_topics", res)
            self.assertIn("recommended_path", res)

            # Check that mistakes were logged into mistake notebook
            mistakes = db.execute("SELECT * FROM mistake_notebook WHERE user_id = ?", (user_id,)).fetchall()
            self.assertGreater(len(mistakes), 0, "Incorrect placement answers must be logged in Mistake Notebook.")

    # 4. Spaced Repetition System (SM-2)
    def test_spaced_repetition_logic(self):
        self.client.get('/auth/guest', follow_redirects=True)
        with self.app.app_context():
            db = get_db()
            u = db.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = u['id']
            v = db.execute("SELECT id FROM vocabulary LIMIT 1").fetchone()
            vocab_id = v['id']

            # Rate as "again"
            res1 = record_srs_review(user_id, vocab_id, 'again')
            self.assertEqual(res1['new_interval'], 1)
            self.assertEqual(res1['reps'], 0)

            # Rate as "good"
            res2 = record_srs_review(user_id, vocab_id, 'good')
            self.assertGreaterEqual(res2['new_interval'], 1)
            self.assertEqual(res2['reps'], 1)

            # Rate as "easy"
            res3 = record_srs_review(user_id, vocab_id, 'easy')
            self.assertGreater(res3['new_interval'], res2['new_interval'])

            # Verify stats
            stats = get_vocab_statistics(user_id)
            self.assertGreaterEqual(stats['total_reviews'], 3)

    # 5. Grammar Lessons & Quiz Evaluation
    def test_grammar_quiz_evaluation(self):
        self.client.get('/auth/guest', follow_redirects=True)
        with self.app.app_context():
            db = get_db()
            u = db.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = u['id']
            lesson = db.execute("SELECT id, slug FROM grammar_lessons LIMIT 1").fetchone()

            # Submit quiz
            quiz_items = db.execute("SELECT id, correct_answer FROM grammar_quizzes WHERE lesson_id = ?", (lesson['id'],)).fetchall()
            answers = {q['id']: q['correct_answer'] for q in quiz_items}

            res = evaluate_lesson_quiz(user_id, lesson['id'], answers)
            self.assertEqual(res['percentage'], 100)
            self.assertGreater(res['xp_earned'], 0)

    # 6. Speaking Presentation Workstation
    def test_speaking_submission(self):
        self.client.get('/auth/guest', follow_redirects=True)
        res = self.client.post('/speaking/topic/1/submit', data={
            'presentation_title': 'My Daily English Routine Speech',
            'outline_notes': 'Hook -> Morning Routine -> Passion -> Conclusion',
            'recorded_transcript': 'Good morning everyone. Today I am thrilled to present my daily routine and passions...',
            'duration_seconds': '145',
            'self_rating': '5'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'presentation and transcript have been safely saved', res.data)

        with self.app.app_context():
            db = get_db()
            sub = db.execute("SELECT * FROM speaking_submissions WHERE presentation_title LIKE '%My Daily English Routine%'").fetchone()
            self.assertIsNotNone(sub)
            self.assertEqual(sub['duration_seconds'], 145)
            self.assertIn("benchmark", sub['feedback_notes'].lower())

    # 7. Writing Workshop Analysis Engine
    def test_writing_analysis_engine(self):
        sample_text = "I study English every day. Although it is demanding, but I persevere. Furthermore, learning vocabulary is very good."
        analysis = analyze_writing_text(sample_text)

        self.assertGreaterEqual(analysis['word_count'], 15)
        self.assertGreaterEqual(analysis['sentence_count'], 2)
        # Should flag "although ... but"
        flag_texts = [f['matched_text'].lower() for f in analysis['grammar_flags']]
        self.assertTrue(any('although' in t for t in flag_texts))
        # Should detect "Furthermore"
        self.assertIn("Addition", analysis['linking_words_found'])
        # Should suggest alternative for "very good"
        orig_sug = [s['original'] for s in analysis['vocab_suggestions']]
        self.assertIn("very good", orig_sug)

    # 8. Mistake Notebook & Practice Similar
    def test_mistake_notebook_workflow(self):
        self.client.get('/auth/guest', follow_redirects=True)
        with self.app.app_context():
            db = get_db()
            u = db.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = u['id']

            # Insert an error
            cur = db.execute("""
                INSERT INTO mistake_notebook (user_id, source_module, question_text, student_answer, correct_answer, explanation, grammar_category)
                VALUES (?, 'quiz', 'He _______ to school.', 'go', 'goes', 'Third person singular takes -es', 'Present Simple')
            """, (user_id,))
            mistake_id = cur.lastrowid
            db.commit()

            # Test similar question generator
            drill = generate_practice_question_for_mistake('Present Simple')
            self.assertIn("question", drill)
            self.assertIn("correct_answer", drill)

        # Test Understood Toggle API
        res_toggle = self.client.post(f'/mistakes/{mistake_id}/understood')
        self.assertEqual(res_toggle.status_code, 200)
        data = json.loads(res_toggle.data)
        self.assertEqual(data['is_understood'], 1)

    # 9. Study Planner & Daily Targets
    def test_study_planner(self):
        self.client.get('/auth/guest', follow_redirects=True)
        # Add a task
        res_add = self.client.post('/planner/add', data={
            'plan_date': '2026-11-16',
            'task_type': 'speaking',
            'task_title': 'Deliver Topic 2 3-minute speech'
        }, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)

        with self.app.app_context():
            db = get_db()
            t = db.execute("SELECT id FROM study_planner WHERE task_title LIKE '%Deliver Topic 2%'").fetchone()
            self.assertIsNotNone(t)

        # Toggle completion
        res_toggle = self.client.post(f'/planner/toggle/{t["id"]}')
        self.assertEqual(res_toggle.status_code, 200)
        data = json.loads(res_toggle.data)
        self.assertEqual(data['is_completed'], 1)

    # 10. Data Exports & SQL Backups
    def test_data_exports(self):
        self.client.get('/auth/guest', follow_redirects=True)

        # CSV Vocab
        res_vocab_csv = self.client.get('/backup/export/vocabulary.csv')
        self.assertEqual(res_vocab_csv.status_code, 200)
        self.assertEqual(res_vocab_csv.mimetype, 'text/csv')

        # CSV Mistakes
        res_mistakes_csv = self.client.get('/backup/export/mistakes.csv')
        self.assertEqual(res_mistakes_csv.status_code, 200)
        self.assertEqual(res_mistakes_csv.mimetype, 'text/csv')

        # TXT Speaking
        res_speaking_txt = self.client.get('/backup/export/speaking.txt')
        self.assertEqual(res_speaking_txt.status_code, 200)
        self.assertEqual(res_speaking_txt.mimetype, 'text/plain')

        # JSON Progress
        res_progress_json = self.client.get('/backup/export/progress.json')
        self.assertEqual(res_progress_json.status_code, 200)
        self.assertEqual(res_progress_json.mimetype, 'application/json')

        # SQL Database Backup
        res_sql = self.client.get('/backup/download-db')
        self.assertEqual(res_sql.status_code, 200)
        self.assertIn(b'CREATE TABLE', res_sql.data)

if __name__ == '__main__':
    unittest.main()
