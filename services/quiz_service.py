import json
from datetime import datetime
from database.db import get_db
from database.seed_data import PLACEMENT_QUESTIONS

def get_placement_questions():
    """Returns the standardized placement questions without revealing correct answers."""
    sanitized = []
    for idx, q in enumerate(PLACEMENT_QUESTIONS):
        sanitized.append({
            "id": idx,
            "category": q["category"],
            "question": q["question"],
            "options": q["options"]
        })
    return sanitized

def evaluate_placement_test(user_id, submitted_answers):
    """
    Evaluates placement test submissions.
    submitted_answers: dict of {question_index: selected_option}
    Returns diagnostic analysis and saves results to database.
    """
    db = get_db()
    total_questions = len(PLACEMENT_QUESTIONS)
    total_correct = 0
    category_stats = {}
    detailed_results = []
    
    for idx, q in enumerate(PLACEMENT_QUESTIONS):
        cat = q["category"]
        if cat not in category_stats:
            category_stats[cat] = {"correct": 0, "total": 0}
        category_stats[cat]["total"] += 1
        
        selected = str(submitted_answers.get(str(idx), submitted_answers.get(idx, ""))).strip()
        is_correct = (selected == q["correct_answer"])
        
        if is_correct:
            total_correct += 1
            category_stats[cat]["correct"] += 1
        else:
            # Record into Mistake Notebook
            db.execute("""
                INSERT INTO mistake_notebook (user_id, source_module, question_text, student_answer, correct_answer, explanation, grammar_category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, 'placement', q['question'], selected or '(No answer)', q['correct_answer'], q['explanation'], cat))
        
        detailed_results.append({
            "index": idx + 1,
            "category": cat,
            "question": q["question"],
            "selected": selected,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    # Calculate percentage
    pct = round((total_correct / total_questions) * 100, 1) if total_questions > 0 else 0
    
    # CEFR Level Estimation (with educational guidance disclaimer)
    if pct < 35:
        level = "Beginner (A1)"
        level_desc = "Building foundational sentence structures and elementary everyday expressions."
    elif pct < 55:
        level = "Elementary (A2)"
        level_desc = "Grasping routine communications, basic past tenses, and everyday descriptive language."
    elif pct < 75:
        level = "Intermediate (B1)"
        level_desc = "Forming cohesive multi-clause sentences, expressing plans, advice, and opinions comfortably."
    else:
        level = "Upper-Intermediate (B2)"
        level_desc = "High degree of fluency and grammatical precision; ready to tackle nuanced debates and complex presentation topics."

    # Identify Weak & Strong topics
    weak_topics = []
    strong_topics = []
    category_breakdown = {}
    
    for cat, stats in category_stats.items():
        cat_pct = round((stats["correct"] / stats["total"]) * 100) if stats["total"] > 0 else 0
        category_breakdown[cat] = {
            "correct": stats["correct"],
            "total": stats["total"],
            "percentage": cat_pct
        }
        if cat_pct < 65:
            weak_topics.append(cat)
        else:
            strong_topics.append(cat)

    # Lesson recommendations & personalized learning path
    recommended_path = []
    for wt in weak_topics:
        # Match with grammar lesson
        cur = db.execute("SELECT id, slug, title, cefr_level FROM grammar_lessons WHERE category LIKE ?", (f"%{wt}%",))
        lesson = cur.fetchone()
        if lesson:
            recommended_path.append({
                "type": "Grammar Lesson",
                "title": lesson["title"],
                "slug": lesson["slug"],
                "reason": f"Strengthen your understanding of {wt}"
            })
            
    # Always include Speaking & Vocabulary in recommended path
    recommended_path.append({
        "type": "Speaking Module",
        "title": "Topic 1: Personal Background & Daily Routine",
        "slug": "topic-1",
        "reason": "Apply grammatical structures in an oral presentation"
    })
    recommended_path.append({
        "type": "Vocabulary Revision",
        "title": "Spaced Repetition Daily Deck",
        "slug": "spaced-repetition",
        "reason": "Expand active lexical repertoire with Khmer translations"
    })

    # Save to database
    cursor = db.execute("""
        INSERT INTO placement_tests (user_id, total_score, max_score, level_assessment, grammar_breakdown, weak_topics, strong_topics, recommended_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, total_correct, total_questions, level,
        json.dumps(category_breakdown), json.dumps(weak_topics),
        json.dumps(strong_topics), json.dumps(recommended_path)
    ))
    test_id = cursor.lastrowid
    
    # Award XP (50 XP for completing placement test)
    from services.progress_service import award_xp
    award_xp(user_id, 50, "Completed English Placement Diagnostic")
    
    db.commit()
    
    return {
        "test_id": test_id,
        "score": total_correct,
        "max_score": total_questions,
        "percentage": pct,
        "level": level,
        "level_desc": level_desc,
        "category_breakdown": category_breakdown,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "recommended_path": recommended_path,
        "detailed_results": detailed_results
    }

def evaluate_lesson_quiz(user_id, lesson_id, answers):
    """
    Evaluates an interactive grammar quiz for a specific lesson.
    answers: dict {quiz_id: selected_option}
    """
    db = get_db()
    cur = db.execute("SELECT * FROM grammar_quizzes WHERE lesson_id = ?", (lesson_id,))
    quizzes = cur.fetchall()
    
    total = len(quizzes)
    correct_count = 0
    results = []
    
    for q in quizzes:
        qid = q["id"]
        selected = str(answers.get(str(qid), answers.get(qid, ""))).strip()
        is_correct = (selected == q["correct_answer"])
        
        if is_correct:
            correct_count += 1
        else:
            # Log in Mistake Notebook
            db.execute("""
                INSERT INTO mistake_notebook (user_id, source_module, question_text, student_answer, correct_answer, explanation, grammar_category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, 'grammar_quiz', q['question'], selected or '(No answer)', q['correct_answer'], q['explanation'], q['category']))
            
        # Log quiz attempt
        db.execute("""
            INSERT INTO quiz_attempts (user_id, lesson_id, quiz_id, selected_answer, is_correct, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, lesson_id, qid, selected, 1 if is_correct else 0, q['category']))
        
        results.append({
            "quiz_id": qid,
            "question": q["question"],
            "selected": selected,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    score_pct = round((correct_count / total) * 100) if total > 0 else 0
    xp_earned = correct_count * 10
    
    from services.progress_service import award_xp
    award_xp(user_id, xp_earned, f"Grammar Quiz - Lesson #{lesson_id}")
    
    db.commit()
    
    return {
        "total": total,
        "correct": correct_count,
        "percentage": score_pct,
        "xp_earned": xp_earned,
        "results": results
    }
