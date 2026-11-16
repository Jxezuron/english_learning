import re
import json

LINKING_WORDS_TAXONOMY = {
    "Addition": ["furthermore", "moreover", "in addition", "additionally", "besides", "also", "not only"],
    "Contrast": ["however", "although", "even though", "on the other hand", "in contrast", "nevertheless", "yet", "whereas", "despite"],
    "Cause & Effect": ["because", "therefore", "consequently", "as a result", "since", "thus", "hence"],
    "Conclusion & Summary": ["in conclusion", "to summarize", "to sum up", "all in all", "ultimately", "in short"],
    "Sequence & Order": ["first of all", "firstly", "secondly", "thirdly", "subsequently", "meanwhile", "finally"]
}

VOCAB_ENHANCEMENT_MAP = {
    "very good": ["exceptional", "outstanding", "superb", "commendable"],
    "good": ["beneficial", "valuable", "effective", "advantageous"],
    "very bad": ["detrimental", "dreadful", "adverse", "regrettable"],
    "bad": ["unfavorable", "flawed", "substandard"],
    "very big": ["monumental", "immense", "substantial", "colossal"],
    "big": ["considerable", "significant", "substantial"],
    "very important": ["paramount", "critical", "indispensable", "vital"],
    "important": ["crucial", "essential", "significant"],
    "very happy": ["ecstatic", "delighted", "thrilled", "jubilant"],
    "happy": ["content", "satisfied", "cheerful"],
    "very sad": ["devastated", "heartbroken", "melancholy"],
    "interesting": ["captivating", "intriguing", "compelling", "thought-provoking"],
    "a lot of": ["a multitude of", "numerous", "an abundance of", "substantial amounts of"],
    "very hard": ["demanding", "formidable", "arduous", "strenuous"],
    "help": ["assist", "facilitate", "support", "collaborate"]
}

ESL_COMMON_MISTAKES_PATTERNS = [
    (r"\b(he|she|it)\s+(go|do|have|say|make|come|know|think|take|see|want|look|use|find|give|tell)\b", 
     "Subject-verb agreement: third-person singular (he/she/it) usually requires -s/-es on present simple verbs (e.g., 'he goes', 'she has')."),
    (r"\b(he|she|it)\s+don't\b", 
     "Subject-verb agreement: use 'doesn't' instead of 'don't' with he/she/it."),
    (r"\b(they|we|you)\s+doesn't\b", 
     "Subject-verb agreement: use 'don't' instead of 'doesn't' with plural subjects / you / we / they."),
    (r"\b(i)\s+is\b", 
     "Pronoun agreement: use 'I am' instead of 'I is'."),
    (r"\b(they|we|you)\s+is\b", 
     "Subject-verb agreement: use 'are' instead of 'is' with plural subjects / you / we / they."),
    (r"\b(he|she|it)\s+are\b", 
     "Subject-verb agreement: use 'is' instead of 'are' with singular third-person subjects."),
    (r"\b(did|didn't|does|doesn't|do|don't)\s+(\w+ed|\w+s)\b", 
     "Auxiliary verb rule: after 'did/didn't/does/doesn't', the main verb must remain in the base form (bare infinitive)."),
    (r"\b(should|can|could|may|might|must|will|would)\s+to\s+(\w+)\b", 
     "Modal verb rule: do not place 'to' after modal verbs (say 'should study', not 'should to study')."),
    (r"\bmore\s+(\w+er)\b", 
     "Double comparative: avoid using 'more' together with an '-er' adjective (e.g. say 'easier', not 'more easier')."),
    (r"\b(the\s+the|a\s+a|an\s+an|in\s+in|to\s+to|of\s+of)\b", 
     "Word repetition: you have accidentally typed the same word twice consecutively."),
    (r"\b(although|even though)\s+(.+?)\s+but\b", 
     "Conjunction conflict: do not use 'although' and 'but' together to link the same clauses.")
]

def analyze_writing_text(text):
    """
    Performs pedagogical linguistic analysis on student's writing.
    Returns:
      - metrics: word count, sentence count, avg words per sentence
      - checklist: capitalization, sentence punctuation, spacing
      - grammar_flags: identified common ESL errors with explanations
      - linking_words_used: categorised list of detected transition markers
      - linking_words_missing: categories that need more development
      - vocab_suggestions: advanced alternatives for simplistic/repetitive words
      - corrected_preview: helpful annotated hints
    """
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "avg_words_per_sentence": 0,
            "checklist": [],
            "grammar_flags": [],
            "linking_words_found": {},
            "linking_suggestions": list(LINKING_WORDS_TAXONOMY.keys()),
            "vocab_suggestions": []
        }

    # 1. Basic counts
    words = re.findall(r"\b[A-Za-z0-9'-]+\b", cleaned_text)
    word_count = len(words)
    
    # Sentences split by . ! ?
    raw_sentences = [s.strip() for s in re.split(r'[.!?]+', cleaned_text) if s.strip()]
    sentence_count = max(1, len(raw_sentences))
    
    paragraphs = [p for p in cleaned_text.split('\n') if p.strip()]
    paragraph_count = max(1, len(paragraphs))
    
    avg_words = round(word_count / sentence_count, 1)

    # 2. Grammar & Mechanical Checklist
    checklist = []
    
    # Check capital letter at beginning
    starts_capital = cleaned_text[0].isupper()
    checklist.append({
        "item": "Beginning capitalization",
        "passed": starts_capital,
        "detail": "Passage begins with a proper uppercase character." if starts_capital else "Remember to capitalize the very first letter of your paragraph."
    })
    
    # Check ending punctuation
    has_end_punct = cleaned_text[-1] in ('.', '!', '?')
    checklist.append({
        "item": "Sentence terminal punctuation",
        "passed": has_end_punct,
        "detail": "Passage ends with appropriate concluding punctuation (. ! ?)." if has_end_punct else "Remember to conclude your final sentence with a period (.), exclamation (!), or question mark (?)."
    })
    
    # Check lowercase "i" as standalone pronoun
    standalone_i = re.search(r'\bi\b', cleaned_text)
    checklist.append({
        "item": "First-person pronoun 'I'",
        "passed": not standalone_i,
        "detail": "Properly capitalized 'I'." if not standalone_i else "Found standalone lowercase 'i'. In English, the pronoun 'I' is always capitalized."
    })

    # Sentence length balance
    length_balanced = (8 <= avg_words <= 25)
    checklist.append({
        "item": "Sentence length balance",
        "passed": length_balanced,
        "detail": f"Average sentence length is {avg_words} words (ideal is 12–20 words)." if length_balanced else f"Average sentence length is {avg_words} words. Aim for 12–20 words to avoid overly short or run-on sentences."
    })

    # 3. Common ESL Grammar Pattern Flags
    grammar_flags = []
    for pattern, explanation in ESL_COMMON_MISTAKES_PATTERNS:
        match = re.search(pattern, cleaned_text, re.IGNORECASE)
        if match:
            matched_phrase = match.group(0)
            grammar_flags.append({
                "matched_text": matched_phrase,
                "explanation": explanation
            })

    # 4. Linking Word Detection
    lower_text = cleaned_text.lower()
    linking_words_found = {}
    for category, connectors in LINKING_WORDS_TAXONOMY.items():
        found = []
        for c in connectors:
            # Match boundary for phrase
            if re.search(rf"\b{re.escape(c)}\b", lower_text):
                found.append(c)
        if found:
            linking_words_found[category] = found

    missing_categories = [cat for cat in LINKING_WORDS_TAXONOMY.keys() if cat not in linking_words_found]

    # 5. Vocabulary Suggestions
    vocab_suggestions = []
    for basic_word, alternatives in VOCAB_ENHANCEMENT_MAP.items():
        if re.search(rf"\b{re.escape(basic_word)}\b", lower_text):
            vocab_suggestions.append({
                "original": basic_word,
                "alternatives": alternatives,
                "advice": f"Consider upgrading '{basic_word}' to more expressive vocabulary: {', '.join(alternatives[:3])}."
            })

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_words_per_sentence": avg_words,
        "checklist": checklist,
        "grammar_flags": grammar_flags,
        "linking_words_found": linking_words_found,
        "linking_suggestions": missing_categories,
        "vocab_suggestions": vocab_suggestions
    }

def generate_practice_question_for_mistake(grammar_category):
    """
    Generates a targeted drill question matching the grammar category
    of an error in the student's mistake notebook.
    """
    category_drills = {
        "Present Simple": {
            "question": "Sokunthea _______ (read) three English articles every morning before breakfast.",
            "options": ["reads", "read", "is reading", "reading"],
            "correct_answer": "reads",
            "explanation": "Third-person singular subject (Sokunthea) takes '-s' in the Present Simple."
        },
        "Present Continuous": {
            "question": "Be quiet please! The professor _______ (deliver) the lecture right now.",
            "options": ["is delivering", "delivers", "delivered", "are delivering"],
            "correct_answer": "is delivering",
            "explanation": "The cue 'right now' indicates an ongoing action requiring the Present Continuous."
        },
        "Past Simple": {
            "question": "Last month, they _______ (complete) the community language project.",
            "options": ["completed", "complete", "did completed", "were completing"],
            "correct_answer": "completed",
            "explanation": "'Last month' indicates a completed past event requiring regular past tense '-ed'."
        },
        "Present Perfect": {
            "question": "Vannak _______ (not see) that new English movie yet.",
            "options": ["hasn't seen", "didn't see", "hadn't saw", "haven't seen"],
            "correct_answer": "hasn't seen",
            "explanation": "With third-person singular and the time marker 'yet', use 'hasn't + past participle (seen)'."
        },
        "Comparative and superlative adjectives": {
            "question": "This second vocabulary exercise is _______ (challenging) than the previous one.",
            "options": ["more challenging", "challenginger", "the most challenging", "most challenging"],
            "correct_answer": "more challenging",
            "explanation": "Multi-syllable adjectives form comparatives with 'more + adjective + than'."
        },
        "Be going to": {
            "question": "Look at the dark clouds! It _______ (rain) in a few minutes.",
            "options": ["is going to rain", "will rain to", "is raining to", "goes to rain"],
            "correct_answer": "is going to rain",
            "explanation": "Predictions based on visible present evidence use 'be going to'."
        },
        "Should": {
            "question": "You _______ (practice) speaking out loud if you want to improve oral fluency.",
            "options": ["should practice", "should to practice", "should practicing", "must to practice"],
            "correct_answer": "should practice",
            "explanation": "Modal verbs like 'should' are immediately followed by the bare infinitive (no 'to')."
        },
        "Linking words": {
            "question": "He was exhausted; _______, he persevered and completed his presentation.",
            "options": ["nevertheless", "furthermore", "because", "in addition"],
            "correct_answer": "nevertheless",
            "explanation": "'Nevertheless' is a cohesive transition showing contrast with the preceding clause."
        }
    }
    
    # Return matched drill or default
    for cat, drill in category_drills.items():
        if cat.lower() in grammar_category.lower():
            return drill
            
    return category_drills["Present Simple"]
