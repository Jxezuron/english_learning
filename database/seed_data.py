import json
from .db import get_db

GRAMMAR_LESSONS = [
    {
        "slug": "present-simple",
        "title": "Present Simple Tense",
        "category": "Present Simple",
        "cefr_level": "A1",
        "order_index": 1,
        "summary": "Express routines, daily habits, permanent situations, and universal truths.",
        "formula": "Affirmative: Subject + Verb(s/es) | Negative: Subject + do/does not + Base Verb | Question: Do/Does + Subject + Base Verb?",
        "explanation_markdown": """### Understanding the Present Simple
The Present Simple is the foundation of English communication. We use it to talk about:
1. **Daily Habits and Routines**: Things you do repeatedly (e.g., *I drink coffee every morning*).
2. **Permanent Situations**: States that do not change often (e.g., *She lives in Phnom Penh*).
3. **General Truths and Facts**: Scientific laws or established facts (e.g., *Water boils at 100°C*).
4. **Timetables and Schedules**: Scheduled events (e.g., *The train departs at 8:00 AM*).

#### The 3rd Person Singular Rule (he / she / it):
- Most verbs: add **-s** (*work -> works, speak -> speaks*).
- Verbs ending in -ch, -sh, -s, -x, -z, -o: add **-es** (*watch -> watches, go -> goes*).
- Verbs ending in consonant + y: change y to **-ies** (*study -> studies*).""",
        "examples_json": json.dumps([
            {"en": "I study English every day at 7:00 PM.", "km": "ខ្ញុំរៀនភាសាអង់គ្លេសជារៀងរាល់ថ្ងៃនៅម៉ោង ៧:០០ យប់។", "note": "Daily routine with adverb of frequency"},
            {"en": "She works at an international school.", "km": "នាងធ្វើការនៅសាលាអន្តរជាតិមួយ។", "note": "Third-person singular +s"},
            {"en": "They do not live in the city center.", "km": "ពួកគេមិនរស់នៅក្នុងកណ្តាលទីក្រុងទេ។", "note": "Negative form using 'do not'"},
            {"en": "Does your brother speak French?", "km": "តើបងប្រុសរបស់អ្នកចេះនិយាយភាសាបារាំងទេ?", "note": "Question form using 'Does'"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "He go to school by bicycle.", "correct": "He goes to school by bicycle.", "reason": "Third-person singular (he/she/it) requires 'goes' instead of 'go'."},
            {"wrong": "She doesn't likes spicy food.", "correct": "She doesn't like spicy food.", "reason": "After auxiliary 'does/doesn't', the main verb must remain in the base form."},
            {"wrong": "I am agree with your opinion.", "correct": "I agree with your opinion.", "reason": "'Agree' is already a verb in English; do not combine with 'am'."}
        ]),
        "tips": "Always look for time markers like: always, usually, often, sometimes, never, every Monday, twice a year.",
        "quizzes": [
            {
                "question": "My father _______ the morning news on TV every morning.",
                "options": ["watch", "watches", "is watching", "watched"],
                "correct_answer": "watches",
                "explanation": "Because 'My father' is singular (he), the verb ending in 'ch' takes '-es': 'watches'."
            },
            {
                "question": "Sophea _______ coffee; she always drinks green tea.",
                "options": ["doesn't like", "don't like", "isn't like", "no likes"],
                "correct_answer": "doesn't like",
                "explanation": "With third-person singular (Sophea = she), we use 'doesn't + base verb'."
            },
            {
                "question": "_______ you usually take notes during the English lecture?",
                "options": ["Do", "Does", "Are", "Have"],
                "correct_answer": "Do",
                "explanation": "With the pronoun 'you', the question auxiliary is 'Do'."
            },
            {
                "question": "Choose the grammatically correct sentence:",
                "options": [
                    "The Earth revolves around the Sun.",
                    "The Earth revolve around the Sun.",
                    "The Earth is revolving around the Sun always.",
                    "The Earth revolves around Sun."
                ],
                "correct_answer": "The Earth revolves around the Sun.",
                "explanation": "Universal scientific facts use the Present Simple with 3rd person singular '-s' and definite article 'the Sun'."
            }
        ]
    },
    {
        "slug": "present-continuous",
        "title": "Present Continuous Tense",
        "category": "Present Continuous",
        "cefr_level": "A1",
        "order_index": 2,
        "summary": "Describe actions happening right now, temporary situations, or gradual changes.",
        "formula": "Affirmative: Subject + am/is/are + Verb-ing | Negative: Subject + am/is/are not + Verb-ing | Question: Am/Is/Are + Subject + Verb-ing?",
        "explanation_markdown": """### Understanding the Present Continuous
The Present Continuous focuses on actions that are in progress at or around the time of speaking.
1. **Actions happening right now**: *Be quiet! The baby is sleeping.*
2. **Temporary situations**: *I am living with my aunt while my house is being painted.*
3. **Current trends or changing states**: *The climate is getting warmer every year.*

#### Stative Verbs Warning:
Verbs of state, emotion, and possession are rarely used in the continuous form:
*love, hate, like, understand, believe, know, want, belong, need.*
- Say: *I know the answer.* (NOT: *I am knowing the answer.*)""",
        "examples_json": json.dumps([
            {"en": "Look! The students are practicing their English presentations.", "km": "មើលហ្ន៎! សិស្សានុសិស្សកំពុងអនុវត្តការធ្វើបទបង្ហាញភាសាអង់គ្លេសរបស់ពួកគេ។", "note": "Action happening at this moment"},
            {"en": "She is preparing dinner in the kitchen right now.", "km": "នាងកំពុងរៀបចំអាហារពេលល្ងាចនៅក្នុងផ្ទះបាយឥឡូវនេះ។", "note": "In-progress activity"},
            {"en": "We are currently developing a new mobile app.", "km": "បច្ចុប្បន្នយើងកំពុងអភិវឌ្ឍកម្មវិធីទូរស័ព្ទដៃថ្មីមួយ។", "note": "Temporary ongoing project"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "I am having two smartphones.", "correct": "I have two smartphones.", "reason": "Possession is stative; use present simple 'have'."},
            {"wrong": "Listen! Somebody knocks at the door.", "correct": "Listen! Somebody is knocking at the door.", "reason": "The cue 'Listen!' indicates an action occurring right now."}
        ]),
        "tips": "Keywords: now, right now, at the moment, currently, Look!, Listen!",
        "quizzes": [
            {
                "question": "Listen! The teacher _______ an important rule.",
                "options": ["explains", "is explaining", "are explaining", "explained"],
                "correct_answer": "is explaining",
                "explanation": "'Listen!' alerts us that the action is happening at the moment of speech, requiring 'is explaining'."
            },
            {
                "question": "I _______ this complex grammar point right now.",
                "options": ["am not understanding", "don't understand", "doesn't understand", "not understand"],
                "correct_answer": "don't understand",
                "explanation": "'Understand' is a stative verb expressing a cognitive state, so it uses the simple tense even with 'right now'."
            },
            {
                "question": "Why _______ your winter jacket today? It is very hot outside!",
                "options": ["are you wearing", "do you wear", "you are wearing", "wear you"],
                "correct_answer": "are you wearing",
                "explanation": "Question order for continuous: Why + auxiliary (are) + subject (you) + verb-ing (wearing)?"
            }
        ]
    },
    {
        "slug": "past-simple",
        "title": "Past Simple Tense",
        "category": "Past Simple",
        "cefr_level": "A2",
        "order_index": 3,
        "summary": "Talk about completed actions, past events, and past habits with specific time markers.",
        "formula": "Affirmative: Subject + Verb(past / -ed) | Negative: Subject + did not + Base Verb | Question: Did + Subject + Base Verb?",
        "explanation_markdown": """### Mastering the Past Simple
The Past Simple describes actions that began and finished in the past at a definite time.

#### Regular vs. Irregular Verbs:
1. **Regular Verbs (+ed)**:
   - *visit -> visited*
   - *study -> studied*
   - *stop -> stopped*
2. **Irregular Verbs (must be memorized)**:
   - *go -> went*
   - *buy -> bought*
   - *speak -> spoke*
   - *write -> wrote*

#### Key Rule for Negatives & Questions:
Use **did** or **didn't** with the **BASE FORM** of the verb:
- *I visited Siem Reap.* -> *I didn't visit Siem Reap.* (NOT: *didn't visited*)
- *Did you see the temple?* (NOT: *Did you saw*)""",
        "examples_json": json.dumps([
            {"en": "Yesterday, we visited Angkor Wat at sunrise.", "km": "កាលពីម្សិលមិញ យើងបានទៅទស្សនាប្រាសាទអង្គរវត្តនៅពេលព្រះអាទិត្យរះ។", "note": "Finished action at a definite past time"},
            {"en": "She didn't attend the seminar last Friday.", "km": "នាងមិនបានចូលរួមសិក្ខាសាលាកាលពីថ្ងៃសុក្រមុនទេ។", "note": "Negative using 'didn't + base verb'"},
            {"en": "Where did you buy that comprehensive grammar book?", "km": "តើអ្នកបានទិញសៀវភៅវេយ្យាករណ៍ដ៏ក្បោះក្បាយនោះនៅឯណា?", "note": "Question using 'did + base verb'"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "She didn't went to the market yesterday.", "correct": "She didn't go to the market yesterday.", "reason": "After 'didn't', the main verb must always be in base form (go)."},
            {"wrong": "Did you saw the news?", "correct": "Did you see the news?", "reason": "After 'did', use the base verb 'see'."}
        ]),
        "tips": "Time markers: yesterday, last week, 3 days ago, in 2022, when I was young.",
        "quizzes": [
            {
                "question": "Two days ago, Visal _______ an impressive presentation to the management board.",
                "options": ["delivers", "delivered", "was deliver", "is delivering"],
                "correct_answer": "delivered",
                "explanation": "'Two days ago' signals a completed past event. The regular past simple is 'delivered'."
            },
            {
                "question": "We _______ to the cinema last night because we were exhausted.",
                "options": ["didn't went", "didn't go", "weren't go", "not went"],
                "correct_answer": "didn't go",
                "explanation": "Past simple negative requires 'didn't' followed by the base verb 'go'."
            },
            {
                "question": "What time _______ you wake up yesterday morning?",
                "options": ["did", "do", "were", "had"],
                "correct_answer": "did",
                "explanation": "The auxiliary verb for past simple questions is 'did'."
            }
        ]
    },
    {
        "slug": "present-perfect",
        "title": "Present Perfect Tense",
        "category": "Present Perfect",
        "cefr_level": "B1",
        "order_index": 4,
        "summary": "Connect past actions with the present: life experiences, recent events, and unfinished time.",
        "formula": "Affirmative: Subject + have/has + Past Participle (V3) | Negative: Subject + have/has not + V3 | Question: Have/Has + Subject + V3?",
        "explanation_markdown": """### Understanding the Present Perfect
The Present Perfect connects the past with the present moment. Unlike the Past Simple, the exact time is NOT specified or the period is still ongoing.

#### Key Uses:
1. **Life Experiences (Ever / Never)**:
   - *I have visited three European countries.* (In my life so far)
2. **Actions with a Result in the Present**:
   - *I have lost my key.* (Result: I cannot enter my room right now)
3. **Recent Events with Just / Already / Yet**:
   - *She has just finished her exam.*
   - *Have you eaten lunch yet?*
4. **Continuing Situations with Since / For**:
   - *For* + period of duration: *for five years, for two hours.*
   - *Since* + starting point: *since 2018, since 8:00 AM.*""",
        "examples_json": json.dumps([
            {"en": "I have lived in this welcoming community for seven years.", "km": "ខ្ញុំបានរស់នៅក្នុងសហគមន៍ដ៏កក់ក្តៅនេះអស់រយៈពេល ៧ ឆ្នាំមកហើយ។", "note": "Started in the past and continues now (for + duration)"},
            {"en": "She has already submitted her research proposal.", "km": "នាងបានដាក់សំណើស្រាវជ្រាវរបស់នាងរួចរាល់ហើយ។", "note": "Completed earlier than expected with 'already'"},
            {"en": "Have you ever spoken in front of a large audience?", "km": "តើអ្នកធ្លាប់និយាយនៅចំពោះមុខទស្សនិកជនច្រើនដែរឬទេ?", "note": "Life experience question with 'ever'"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "I have seen that movie yesterday.", "correct": "I saw that movie yesterday.", "reason": "Never use Present Perfect with specific past time indicators like 'yesterday' or 'last year'."},
            {"wrong": "She has lived here since five years.", "correct": "She has lived here for five years.", "reason": "Use 'for' with duration (five years) and 'since' with a specific point in time."}
        ]),
        "tips": "Use 'since' for starting points (since Monday, since 2020) and 'for' for spans of time (for 3 months, for 10 years).",
        "quizzes": [
            {
                "question": "Sina _______ in Siem Reap since she graduated from university.",
                "options": ["has lived", "lives", "lived", "is living"],
                "correct_answer": "has lived",
                "explanation": "'Since + past event' indicates an action that started in the past and continues into the present, requiring the Present Perfect: 'has lived'."
            },
            {
                "question": "Have you completed your writing assignment _______?",
                "options": ["already", "yet", "since", "just"],
                "correct_answer": "yet",
                "explanation": "In questions asking whether something has happened up to the present, 'yet' is used at the end."
            },
            {
                "question": "Which sentence is grammatically correct?",
                "options": [
                    "I have visited Singapore last December.",
                    "I visited Singapore last December.",
                    "I have visit Singapore last December.",
                    "I was visiting Singapore last December once."
                ],
                "correct_answer": "I visited Singapore last December.",
                "explanation": "Because 'last December' is a specific completed past time, the Past Simple 'visited' must be used."
            }
        ]
    },
    {
        "slug": "comparative-superlative",
        "title": "Comparative and Superlative Adjectives",
        "category": "Comparative and superlative adjectives",
        "cefr_level": "A2",
        "order_index": 5,
        "summary": "Compare two or more people, objects, places, or abstract concepts with precision.",
        "formula": "Comparative: Short Adj + -er than / more + Long Adj + than | Superlative: the + Short Adj + -est / the most + Long Adj",
        "explanation_markdown": """### Comparatives vs. Superlatives
- **Comparatives**: Compare **two** entities (*A is taller than B*).
- **Superlatives**: Compare **one entity against a whole group** of three or more (*A is the tallest in the class*).

#### Rules by Syllable Count:
1. **One syllable**: Add *-er / -est*
   - *fast -> faster than -> the fastest*
   - *large -> larger than -> the largest*
2. **Two syllables ending in -y**: Change -y to *-ier / -iest*
   - *easy -> easier than -> the easiest*
   - *busy -> busier than -> the busiest*
3. **Two or more syllables**: Use *more / the most*
   - *fluent -> more fluent than -> the most fluent*
   - *expensive -> more expensive than -> the most expensive*
4. **Irregular Adjectives (crucial to memorize)**:
   - *good -> better -> the best*
   - *bad -> worse -> the worst*
   - *far -> farther/further -> the farthest/furthest*""",
        "examples_json": json.dumps([
            {"en": "Public transport is much cheaper than driving a car.", "km": "ការធ្វើដំណើរសាធារណៈមានតម្លៃថោកជាងការបើកបររថយន្តយ៉ាងខ្លាំង។", "note": "Comparative with short adjective + -er"},
            {"en": "English is one of the most widely spoken languages in the world.", "km": "ភាសាអង់គ្លេសគឺជាភាសាមួយក្នុងចំណោមភាសាដែលត្រូវបានគេនិយាយយ៉ាងទូលំទូលាយបំផុតនៅក្នុងពិភពលោក។", "note": "Superlative with 'the most'"},
            {"en": "Today's speaking practice was significantly better than yesterday's.", "km": "ការអនុវត្តនិយាយថ្ងៃនេះគឺប្រសើរជាងកាលពីម្សិលមិញគួរឱ្យកត់សម្គាល់។", "note": "Irregular comparative: better"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "This exercise is more easier than the last one.", "correct": "This exercise is easier than the last one.", "reason": "Double comparative: do not use 'more' with '-er'."},
            {"wrong": "She is the most smart student.", "correct": "She is the smartest student.", "reason": "One-syllable adjectives take '-est', not 'most'."}
        ]),
        "tips": "Never say 'more better' or 'most easiest'. Remember 'good -> better -> the best' and 'bad -> worse -> the worst'.",
        "quizzes": [
            {
                "question": "Mount Everest is _______ mountain on our planet.",
                "options": ["the highest", "higher", "the most high", "highest"],
                "correct_answer": "the highest",
                "explanation": "Comparing Mount Everest against all mountains requires the superlative 'the highest'."
            },
            {
                "question": "Learning English vocabulary through spaced repetition is _______ than memorizing random lists.",
                "options": ["more effective", "effectiver", "the most effective", "most effective"],
                "correct_answer": "more effective",
                "explanation": "'Effective' has three syllables, so the comparative form is 'more effective than'."
            },
            {
                "question": "My second essay was much _______ than my first attempt.",
                "options": ["better", "gooder", "more good", "more better"],
                "correct_answer": "better",
                "explanation": "'Good' is irregular: good -> better -> the best."
            }
        ]
    },
    {
        "slug": "be-going-to",
        "title": "Future with 'Be Going To'",
        "category": "Be going to",
        "cefr_level": "A2",
        "order_index": 6,
        "summary": "Express pre-meditated plans, intentions, and predictions based on present physical evidence.",
        "formula": "Affirmative: Subject + am/is/are + going to + Base Verb | Negative: Subject + am/is/are not + going to + Base Verb",
        "explanation_markdown": """### When to Use 'Be Going To'
1. **Prior Intentions and Decisions**:
   Decisions made **before** the moment of speaking (a plan already formed):
   - *I am going to take the IELTS examination in November.*
2. **Predictions Based on Present Evidence**:
   When you can see, hear, or feel evidence right now that something is about to happen:
   - *Look at those dark storm clouds! It is going to rain.*
   - *Watch out! That ladder is going to collapse!*

#### Difference between 'Will' and 'Be Going To':
- **Will**: Spontaneous, instant decisions made right now (*The phone is ringing. I will answer it!*).
- **Be Going To**: Planned intentions (*I am going to visit my grandmother this weekend.*).""",
        "examples_json": json.dumps([
            {"en": "We are going to start our own tech startup next year.", "km": "យើងនឹងចាប់ផ្តើមអាជីវកម្មបច្ចេកវិទ្យាផ្ទាល់ខ្លួនរបស់យើងនៅឆ្នាំក្រោយ។", "note": "Pre-meditated plan/intention"},
            {"en": "Look at the dark clouds gathering; it is going to pour down.", "km": "មើលពពកខ្មៅដែលកំពុងប្រមូលផ្តុំចុះ វានឹងមានភ្លៀងធ្លាក់ខ្លាំងមិនខាន។", "note": "Prediction based on immediate visual evidence"},
            {"en": "Are you going to practice speaking for two hours this evening?", "km": "តើអ្នកនឹងអនុវត្តការនិយាយរយៈពេលពីរម៉ោងនៅល្ងាចនេះឬ?", "note": "Question about intention"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "She is going to visits her doctor.", "correct": "She is going to visit her doctor.", "reason": "After 'be going to', always use the base form of the verb."},
            {"wrong": "I going to learn Spanish.", "correct": "I am going to learn Spanish.", "reason": "Do not omit the auxiliary 'be' (am/is/are)."}
        ]),
        "tips": "Always remember the full structure: [am / is / are] + going to + [base verb].",
        "quizzes": [
            {
                "question": "Be careful! You _______ drop that heavy glass vase!",
                "options": ["are going to", "will to", "go to", "are going"],
                "correct_answer": "are going to",
                "explanation": "A prediction based on immediate physical evidence uses 'be going to': 'are going to'."
            },
            {
                "question": "Dara has saved money for months. He _______ a new laptop next week.",
                "options": ["is going to purchase", "will purchasing", "purchases", "is purchase"],
                "correct_answer": "is going to purchase",
                "explanation": "Because Dara planned this in advance (saving money for months), 'is going to purchase' is the correct expression of intention."
            }
        ]
    },
    {
        "slug": "modal-should",
        "title": "Modal Verb: Should",
        "category": "Should",
        "cefr_level": "A2",
        "order_index": 7,
        "summary": "Give recommendations, express opinions, suggest best courses of action, and state mild obligations.",
        "formula": "Affirmative: Subject + should + Base Verb | Negative: Subject + should not (shouldn't) + Base Verb | Question: Should + Subject + Base Verb?",
        "explanation_markdown": """### Using the Modal 'Should'
'Should' is used to express advice, suggestions, and what is desirable or correct.

#### Primary Functions:
1. **Giving Advice / Recommendations**:
   - *You should review your vocabulary cards every single day.*
   - *You look tired; you should take a 15-minute break.*
2. **Asking for Advice**:
   - *Should I choose topic 1 or topic 3 for my speaking presentation?*
3. **Expectation (what is probable)**:
   - *The bus should arrive in five minutes.*

#### Important Structural Rule:
Modal verbs are **never** followed by 'to' and never change form for he/she/it:
- *He should study.* (NOT: *He shoulds study* or *He should to study*).""",
        "examples_json": json.dumps([
            {"en": "Language learners should listen to English podcasts regularly.", "km": "អ្នករៀនភាសាគួរតែស្តាប់ផតខាសភាសាអង់គ្លេសឱ្យបានទៀងទាត់។", "note": "Constructive pedagogical advice"},
            {"en": "You shouldn't stay up late before your big presentation.", "km": "អ្នកមិនគួរចូលគេងយឺតមុនពេលធ្វើបទបង្ហាញដ៏សំខាន់របស់អ្នកនោះទេ។", "note": "Negative advice using shouldn't"},
            {"en": "What strategies should I apply to improve my pronunciation?", "km": "តើខ្ញុំគួរអនុវត្តយុទ្ធសាស្ត្រអ្វីខ្លះដើម្បីកែលម្អការបញ្ចេញសំឡេងរបស់ខ្ញុំ?", "note": "Asking for expert recommendation"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "You should to practice every day.", "correct": "You should practice every day.", "reason": "'Should' is a modal auxiliary; do not add 'to' before the main verb."},
            {"wrong": "He shoulds speak louder.", "correct": "He should speak louder.", "reason": "Modal verbs never take '-s' in the third person."}
        ]),
        "tips": "Always use 'should + bare infinitive' (no 'to', no '-ing', no '-s').",
        "quizzes": [
            {
                "question": "If you struggle with pronunciation, you _______ practice shadowing native speakers.",
                "options": ["should", "should to", "ought", "must to"],
                "correct_answer": "should",
                "explanation": "'Should' directly takes the bare infinitive 'practice' without 'to'."
            },
            {
                "question": "Students _______ rely solely on translation apps if they want to think in English.",
                "options": ["shouldn't", "don't should", "should to not", "are not should"],
                "correct_answer": "shouldn't",
                "explanation": "The standard negative form of 'should' is 'should not' or 'shouldn't'."
            }
        ]
    },
    {
        "slug": "linking-words",
        "title": "Linking Words & Discourse Markers",
        "category": "Linking words",
        "cefr_level": "B1",
        "order_index": 8,
        "summary": "Connect sentences, show logical relationships, and deliver cohesive 2–3 minute speaking presentations.",
        "formula": "Addition: Furthermore, Moreover | Contrast: However, Although, On the other hand | Cause/Effect: Therefore, Because, As a result | Sequence: First, Next, Finally",
        "explanation_markdown": """### The Power of Linking Words (Cohesion & Coherence)
Linking words guide the listener or reader through your ideas. They are essential for achieving fluency in writing and speeches.

#### Major Categories:
1. **Addition (Adding extra support)**:
   - *Furthermore, Moreover, In addition, Besides.*
   - Example: *He speaks fluent French. Furthermore, he has lived in Paris.*
2. **Contrast (Showing opposition or exceptions)**:
   - *However, Although, Even though, In contrast, On the other hand.*
   - Example: *Although it rained heavily, they completed the charity marathon.*
   - Note: *However* usually starts a new sentence followed by a comma (*... . However, ...*).
3. **Cause, Reason & Result**:
   - *Because, As, Since, Therefore, Consequently, As a result.*
   - Example: *She studied methodically; therefore, she scored 95% on the test.*
4. **Summary and Conclusion**:
   - *In conclusion, To summarize, All in all, Ultimately.*""",
        "examples_json": json.dumps([
            {"en": "He studied diligently; therefore, he passed the placement test with distinction.", "km": "គាត់បានរៀនយ៉ាងយកចិត្តទុកដាក់ ដូច្នេះហើយ គាត់បានប្រឡងជាប់ការធ្វើតេស្តកំណត់កម្រិតដោយពិន្ទុល្អឥតខ្ចោះ។", "note": "Cause and effect connector: therefore"},
            {"en": "Although the grammar exercise was demanding, all students completed it.", "km": "ទោះបីជាលំហាត់វេយ្យាករណ៍នោះពិបាកក៏ដោយ ក៏សិស្សទាំងអស់បានបំពេញវាបានដែរ។", "note": "Contrast clause starting with although"},
            {"en": "To summarize, daily practice is the true key to language confidence.", "km": "សរុបមក ការអនុវត្តជារៀងរាល់ថ្ងៃគឺជាគន្លឹះពិតប្រាកដឆ្ពោះទៅរកទំនុកចិត្តក្នុងការប្រើប្រាស់ភាសា។", "note": "Conclusion marker"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "Although he was exhausted, but he kept running.", "correct": "Although he was exhausted, he kept running.", "reason": "Never use 'although' and 'but' in the same sentence; choose one."},
            {"wrong": "Because of he was late, he missed the exam.", "correct": "Because he was late, he missed the exam.", "reason": "'Because of' must be followed by a noun or noun phrase, while 'Because' introduces a subject + verb clause."}
        ]),
        "tips": "In speaking presentations, transitions like 'First of all', 'Moreover', and 'On the other hand' give you time to organize your thoughts smoothly.",
        "quizzes": [
            {
                "question": "_______ it was raining persistently, they decided to continue their outdoor hiking trip.",
                "options": ["Although", "However", "Because", "Despite of"],
                "correct_answer": "Although",
                "explanation": "'Although' introduces a subordinate clause of contrast followed by a subject and verb: 'it was raining'."
            },
            {
                "question": "Channarith practiced his speech for three hours every evening. _______, his final presentation was articulate and flawless.",
                "options": ["Consequently", "Although", "In contrast", "Whereas"],
                "correct_answer": "Consequently",
                "explanation": "'Consequently' expresses a logical consequence or result of the hard work mentioned."
            },
            {
                "question": "Which transition phrase is ideal for introducing an opposite viewpoint?",
                "options": ["On the other hand", "Furthermore", "In addition", "For instance"],
                "correct_answer": "On the other hand",
                "explanation": "'On the other hand' introduces a contrasting perspective or counterbalance."
            }
        ]
    },
    {
        "slug": "passive-voice",
        "title": "Passive Voice",
        "category": "Passive Voice",
        "cefr_level": "B1",
        "order_index": 9,
        "summary": "Shift focus to the action or recipient when the doer is unknown, obvious, or less important.",
        "formula": "Subject + Form of 'Be' + Past Participle (V3) (+ by Agent)",
        "explanation_markdown": """### Understanding Passive Voice
In an active sentence, the subject **performs** the action:
- *Active: Thomas Edison invented the phonograph.*
In a passive sentence, the subject **receives** the action:
- *Passive: The phonograph was invented by Thomas Edison.*

#### Tense Shifts:
- Present Simple: *is / are + V3* (*English is spoken worldwide.*)
- Past Simple: *was / were + V3* (*The temple was built in the 12th century.*)
- Present Perfect: *has / have been + V3* (*The report has been completed.*)
- Modal: *modal + be + V3* (*The document must be signed.*)""",
        "examples_json": json.dumps([
            {"en": "Angkor Wat was built in the early 12th century.", "km": "ប្រាសាទអង្គរវត្តត្រូវបានសាងសង់ឡើងនៅដើមសតវត្សរ៍ទី ១២។", "note": "Past passive: was + built"},
            {"en": "English is spoken by millions of people across continents.", "km": "ភាសាអង់គ្លេសត្រូវបាននិយាយដោយមនុស្សរាប់លាននាក់នៅទូទាំងទ្វីប។", "note": "Present passive: is + spoken"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "The car was damage in the accident.", "correct": "The car was damaged in the accident.", "reason": "Passive voice always uses the past participle (damaged), not the base form."},
            {"wrong": "The bridge was builded in 1995.", "correct": "The bridge was built in 1995.", "reason": "The past participle of 'build' is irregular: 'built'."}
        ]),
        "tips": "Only transitive verbs (verbs that take an object) can be transformed into the passive voice.",
        "quizzes": [
            {
                "question": "The historic novel _______ into over twenty languages.",
                "options": ["has been translated", "has translated", "is translate", "was translating"],
                "correct_answer": "has been translated",
                "explanation": "Passive present perfect requires 'has been + past participle': 'has been translated'."
            },
            {
                "question": "All assignments must _______ before Friday afternoon.",
                "options": ["be submitted", "submit", "being submitted", "submitted"],
                "correct_answer": "be submitted",
                "explanation": "Modal passive follows the pattern: modal + be + past participle: 'must be submitted'."
            }
        ]
    },
    {
        "slug": "conditionals",
        "title": "First & Second Conditionals",
        "category": "Conditionals",
        "cefr_level": "B1",
        "order_index": 10,
        "summary": "Express real possibilities in the future (First) and hypothetical or imaginary situations (Second).",
        "formula": "First Conditional: If + Present Simple, will + Base Verb | Second Conditional: If + Past Simple, would + Base Verb",
        "explanation_markdown": """### Conditionals: Real vs. Imaginary
Conditionals describe the result of a certain condition being fulfilled.

#### 1. First Conditional (Real / Probable Future):
Used for things that are likely to happen if a condition occurs:
- *If you practice speaking every day, your fluency will improve.*
- Structure: **If + Present Simple, will + base verb**

#### 2. Second Conditional (Hypothetical / Imaginary Present or Future):
Used for dreams, unreal conditions, or advice:
- *If I won a scholarship, I would study abroad in Canada.*
- *If I were you, I would consult an ESL tutor.*
- Structure: **If + Past Simple, would + base verb**
*(Note: 'were' is traditionally preferred over 'was' for all persons in formal English: If I were you).*""",
        "examples_json": json.dumps([
            {"en": "If you review your flashcards daily, you will remember them effortlessly.", "km": "ប្រសិនបើអ្នកពិនិត្យមើលកាតពាក្យរបស់អ្នកជារៀងរាល់ថ្ងៃ អ្នកនឹងចងចាំវាដោយមិនពិបាកឡើយ។", "note": "First conditional: real condition"},
            {"en": "If I had more leisure time, I would learn a third foreign language.", "km": "ប្រសិនបើខ្ញុំមានពេលទំនេរច្រើនជាងនេះ ខ្ញុំនឹងរៀនភាសាបរទេសទីបី។", "note": "Second conditional: hypothetical dream"}
        ]),
        "common_mistakes_json": json.dumps([
            {"wrong": "If it will rain tomorrow, I will stay home.", "correct": "If it rains tomorrow, I will stay home.", "reason": "Never use 'will' in the 'if'-clause of a first conditional."},
            {"wrong": "If I was you, I would accept the scholarship.", "correct": "If I were you, I would accept the scholarship.", "reason": "In hypothetical subjunctive advice, 'were' is standard for all subjects."}
        ]),
        "tips": "Notice the sequence of tenses: Present -> Will (First conditional); Past -> Would (Second conditional).",
        "quizzes": [
            {
                "question": "If you _______ to class on time, you will not miss the presentation instructions.",
                "options": ["come", "will come", "came", "are coming"],
                "correct_answer": "come",
                "explanation": "In a first conditional, the 'if'-clause always takes the Present Simple ('come')."
            },
            {
                "question": "If I _______ a million dollars, I would establish an educational scholarship fund.",
                "options": ["had", "have", "will have", "would have"],
                "correct_answer": "had",
                "explanation": "In a second conditional (hypothetical), the condition uses the Past Simple: 'had'."
            }
        ]
    }
]

PLACEMENT_QUESTIONS = [
    # 1. Present Simple
    {
        "category": "Present Simple",
        "question": "Darith _______ to the local sports club three times a week.",
        "options": ["go", "goes", "is going", "has gone"],
        "correct_answer": "goes",
        "explanation": "With third-person singular (Darith), verbs ending in -o take '-es' in the Present Simple."
    },
    {
        "category": "Present Simple",
        "question": "My friends _______ like spicy food, so we usually order mild dishes.",
        "options": ["doesn't", "don't", "aren't", "not"],
        "correct_answer": "don't",
        "explanation": "'My friends' is plural, requiring 'don't + base verb'."
    },
    {
        "category": "Present Simple",
        "question": "_______ water boil at 100 degrees Celsius under standard atmospheric pressure?",
        "options": ["Do", "Does", "Is", "Has"],
        "correct_answer": "Does",
        "explanation": "For singular uncountable nouns (water), the question auxiliary in Present Simple is 'Does'."
    },
    # 2. Present Continuous
    {
        "category": "Present Continuous",
        "question": "Right now, the research team _______ the results of the survey.",
        "options": ["analyses", "is analysing", "has analysed", "analysed"],
        "correct_answer": "is analysing",
        "explanation": "'Right now' specifies an ongoing action in progress at this moment, using the Present Continuous."
    },
    {
        "category": "Present Continuous",
        "question": "Why _______ your sunglasses inside the dark auditorium?",
        "options": ["are you wearing", "do you wear", "you are wearing", "wear you"],
        "correct_answer": "are you wearing",
        "explanation": "Question word order: Question word + auxiliary (are) + subject (you) + verb-ing (wearing)?"
    },
    # 3. Past Simple
    {
        "category": "Past Simple",
        "question": "Last weekend, our class _______ an educational excursion to the National Museum.",
        "options": ["organises", "organised", "was organise", "has organised"],
        "correct_answer": "organised",
        "explanation": "'Last weekend' requires the Past Simple form 'organised'."
    },
    {
        "category": "Past Simple",
        "question": "She _______ attend the conference because she had a severe fever.",
        "options": ["didn't", "wasn't", "not did", "doesn't"],
        "correct_answer": "didn't",
        "explanation": "Past simple negative for main verbs requires 'didn't + base verb (attend)'."
    },
    {
        "category": "Past Simple",
        "question": "Where _______ you meet your current best friend for the first time?",
        "options": ["did", "do", "were", "have"],
        "correct_answer": "did",
        "explanation": "Questions in the Past Simple use the auxiliary 'did'."
    },
    # 4. Present Perfect
    {
        "category": "Present Perfect",
        "question": "I _______ in this historic neighborhood since I was seven years old.",
        "options": ["live", "lived", "have lived", "am living"],
        "correct_answer": "have lived",
        "explanation": "'Since' with a past starting point denotes an action continuing up to the present: 'have lived'."
    },
    {
        "category": "Present Perfect",
        "question": "Have you _______ delivered a presentation in English in front of an international audience?",
        "options": ["ever", "never", "yet", "already"],
        "correct_answer": "ever",
        "explanation": "'Ever' is used in questions to ask about experiences at any point in one's life."
    },
    {
        "category": "Present Perfect",
        "question": "He has worked at the financial institution _______ nearly a decade.",
        "options": ["since", "for", "during", "ago"],
        "correct_answer": "for",
        "explanation": "Use 'for' when referring to a duration of time ('nearly a decade')."
    },
    # 5. Comparative and Superlative
    {
        "category": "Comparative and superlative adjectives",
        "question": "This newly constructed highway is _______ than the old rural route.",
        "options": ["more safe", "safer", "safest", "the safest"],
        "correct_answer": "safer",
        "explanation": "One-syllable adjective 'safe' forms its comparative by adding '-r': 'safer than'."
    },
    {
        "category": "Comparative and superlative adjectives",
        "question": "Public speaking is considered _______ fear among university freshmen.",
        "options": ["the most common", "most common", "the commonest", "more common"],
        "correct_answer": "the most common",
        "explanation": "The superlative for multi-syllable adjectives requires 'the most + adjective': 'the most common'."
    },
    # 6. Be Going To
    {
        "category": "Be going to",
        "question": "Look at those dark storm clouds gathering; it _______ rain soon.",
        "options": ["is going to", "will to", "is going", "shall to"],
        "correct_answer": "is going to",
        "explanation": "Predictions based on present tangible evidence take 'is going to'."
    },
    {
        "category": "Be going to",
        "question": "We have booked our flights! We _______ our relatives in Siem Reap next month.",
        "options": ["are going to visit", "will visiting", "visit", "are visit"],
        "correct_answer": "are going to visit",
        "explanation": "A prior planned arrangement/intention uses 'are going to visit'."
    },
    # 7. Should
    {
        "category": "Should",
        "question": "You have a sore throat and fever; you _______ rest and drink warm water.",
        "options": ["should", "should to", "ought", "must to"],
        "correct_answer": "should",
        "explanation": "'Should' takes a bare infinitive without 'to': 'should rest'."
    },
    {
        "category": "Should",
        "question": "Learners _______ memorize grammar rules without understanding their real-world usage.",
        "options": ["shouldn't", "don't should", "should to not", "are not should"],
        "correct_answer": "shouldn't",
        "explanation": "The negative form of advice is 'shouldn't + base verb'."
    },
    # 8. Linking Words
    {
        "category": "Linking words",
        "question": "He practiced speaking every day. _______, his confidence and fluency flourished.",
        "options": ["Consequently", "Although", "Whereas", "Despite"],
        "correct_answer": "Consequently",
        "explanation": "'Consequently' introduces a logical result or effect of the daily practice."
    },
    {
        "category": "Linking words",
        "question": "_______ it was late and everyone was weary, the team finished the platform prototype.",
        "options": ["Although", "However", "Because of", "In spite"],
        "correct_answer": "Although",
        "explanation": "'Although' introduces a subordinate clause of contrast followed by a clause with subject and verb."
    },
    {
        "category": "Linking words",
        "question": "She excels in conversational fluency; _______, her written academic essays are outstanding.",
        "options": ["moreover", "however", "on the contrary", "nevertheless"],
        "correct_answer": "moreover",
        "explanation": "'Moreover' adds supplementary positive information supporting the first statement."
    },
    # 9. Vocabulary
    {
        "category": "Vocabulary",
        "question": "A person who can communicate with ease, speed, and accuracy in a language is said to be _______.",
        "options": ["fluent", "hesitant", "reluctant", "ambiguous"],
        "correct_answer": "fluent",
        "explanation": "'Fluent' means able to speak or write a foreign language easily and accurately."
    },
    {
        "category": "Vocabulary",
        "question": "Regular spaced repetition aids in the _______ of new vocabulary in long-term memory.",
        "options": ["retention", "hesitation", "distraction", "omission"],
        "correct_answer": "retention",
        "explanation": "'Retention' refers to the ability to retain or keep facts and knowledge in memory."
    },
    {
        "category": "Vocabulary",
        "question": "When facing a daunting obstacle, students who _______ eventually attain mastery.",
        "options": ["persevere", "surrender", "hesitate", "neglect"],
        "correct_answer": "persevere",
        "explanation": "'Persevere' means to persist in an endeavor despite difficulties or delays."
    },
    # 10. Sentence Construction
    {
        "category": "Sentence construction",
        "question": "Which of the following sentences has the most natural and grammatically correct word order?",
        "options": [
            "Every evening after dinner, Sophea meticulously reviews her English vocabulary notebook.",
            "Reviews Sophea her English vocabulary notebook every evening after dinner meticulously.",
            "Sophea reviews meticulously after dinner every evening her English vocabulary notebook.",
            "Her English vocabulary notebook Sophea every evening reviews meticulously after dinner."
        ],
        "correct_answer": "Every evening after dinner, Sophea meticulously reviews her English vocabulary notebook.",
        "explanation": "Standard English syntax places time adverbials either at the start or end, with Subject + Adverb of manner + Verb + Direct Object."
    },
    # 11. Reading Comprehension
    {
        "category": "Reading comprehension",
        "question": "Read the passage: 'Active language production, such as speaking and writing, builds neural pathways far more effectively than passive observation. When learners synthesize their own thoughts into coherent sentences, they bridge the gap between comprehension and true fluency.' According to the text, what is essential for true fluency?",
        "options": [
            "Synthesizing personal thoughts into coherent sentences through active production",
            "Passively listening to lectures without speaking",
            "Memorizing grammar rules without producing sentences",
            "Relying entirely on translation software"
        ],
        "correct_answer": "Synthesizing personal thoughts into coherent sentences through active production",
        "explanation": "The text directly states that bridging the gap to true fluency occurs when learners actively synthesize their own thoughts into sentences."
    },
    {
        "category": "Reading comprehension",
        "question": "Based on the same passage, why is passive observation less effective than active practice?",
        "options": [
            "Because active production builds neural pathways much more effectively",
            "Because passive observation requires more physical effort",
            "Because neural pathways are only formed during examinations",
            "Because writing is easier than reading"
        ],
        "correct_answer": "Because active production builds neural pathways much more effectively",
        "explanation": "The passage states that active production 'builds neural pathways far more effectively than passive observation'."
    }
]

SPEAKING_TOPICS = [
    {
        "topic_number": 1,
        "title": "Topic 1: Personal Background, Daily Routine & Passions",
        "subtitle": "Introducing yourself fluently, describing your day with precision, and sharing what drives your ambitions.",
        "duration_target": "2–3 Minutes",
        "overview": "Mastering the 2–3 minute self-presentation is the benchmark of spoken English confidence. In this topic, you will learn to structure your introduction, describe daily habits with adverbs of frequency, explain your primary passion, and conclude memorably.",
        "structure_json": json.dumps([
            {
                "section": "1. Engaging Hook & Personal Introduction",
                "target_time": "0:00 - 0:30 (30 seconds)",
                "guiding_questions": "Who are you? What is your background, and what is one memorable adjective or motto that defines you?",
                "key_phrases": ["Good morning/afternoon everyone. Today, I am excited to share...", "My name is... and I would describe myself as an avid learner.", "Currently, I am focusing on..."]
            },
            {
                "section": "2. Daily Routine & Disciplined Habits",
                "target_time": "0:30 - 1:30 (60 seconds)",
                "guiding_questions": "What does a productive day look like for you? How do you balance responsibilities with personal growth?",
                "key_phrases": ["On a typical weekday, my morning commences with...", "Without exception, I dedicate at least thirty minutes to...", "In the afternoon, my primary responsibility involves..."]
            },
            {
                "section": "3. Passions, Hobbies & What Inspires You",
                "target_time": "1:30 - 2:15 (45 seconds)",
                "guiding_questions": "What activity makes you lose track of time? Why is it meaningful to your character?",
                "key_phrases": ["Beyond my daily duties, my true passion lies in...", "What captivates me most about this pursuit is...", "It allows me to unwind while simultaneously broadening my perspective."]
            },
            {
                "section": "4. Memorable Conclusion & Future Vision",
                "target_time": "2:15 - 2:45 (30 seconds)",
                "guiding_questions": "What core message or takeaway do you want your audience to remember about you?",
                "key_phrases": ["To wrap up my thoughts, I firmly believe that...", "Consistency is the vehicle for long-term growth.", "Thank you very much for your time and kind attention."]
            }
        ]),
        "vocabulary_json": json.dumps([
            {"word": "Productivity", "pos": "noun", "km": "ផលិតភាព", "en": "The effectiveness of productive effort, especially in industry or personal work.", "example": "A disciplined morning routine enhances my daily productivity."},
            {"word": "Dedicate", "pos": "verb", "km": "លះបង់ / ឧទ្ទិស", "en": "Devote time or resources to a particular task or purpose.", "example": "I dedicate one hour every evening to mastering English."},
            {"word": "Passionate", "pos": "adj", "km": "ដែលមានចំណង់ចំណូលចិត្តខ្លាំង", "en": "Having or showing compelling enthusiasm or belief.", "example": "She is passionate about educational technology."},
            {"word": "Perseverance", "pos": "noun", "km": "ការតស៊ូព្យាយាម", "en": "Persistence in doing something despite difficulty or delay.", "example": "Through sheer perseverance, he achieved fluency."},
            {"word": "Unwind", "pos": "verb", "km": "សម្រាកបន្ធូរអារម្មណ៍", "en": "Relax after a period of work or tension.", "example": "Reading non-fiction helps me unwind before bed."}
        ]),
        "transition_phrases_json": json.dumps([
            "First of all, let me introduce myself...",
            "On a typical day, I usually start by...",
            "Furthermore, what really drives me is...",
            "In addition to my daily responsibilities...",
            "All in all, this daily rhythm shapes who I am."
        ]),
        "sample_speech": """Good morning, everyone. It is a genuine pleasure to speak with you today. My name is Visal, and if I had to describe myself in a few words, I would say I am a curious, disciplined, and forward-thinking individual. 

On a typical day, my routine begins at six o'clock in the morning. I believe that how you spend your first hour sets the tone for the entire day. Therefore, I always spend fifteen minutes doing light exercise, followed by a nutritious breakfast and a quick review of my English vocabulary flashcards. During the day, I am fully engaged in my academic studies and professional projects. What I prioritize above all else is focused productivity; rather than multitasking, I prefer to tackle my most challenging tasks when my energy is at its peak.

Beyond my daily obligations, my greatest passion lies in technology and foreign languages. To me, learning English is not merely memorizing grammar rules; it is a bridge that connects me with global ideas, diverse cultures, and endless opportunities. Whenever I have free time on the weekend, I enjoy reading tech journals, engaging in language exchange discussions, and mentoring younger students in my community. 

To conclude, I firmly believe that success is not determined by sporadic bursts of effort, but by the quiet consistency of our daily habits. Every single day offers a fresh canvas to learn something new and become a better version of ourselves. Thank you very much for listening, and I look forward to hearing your thoughts!""",
        "guiding_questions_json": json.dumps([
            "How do you greet your audience and present your core identity?",
            "What adverbs of frequency (always, usually, rarely) can you weave into your morning description?",
            "What specific example demonstrates your passion rather than just stating it?",
            "How does your conclusion tie back to your opening statement?"
        ])
    },
    {
        "topic_number": 2,
        "title": "Topic 2: Hometown, Cultural Heritage & Community Life",
        "subtitle": "Describing where you come from, local traditions, culinary pride, and community atmosphere.",
        "duration_target": "2–3 Minutes",
        "overview": "Learn how to paint vivid visual pictures with sensory language and descriptive adjectives. This topic guides you through presenting your hometown's geographical setting, cultural landmarks, local gastronomy, and the warm spirit of your community.",
        "structure_json": json.dumps([
            {
                "section": "1. Geographic Setting & First Impression",
                "target_time": "0:00 - 0:35 (35 seconds)",
                "guiding_questions": "Where is your hometown situated? What is the atmosphere when someone visits for the first time?",
                "key_phrases": ["Today, I would like to transport you to my hometown...", "Nestled in the heart of...", "What strikes visitors first is the vibrant atmosphere..."]
            },
            {
                "section": "2. Cultural Heritage & Architectural Marvels",
                "target_time": "0:35 - 1:25 (50 seconds)",
                "guiding_questions": "What historic or cultural treasures distinguish your hometown? What stories do they tell?",
                "key_phrases": ["My hometown is steeped in rich history...", "One landmark that stands out is...", "It stands as a testament to our ancestors' craftsmanship..."]
            },
            {
                "section": "3. Gastronomy, Local Life & Hospitality",
                "target_time": "1:25 - 2:15 (50 seconds)",
                "guiding_questions": "What local dishes must every traveler taste? How do neighbors interact?",
                "key_phrases": ["No visit would be complete without savoring...", "The local cuisine features a harmonious blend of...", "Above all, the residents are renowned for their hospitality..."]
            },
            {
                "section": "4. Reflection & Personal Connection",
                "target_time": "2:15 - 2:45 (30 seconds)",
                "guiding_questions": "Why does this place hold a special place in your heart, and what is its future?",
                "key_phrases": ["No matter where my future endeavors take me...", "My hometown will always remain my anchor.", "I warmly invite each of you to experience its charm firsthand."]
            }
        ]),
        "vocabulary_json": json.dumps([
            {"word": "Picturesque", "pos": "adj", "km": "ស្រស់ស្អាតដូចគំនូរ", "en": "Visually attractive, especially in a quaint or charming way.", "example": "The riverside promenade in my hometown is truly picturesque."},
            {"word": "Hospitality", "pos": "noun", "km": "បដិសណ្ឋារកិច្ច", "en": "The friendly and generous reception and entertainment of guests.", "example": "Cambodian hospitality is celebrated across the world."},
            {"word": "Heritage", "pos": "noun", "km": "បេតិកភណ្ឌ", "en": "Valued objects and qualities such as historic buildings and cultural traditions passed down.", "example": "Preserving our cultural heritage is our generational duty."},
            {"word": "Bustling", "pos": "adj", "km": "អ៊ូអរ / អ៊ូអរដោយសកម្មភាព", "en": "Full of energetic and noisy activity.", "example": "The morning market is always bustling with traders and aroma."},
            {"word": "Culinary", "pos": "adj", "km": "ទាក់ទងនឹងការចម្អិនអាហារ", "en": "Related to cooking or the kitchen.", "example": "Our town offers an unforgettable culinary experience."}
        ]),
        "transition_phrases_json": json.dumps([
            "Speaking of geographic charm...",
            "What makes our culture truly distinctive is...",
            "In terms of local gastronomy...",
            "Equally important is the warmth of the people...",
            "Looking toward the future..."
        ]),
        "sample_speech": """Hello everyone. Today, I am proud to take you on a journey to my beloved hometown: Siem Reap, a historic province in northwestern Cambodia that seamlessly bridges ancient heritage with modern vitality.

When people think of Siem Reap, the majestic silhouette of Angkor Wat immediately springs to mind. And indeed, living in the shadow of the world's largest religious monument is an awe-inspiring privilege. The intricate bas-reliefs, soaring towers, and ancient stone carvings remind us every day of the remarkable artistic and architectural genius of our ancestors. Yet, Siem Reap is far more than an open-air museum; it is a living, breathing community.

In the early morning, our town awakens to the cheerful clamor of local markets. The air is filled with the tantalizing aroma of Nom Banh Chok, our traditional Khmer rice noodles served in a fragrant lemongrass fish broth, and freshly brewed robust coffee. What truly sets our community apart, however, is not just the food or the architecture—it is the heartfelt warmth of its people. Neighbors still greet one another by name, elders are treated with deep reverence, and visitors are welcomed as extended family.

While rapid modernization has brought international cafes and boutique hotels, the soul of the province remains grounded in kindness and cultural pride. No matter where my career or studies may lead me in the future, Siem Reap will always be my anchor and source of inspiration. If you have not yet experienced the magic of sunrise over the ancient temples and the genuine smile of our residents, I wholeheartedly invite you to visit. Thank you very much.""",
        "guiding_questions_json": json.dumps([
            "What sensory details (sight, sound, aroma) bring your hometown to life?",
            "How do you balance talking about physical places with the spirit of the people?",
            "What transitional phrases guide the listener from morning markets to personal reflections?"
        ])
    },
    {
        "topic_number": 3,
        "title": "Topic 3: Educational Aspirations, Career Goals & Technology",
        "subtitle": "Articulating your academic ambitions, professional vision, and the transformative impact of technology.",
        "duration_target": "2–3 Minutes",
        "overview": "Delivering an articulate professional presentation requires clarity of vision, modal verbs of future intent, and specialized vocabulary. Here you will structure an argument detailing your academic journey, career goals, and how digital innovation shapes your path.",
        "structure_json": json.dumps([
            {
                "section": "1. Academic Foundation & Current Pursuits",
                "target_time": "0:00 - 0:35 (35 seconds)",
                "guiding_questions": "What are you studying or researching? What sparked your fascination with this field?",
                "key_phrases": ["Currently, my academic pursuits are centered on...", "What initially ignited my passion for this field was...", "Throughout my learning journey, I have realized..."]
            },
            {
                "section": "2. Short-term and Long-term Career Milestones",
                "target_time": "0:35 - 1:30 (55 seconds)",
                "guiding_questions": "Where do you see yourself in 3 years? In 10 years? What specific impact do you strive to create?",
                "key_phrases": ["In the short term, I aim to master...", "Looking ahead toward the next five years, my goal is to...", "Ultimately, I aspire to lead initiatives that..."]
            },
            {
                "section": "3. The Transformative Role of Technology",
                "target_time": "1:30 - 2:15 (45 seconds)",
                "guiding_questions": "How does digital transformation influence your discipline? How are you preparing for it?",
                "key_phrases": ["In today's fast-evolving landscape, technology is not optional; it is essential.", "Tools like artificial intelligence and automated systems allow us to...", "By embracing digital literacy, we can solve complex challenges..."]
            },
            {
                "section": "4. Decisive Action Plan & Closing Vision",
                "target_time": "2:15 - 2:45 (30 seconds)",
                "guiding_questions": "What concrete steps are you taking right now to ensure this ambition becomes reality?",
                "key_phrases": ["To turn these aspirations into tangible reality, I am...", "With perseverance and lifelong learning, I am confident that...", "Thank you for sharing this vision with me today."]
            }
        ]),
        "vocabulary_json": json.dumps([
            {"word": "Aspiration", "pos": "noun", "km": "សេចក្តីប្រាថ្នា / បំណងប្រាថ្នា", "en": "A hope or ambition of achieving something worthwhile.", "example": "Her aspiration is to become a leading data scientist."},
            {"word": "Transformative", "pos": "adj", "km": "ដែលមានការផ្លាស់ប្តូរជាវិជ្ជមានខ្លាំង", "en": "Causing a marked change in someone or something.", "example": "Artificial intelligence has had a transformative effect on education."},
            {"word": "Milestone", "pos": "noun", "km": "សមិទ្ធផលសំខាន់ / ព្រឹត្តិការណ៍សំខាន់", "en": "A significant stage or event in the development of something.", "example": "Graduating with honors was a key milestone in his career."},
            {"word": "Digital literacy", "pos": "noun", "km": "ចំណេះដឹងឌីជីថល", "en": "The ability to use information and communication technologies effectively.", "example": "Digital literacy is essential for modern career mobility."},
            {"word": "Innovate", "pos": "verb", "km": "បង្កើតគំនិតថ្មី / ធ្វើនវានុវត្តន៍", "en": "Make changes in something established, especially by introducing new methods.", "example": "Enterprises must innovate continuously to remain competitive."}
        ]),
        "transition_phrases_json": json.dumps([
            "Regarding my professional trajectory...",
            "In terms of technological integration...",
            "Furthermore, to bridge theory and practice...",
            "In consequence of these rapid advancements...",
            "To conclude on an ambitious note..."
        ]),
        "sample_speech": """Good afternoon, esteemed listeners. We live in an era of unprecedented technological transformation, where traditional boundaries are disappearing and lifelong learning has become our most vital asset. Today, I am excited to share with you my educational aspirations, career objectives, and how I plan to harness technology to contribute meaningfully to society.

Currently, my academic efforts are concentrated on computer science and international communication. I chose this intersection because I realized early on that technical acumen without effective communication is limited, while communication without modern technical tools cannot scale. Mastering fluent English is an integral pillar of this vision; it empowers me to study cutting-edge research, collaborate with engineers globally, and articulate innovative ideas with precision.

Looking ahead toward the next three to five years, my primary milestone is to work as a software architect focusing on educational platforms. In many developing regions, talented students lack access to high-quality learning resources. My vision is to design intelligent, lightweight applications that run smoothly even in low-bandwidth environments, delivering interactive language and STEM lessons to learners regardless of socioeconomic background.

Technology, particularly artificial intelligence and automated feedback systems, will be the catalyst for this transformation. Rather than replacing human educators, these tools can handle repetitive grading and provide personalized pacing, allowing teachers to focus on mentorship and critical thinking.

To transform these aspirations into reality, I hold myself accountable each day. I spend two hours writing code, one hour practicing oral English presentations, and thirty minutes reading technology literature. I firmly believe that the future belongs to those who prepare for it today with deliberate dedication. Thank you very much for your kind attention.""",
        "guiding_questions_json": json.dumps([
            "How do you introduce your academic specialization with authority?",
            "What specific problem does your career goal aim to solve for society?",
            "How do you use 'be going to' and 'plan to' to demonstrate concrete planning?"
        ])
    },
    {
        "topic_number": 4,
        "title": "Topic 4: A Memorable Experience, Travel & Life Lessons",
        "subtitle": "Narrating a defining journey, overcoming an unforeseen obstacle, and reflecting on wisdom gained.",
        "duration_target": "2–3 Minutes",
        "overview": "Storytelling is one of the most powerful forms of human communication. This topic equips you with the narrative past tenses (Past Simple, Past Continuous, Past Perfect) needed to recount a memorable journey or challenge, build suspense, and draw a meaningful moral lesson.",
        "structure_json": json.dumps([
            {
                "section": "1. Setting the Stage & Context",
                "target_time": "0:00 - 0:35 (35 seconds)",
                "guiding_questions": "When and where did this event take place? What were your expectations at the start?",
                "key_phrases": ["I would like to take you back three years ago...", "It was a crisp Saturday morning when...", "Little did I know that this journey would completely transform my perspective."]
            },
            {
                "section": "2. The Rising Action & Unforeseen Challenge",
                "target_time": "0:35 - 1:30 (55 seconds)",
                "guiding_questions": "What went wrong? How did you feel when confronting the obstacle?",
                "key_phrases": ["Everything was proceeding smoothly until suddenly...", "While we were trekking through the dense forest...", "Faced with this predicament, panic initially set in..."]
            },
            {
                "section": "3. The Climax, Teamwork & Resolution",
                "target_time": "1:30 - 2:15 (45 seconds)",
                "guiding_questions": "How did you overcome the hurdle? Who assisted you, and what action resolved the situation?",
                "key_phrases": ["Taking a deep breath, we realized that collaboration was our only option.", "Step by step, we improvised a solution by...", "When we finally reached our destination, the feeling of relief was overwhelming."]
            },
            {
                "section": "4. The Philosophical Moral & Lasting Impact",
                "target_time": "2:15 - 2:45 (30 seconds)",
                "guiding_questions": "How did this experience shape your outlook on life? What advice would you offer to others?",
                "key_phrases": ["Reflecting on that unforgettable day, I learned that...", "True resilience is forged not in comfort, but in adversity.", "Thank you for allowing me to share this personal chapter with you."]
            }
        ]),
        "vocabulary_json": json.dumps([
            {"word": "Unforgettable", "pos": "adj", "km": "ដែលមិនអាចបំភ្លេចបាន", "en": "Impossible to forget; very memorable.", "example": "Standing at the summit was an unforgettable moment."},
            {"word": "Predicament", "pos": "noun", "km": "ស្ថានភាពលំបាក / វិបត្តិ", "en": "A difficult, unpleasant, or embarrassing situation.", "example": "We found ourselves in an unexpected predicament when the engine failed."},
            {"word": "Resilience", "pos": "noun", "km": "ភាពធន់រឹងមាំ / ភាពមិនចុះចាញ់", "en": "The capacity to recover quickly from difficulties; toughness.", "example": "The community displayed admirable resilience after the flood."},
            {"word": "Epiphany", "pos": "noun", "km": "ការភ្ញាក់រលឹកភ្លាមៗ / ការយល់ឃើញដ៏ជ្រាលជ្រៅ", "en": "A moment of sudden and great revelation or realization.", "example": "During the journey, I had an epiphany regarding my life priorities."},
            {"word": "Broaden horizons", "pos": "idiom", "km": "ពង្រីកការយល់ដឹងនិងទស្សនវិស័យ", "en": "Expand one's knowledge, experience, or perspective.", "example": "Traveling solo to new places broadens your horizons immensely."}
        ]),
        "transition_phrases_json": json.dumps([
            "It all began on an ordinary afternoon...",
            "Suddenly and without warning...",
            "While we were attempting to find our way...",
            "In that critical moment, I realized...",
            "Looking back on this experience with maturity..."
        ]),
        "sample_speech": """Good afternoon, everyone. Have you ever experienced a single moment that completely shattered your comfort zone and forced you to discover strengths you never knew you possessed? Today, I want to share a memorable journey that taught me the true meaning of resilience and adaptability.

Two years ago, during the monsoon season, my friends and I embarked on a weekend hiking expedition to the Cardamom Mountains. We were energetic and enthusiastic, expecting an easy trek along scenic trails. However, nature had a different lesson in store for us. Around three o'clock in the afternoon, while we were navigating a steep, rocky ridge, the sky turned pitch black and a torrential downpour unleashed without warning.

Within minutes, the gentle stream we were supposed to cross swelled into a raging, impassable muddy torrent. To make matters worse, our mobile phones lost all cellular reception, and darkness was rapidly encroaching. For a brief moment, anxiety gripped our group; we were soaked, exhausted, and stranded miles away from the base camp.

In that critical juncture, we understood that succumbing to panic would solve nothing. We huddled together, took stock of our supplies, and decided to establish a makeshift shelter on high ground using tarpaulins and sturdy bamboo poles. We took turns keeping watch and sharing our remaining rations. That night, sitting in the damp chill listening to the howling storm, we spoke openly about our fears, our dreams, and our gratitude for one another. When dawn finally broke and local rangers reached our coordinates, the relief was indescribable.

Looking back, while that ordeal was terrifying at the time, it was also the most transformative lesson of my youth. It taught me that life's storms are inevitable, but panic is a choice. When we confront adversity with calm reasoning and solidarity, no obstacle is insurmountable. Thank you very much for listening.""",
        "guiding_questions_json": json.dumps([
            "How do you hook the listener with an introspective question at the beginning?",
            "What past continuous clauses ('while we were navigating...') add dramatic tension?",
            "How does your conclusion elevate a personal hiking adventure into universal human wisdom?"
        ])
    }
]

VOCABULARY_ITEMS = [
    # Beginner (A1-A2)
    {"word": "Accomplish", "pos": "verb", "phonetic": "/əˈkʌm.plɪʃ/", "definition_en": "Achieve or complete successfully.", "definition_km": "សម្រេចបានជោគជ័យ", "example_sentence": "If you plan your daily schedule well, you will accomplish all your goals.", "difficulty_level": "Beginner", "category": "Work & Career"},
    {"word": "Accurate", "pos": "adj", "phonetic": "/ˈæk.jə.rət/", "definition_en": "Correct in all details; exact.", "definition_km": "ត្រឹមត្រូវច្បាស់លាស់", "example_sentence": "Her pronunciation was accurate and easy for everyone to understand.", "difficulty_level": "Beginner", "category": "Education"},
    {"word": "Habit", "pos": "noun", "phonetic": "/ˈhæb.ɪt/", "definition_en": "A settled or regular tendency or practice.", "definition_km": "ទម្លាប់", "example_sentence": "Reviewing ten English words each morning is an excellent habit.", "difficulty_level": "Beginner", "category": "Daily Life"},
    {"word": "Improve", "pos": "verb", "phonetic": "/ɪmˈpruːv/", "definition_en": "Make or become better.", "definition_km": "កែលម្អ / ធ្វើឱ្យប្រសើរឡើង", "example_sentence": "Your speaking confidence will improve with daily vocal practice.", "difficulty_level": "Beginner", "category": "Education"},
    {"word": "Nutritious", "pos": "adj", "phonetic": "/njuːˈtrɪʃ.əs/", "definition_en": "Efficient as food; nourishing.", "definition_km": "ដែលសំបូរទៅដោយជីវជាតិ", "example_sentence": "Eating a nutritious breakfast provides steady energy throughout the morning.", "difficulty_level": "Beginner", "category": "Health & Wellness"},
    {"word": "Routine", "pos": "noun", "phonetic": "/ruːˈtiːn/", "definition_en": "A sequence of actions regularly followed.", "definition_km": "កាលវិភាគ ឬទម្លាប់ប្រចាំថ្ងៃ", "example_sentence": "My morning routine includes stretching and reading for twenty minutes.", "difficulty_level": "Beginner", "category": "Daily Life"},
    {"word": "Confident", "pos": "adj", "phonetic": "/ˈkɒn.fɪ.dənt/", "definition_en": "Feeling or showing certainty about something.", "definition_km": "ដែលមានទំនុកចិត្តលើខ្លួនឯង", "example_sentence": "He felt confident before stepping on stage to deliver his speech.", "difficulty_level": "Beginner", "category": "Emotions & Character"},
    {"word": "Community", "pos": "noun", "phonetic": "/kəˈmjuː.nə.ti/", "definition_en": "A group of people living in the same place or having a particular characteristic in common.", "definition_km": "សហគមន៍", "example_sentence": "Our local community organized a clean-up campaign last weekend.", "difficulty_level": "Beginner", "category": "Daily Life"},
    {"word": "Frequent", "pos": "adj", "phonetic": "/ˈfriː.kwənt/", "definition_en": "Occurring or done on many occasions.", "definition_km": "ដែលកើតឡើងញឹកញាប់", "example_sentence": "Frequent revision prevents newly learned words from fading.", "difficulty_level": "Beginner", "category": "Education"},
    {"word": "Polite", "pos": "adj", "phonetic": "/pəˈlaɪt/", "definition_en": "Having or showing behavior that is respectful and considerate.", "definition_km": "គួរសម / សុភាពរាបសារ", "example_sentence": "Using 'please' and 'thank you' is always polite.", "difficulty_level": "Beginner", "category": "Daily Life"},

    # Intermediate (B1)
    {"word": "Articulate", "pos": "adj", "phonetic": "/ɑːˈtɪk.jə.lət/", "definition_en": "Able to express thoughts and ideas clearly and effectively in speech.", "definition_km": "ដែលអាចបញ្ចេញគំនិតបានច្បាស់លាស់និងស្ទាត់ជំនាញ", "example_sentence": "She delivered an articulate speech that impressed all the judges.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Collaborate", "pos": "verb", "phonetic": "/kəˈlæb.ə.reɪt/", "definition_en": "Work jointly on an activity or project.", "definition_km": "សហការគ្នាធ្វើការងារ", "example_sentence": "Engineers and designers must collaborate closely to build great software.", "difficulty_level": "Intermediate", "category": "Work & Career"},
    {"word": "Distinction", "pos": "noun", "phonetic": "/dɪˈstɪŋk.ʃən/", "definition_en": "A difference or contrast between similar things or people; excellence.", "definition_km": "ភាពខុសប្លែកគ្នា / ភាពឆ្នើម", "example_sentence": "He passed the advanced English examination with highest distinction.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Encounter", "pos": "verb", "phonetic": "/ɪnˈkaʊn.tər/", "definition_en": "Unexpectedly experience or be faced with something difficult.", "definition_km": "ជួបប្រទះ (ឧបសគ្គ ឬបទពិសោធន៍)", "example_sentence": "Every language learner will encounter challenging vocabulary.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Fluency", "pos": "noun", "phonetic": "/ˈfluː.ən.si/", "definition_en": "The ability to speak or write a foreign language easily and accurately.", "definition_km": "ភាពស្ទាត់ជំនាញក្នុងការនិយាយឬសរសេរ", "example_sentence": "Fluency comes from daily spoken practice rather than silent reading alone.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Hesitate", "pos": "verb", "phonetic": "/ˈhez.ɪ.teɪt/", "definition_en": "Pause before saying or doing something through uncertainty.", "definition_km": "ស្ទាក់ស្ទើរ / រារែក", "example_sentence": "Do not hesitate to ask questions when you don't understand a grammar rule.", "difficulty_level": "Intermediate", "category": "Emotions & Character"},
    {"word": "Incorporate", "pos": "verb", "phonetic": "/ɪnˈkɔː.pər.eɪt/", "definition_en": "Take in or contain something as part of a whole; include.", "definition_km": "បញ្ចូល ឬដាក់បញ្ចូលគ្នា", "example_sentence": "Try to incorporate new linking words into your speaking practice.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Milestone", "pos": "noun", "phonetic": "/ˈmaɪl.stəʊn/", "definition_en": "An action or event marking a significant change or stage.", "definition_km": "ដំណាក់កាលឬសមិទ្ធផលសំខាន់", "example_sentence": "Completing the first speaking presentation was a monumental milestone.", "difficulty_level": "Intermediate", "category": "Work & Career"},
    {"word": "Persevere", "pos": "verb", "phonetic": "/ˌpɜː.sɪˈvɪər/", "definition_en": "Continue in a course of action even in the face of difficulty.", "definition_km": "តស៊ូព្យាយាមមិនចុះចាញ់", "example_sentence": "If you persevere through the beginner hurdles, English will become natural.", "difficulty_level": "Intermediate", "category": "Emotions & Character"},
    {"word": "Retention", "pos": "noun", "phonetic": "/rɪˈten.ʃən/", "definition_en": "The continued use, existence, or keeping in memory of something.", "definition_km": "ការរក្សាទុកក្នុងការចងចាំ", "example_sentence": "Spaced repetition drastically increases vocabulary retention over time.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Scenic", "pos": "adj", "phonetic": "/ˈsiː.nɪk/", "definition_en": "Providing or relating to views of impressive or beautiful natural scenery.", "definition_km": "ដែលមានទេសភាពធម្មជាតិស្រស់ត្រកាល", "example_sentence": "We took a scenic train ride through the mountainous countryside.", "difficulty_level": "Intermediate", "category": "Travel & Nature"},
    {"word": "Substantial", "pos": "adj", "phonetic": "/səbˈstæn.ʃəl/", "definition_en": "Of considerable importance, size, or worth.", "definition_km": "ច្រើនគួរឱ្យកត់សម្គាល់ / សំខាន់", "example_sentence": "He showed substantial improvement in his IELTS band score.", "difficulty_level": "Intermediate", "category": "Work & Career"},
    {"word": "Versatile", "pos": "adj", "phonetic": "/ˈvɜː.sə.taɪl/", "definition_en": "Able to adapt or be adapted to many different functions or activities.", "definition_km": "ដែលមានភាពបត់បែននិងប្រើប្រាស់បានច្រើនយ៉ាង", "example_sentence": "A versatile vocabulary enables you to converse in both formal and casual settings.", "difficulty_level": "Intermediate", "category": "Education"},
    {"word": "Vibrant", "pos": "adj", "phonetic": "/ˈvaɪ.brənt/", "definition_en": "Full of energy and enthusiasm; bright and striking.", "definition_km": "ដែលពោរពេញទៅដោយភាពរស់រវើក", "example_sentence": "Phnom Penh has a vibrant cultural and technological startup scene.", "difficulty_level": "Intermediate", "category": "Travel & Nature"},
    {"word": "Furthermore", "pos": "adverb", "phonetic": "/ˌfɜː.ðəˈmɔːr/", "definition_en": "In addition; moreover (used to introduce a fresh point).", "definition_km": "លើសពីនេះទៅទៀត", "example_sentence": "The course is free; furthermore, all study materials are included.", "difficulty_level": "Intermediate", "category": "Connectors & Discourse"},

    # Upper-Intermediate (B2)
    {"word": "Ambiguity", "pos": "noun", "phonetic": "/ˌæm.bɪˈɡjuː.ə.ti/", "definition_en": "The quality of being open to more than one interpretation; inexactness.", "definition_km": "ភាពមិនច្បាស់លាស់ / ន័យកប់ច្រើនយ៉ាង", "example_sentence": "Precise linking words eliminate ambiguity in your academic essays.", "difficulty_level": "Upper-Intermediate", "category": "Education"},
    {"word": "Comprehensive", "pos": "adj", "phonetic": "/ˌkɒm.prɪˈhen.sɪv/", "definition_en": "Including or dealing with all or nearly all elements or aspects of something.", "definition_km": "ដែលទូលំទូលាយនិងក្បោះក្បាយគ្រប់ជ្រុងជ្រោយ", "example_sentence": "This platform provides a comprehensive curriculum for English mastery.", "difficulty_level": "Upper-Intermediate", "category": "Education"},
    {"word": "Cultivate", "pos": "verb", "phonetic": "/ˈkʌl.tɪ.veɪt/", "definition_en": "Try to acquire or develop a quality or skill.", "definition_km": "បណ្តុះបណ្តាល / អភិវឌ្ឍជំនាញ", "example_sentence": "It takes patience to cultivate critical thinking in a second language.", "difficulty_level": "Upper-Intermediate", "category": "Education"},
    {"word": "Eloquent", "pos": "adj", "phonetic": "/ˈel.ə.kwənt/", "definition_en": "Fluent or persuasive in speaking or writing.", "definition_km": "ដែលមានវោហារស័ព្ទល្អនិងមានឥទ្ធិពលទាក់ទាញ", "example_sentence": "The diplomat gave an eloquent speech advocating for educational equality.", "difficulty_level": "Upper-Intermediate", "category": "Work & Career"},
    {"word": "Formidable", "pos": "adj", "phonetic": "/fɔːˈmɪd.ə.bəl/", "definition_en": "Inspiring fear or respect through being impressively large or capable.", "definition_km": "ដែលអស្ចារ្យគួរឱ្យកោតសរសើរនិងស្ញប់ស្ញែង", "example_sentence": "Overcoming public speaking anxiety is a formidable but rewarding challenge.", "difficulty_level": "Upper-Intermediate", "category": "Emotions & Character"},
    {"word": "Insurmountable", "pos": "adj", "phonetic": "/ˌɪn.səˈmaʊn.tə.bəl/", "definition_en": "Too great to be overcome.", "definition_km": "ដែលមិនអាចឆ្លងកាត់ឬយកឈ្នះបាន", "example_sentence": "With persistent effort and support, no academic hurdle is insurmountable.", "difficulty_level": "Upper-Intermediate", "category": "Emotions & Character"},
    {"word": "Nuance", "pos": "noun", "phonetic": "/ˈnjuː.ɑːns/", "definition_en": "A subtle difference in or shade of meaning, expression, or sound.", "definition_km": "ភាពខុសគ្នាបន្តិចបន្តួចយ៉ាងស៊ីជម្រៅនៃអត្ថន័យ", "example_sentence": "Advanced learners appreciate the subtle nuances between near-synonyms.", "difficulty_level": "Upper-Intermediate", "category": "Education"},
    {"word": "Paradigm", "pos": "noun", "phonetic": "/ˈpær.ə.daɪm/", "definition_en": "A typical example or pattern of something; a model.", "definition_km": "គំរូទ្រឹស្តី ឬទស្សនទានគំរូ", "example_sentence": "Spaced repetition represents a paradigm shift in memorization science.", "difficulty_level": "Upper-Intermediate", "category": "Technology"},
    {"word": "Pragmatic", "pos": "adj", "phonetic": "/præɡˈmæt.ɪk/", "definition_en": "Dealing with things sensibly and realistically based on practical considerations.", "definition_km": "ដែលផ្អែកលើការអនុវត្តជាក់ស្តែងនិយម", "example_sentence": "We adopted a pragmatic approach to language learning focusing on speech first.", "difficulty_level": "Upper-Intermediate", "category": "Work & Career"},
    {"word": "Resilience", "pos": "noun", "phonetic": "/rɪˈzɪl.jəns/", "definition_en": "The capacity to recover quickly from difficulties; toughness.", "definition_km": "ភាពធន់រឹងមាំក្នុងការជម្នះឧបសគ្គ", "example_sentence": "Psychological resilience helps students embrace constructive feedback.", "difficulty_level": "Upper-Intermediate", "category": "Emotions & Character"},
    {"word": "Spontaneous", "pos": "adj", "phonetic": "/spɒnˈteɪ.ni.əs/", "definition_en": "Performed or occurring as a result of a sudden impulse without premeditation.", "definition_km": "ដែលកើតឡើងដោយឯកឯងភ្លាមៗមិនបានព្រាងទុក", "example_sentence": "True fluency enables spontaneous conversation without translating in your head.", "difficulty_level": "Upper-Intermediate", "category": "Education"},
    {"word": "Unprecedented", "pos": "adj", "phonetic": "/ʌnˈpres.ɪ.den.tɪd/", "definition_en": "Never done or known before.", "definition_km": "ដែលមិនធ្លាប់មានពីមុនមក", "example_sentence": "Online educational tools have democratized knowledge on an unprecedented scale.", "difficulty_level": "Upper-Intermediate", "category": "Technology"},
    {"word": "Consequently", "pos": "adverb", "phonetic": "/ˈkɒn.sɪ.kwənt.li/", "definition_en": "As a result.", "definition_km": "ជាលទ្ធផល / ដូច្នេះហើយ", "example_sentence": "He spent two hours studying daily; consequently, his test scores soared.", "difficulty_level": "Upper-Intermediate", "category": "Connectors & Discourse"},
    {"word": "Notwithstanding", "pos": "prep", "phonetic": "/ˌnɒt.wɪðˈstæn.dɪŋ/", "definition_en": "In spite of.", "definition_km": "ទោះបីជាយ៉ាងណាក៏ដោយ / បើទោះបីជា", "example_sentence": "Notwithstanding the initial difficulty, she mastered the English phonetic chart.", "difficulty_level": "Upper-Intermediate", "category": "Connectors & Discourse"}
]

PRONUNCIATION_ITEMS = [
    {
        "target_text": "think vs sink",
        "item_type": "minimal_pair",
        "phonetic": "/θɪŋk/ vs /sɪŋk/",
        "focus_sound": "/θ/ (Voiceless dental fricative) vs /s/",
        "difficulty": "Beginner",
        "tip": "Place the tip of your tongue lightly between your upper and lower teeth and blow air gently for 'think'. For 'sink', keep your tongue behind closed teeth."
    },
    {
        "target_text": "three vs tree",
        "item_type": "minimal_pair",
        "phonetic": "/θriː/ vs /triː/",
        "focus_sound": "/θ/ vs /t/",
        "difficulty": "Beginner",
        "tip": "Do not stop the air completely on 'three'. Let air flow through your teeth before releasing the 'r'."
    },
    {
        "target_text": "light vs right",
        "item_type": "minimal_pair",
        "phonetic": "/laɪt/ vs /raɪt/",
        "focus_sound": "/l/ vs /r/",
        "difficulty": "Beginner",
        "tip": "For /l/, the tip of your tongue touches the alveolar ridge behind your top teeth. For /r/, curl your tongue slightly back without touching the roof of your mouth."
    },
    {
        "target_text": "He asked, walked, and helped yesterday.",
        "item_type": "sentence",
        "phonetic": "/t/ ending: [æskt], [wɔːkt], [helpt]",
        "focus_sound": "Past tense -ed pronounced as /t/",
        "difficulty": "Intermediate",
        "tip": "After voiceless sounds like /k/, /p/, /s/, /ʃ/, /tʃ/, the past tense '-ed' is pronounced as a crisp /t/ sound, not /ɪd/."
    },
    {
        "target_text": "She decided, needed, and waited patiently.",
        "item_type": "sentence",
        "phonetic": "/ɪd/ ending: [dɪˈsaɪ.dɪd], [ˈniː.dɪd], [ˈweɪ.tɪd]",
        "focus_sound": "Past tense -ed pronounced as /ɪd/",
        "difficulty": "Intermediate",
        "tip": "Only verbs ending with the /t/ or /d/ sound take the extra syllable /ɪd/ (e.g. decided, waited)."
    },
    {
        "target_text": "I doubt there is a subtle island in the calm reservoir.",
        "item_type": "sentence",
        "phonetic": "Silent letters: 'b' in doubt/subtle, 's' in island, 'l' in calm",
        "focus_sound": "English Silent Letters",
        "difficulty": "Upper-Intermediate",
        "tip": "In 'doubt' and 'subtle', the 'b' is completely silent. In 'island', the 's' is silent. In 'calm', do not pronounce the 'l'."
    },
    {
        "target_text": "She sells seashells by the seashore.",
        "item_type": "tongue_twister",
        "phonetic": "/ʃ/ vs /s/ alternation",
        "focus_sound": "/ʃ/ (postalveolar) vs /s/ (alveolar)",
        "difficulty": "Intermediate",
        "tip": "Round your lips forward for /ʃ/ ('she', 'shells') and retract your lips wide into a smile for /s/ ('sells', 'seashore')."
    },
    {
        "target_text": "Consistent daily practice produces profound speaking fluency.",
        "item_type": "sentence",
        "phonetic": "Sentence stress and rhythm: Con-SIS-tent DAI-ly PRAC-tice pro-DU-ces pro-FOUND SPEA-king FLUEN-cy",
        "focus_sound": "Sentence Stress & Rhythm",
        "difficulty": "Upper-Intermediate",
        "tip": "Stress the content words (Consistent, daily, practice, profound, speaking, fluency) and glide smoothly over grammatical words."
    },
    {
        "target_text": "The thirty-three thieves thought that they thrilled the throne throughout Thursday.",
        "item_type": "tongue_twister",
        "phonetic": "/θ/ voiced and unvoiced mastery",
        "focus_sound": "/θ/ repetition",
        "difficulty": "Upper-Intermediate",
        "tip": "Maintain conscious tongue-to-teeth contact on every 'th' word: thirty-three, thieves, thought, thrilled, throne, throughout, Thursday."
    }
]

LISTENING_EXERCISES = [
    # Beginner 1
    {
        "title": "At the University Library",
        "difficulty_level": "Beginner",
        "topic_category": "Classroom conversations",
        "situation_description": "A new university student asks the campus librarian how to register for a library card and locate English reference textbooks.",
        "audio_script": """Librarian: Good morning! Welcome to the University Central Library. How may I assist you today?
Student: Good morning. I am a first-year student, and I would like to register for a library card.
Librarian: Wonderful! You will need your student ID card and a copy of your enrollment confirmation. Do you have those with you?
Student: Yes, here is my ID card and my enrollment form.
Librarian: Perfect. Your card is ready. You are allowed to borrow up to five books for two weeks at a time.
Student: Thank you very much! Could you also show me where the English grammar and vocabulary section is?
Librarian: Certainly. Walk straight past the computer lab, take the stairs to the second floor, and you will find Section B on your left.
Student: That is very clear. Thank you for your kind guidance!
Librarian: You are most welcome. Happy studying!""",
        "questions_json": json.dumps([
            {
                "type": "mcq",
                "question": "What documents does the student need to register for a library card?",
                "options": [
                    "A passport and utility bill",
                    "A student ID card and enrollment confirmation",
                    "A driver's license and money",
                    "A letter from the professor"
                ],
                "correct_answer": "A student ID card and enrollment confirmation",
                "explanation": "The librarian explicitly asked for: 'your student ID card and a copy of your enrollment confirmation'."
            },
            {
                "type": "mcq",
                "question": "How many books is the student allowed to borrow at one time?",
                "options": ["Two books", "Three books", "Five books", "Ten books"],
                "correct_answer": "Five books",
                "explanation": "The librarian said: 'You are allowed to borrow up to five books for two weeks at a time.'"
            },
            {
                "type": "true_false",
                "question": "The English grammar and vocabulary section is located on the ground floor next to the entrance.",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "The librarian said: 'take the stairs to the second floor, and you will find Section B on your left'."
            },
            {
                "type": "fill_blank",
                "question": "The student can borrow books for a duration of _______ weeks.",
                "options": ["two", "2"],
                "correct_answer": "two",
                "explanation": "The loan period is two weeks."
            }
        ]),
        "order_index": 1
    },
    # Beginner 2
    {
        "title": "Meeting a New Colleague",
        "difficulty_level": "Beginner",
        "topic_category": "Introductions",
        "situation_description": "Sophea meets John, an international volunteer teacher who has recently arrived in Cambodia.",
        "audio_script": """Sophea: Hello! My name is Sophea. It is a pleasure to meet you.
John: Hi Sophea! Nice to meet you too. I am John. I just arrived from Australia two days ago.
Sophea: Welcome to Cambodia, John! How are you adjusting to the weather here in Phnom Penh?
John: Well, it is much warmer and more humid than Melbourne, but I love the tropical sunshine!
Sophea: What subjects will you be teaching at our center?
John: I will be teaching beginner and intermediate conversational English, focusing especially on pronunciation and daily speaking confidence.
Sophea: That is fantastic! Our students are very eager to practice speaking with international teachers.
John: I cannot wait to start our first lesson on Monday morning.""",
        "questions_json": json.dumps([
            {
                "type": "mcq",
                "question": "Where did John travel from?",
                "options": ["Canada", "Australia", "The United Kingdom", "The United States"],
                "correct_answer": "Australia",
                "explanation": "John states: 'I just arrived from Australia two days ago.'"
            },
            {
                "type": "true_false",
                "question": "John will be teaching advanced mathematics and physics.",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "John said he will teach beginner and intermediate conversational English."
            },
            {
                "type": "fill_blank",
                "question": "John will begin his first teaching lesson on _______ morning.",
                "options": ["Monday", "monday"],
                "correct_answer": "Monday",
                "explanation": "John stated: 'I cannot wait to start our first lesson on Monday morning.'"
            }
        ]),
        "order_index": 2
    },
    # Intermediate 1
    {
        "title": "Healthy Living & Nutrition Habits",
        "difficulty_level": "Intermediate",
        "topic_category": "Healthy living",
        "situation_description": "A wellness counselor discusses the critical connection between sleep quality, hydration, and academic focus.",
        "audio_script": """Counselor: Good afternoon, students. Many learners ask me: 'Why do I struggle to concentrate during evening English grammar classes?' Often, the answer is not lack of intelligence, but poor lifestyle habits.
Student: Dr. Sarah, how much sleep do adult learners genuinely require to maintain peak mental performance?
Counselor: Most cognitive science research indicates that adults need between seven and eight hours of quality sleep each night. During deep sleep, your brain consolidates new vocabulary words and transfers them from short-term memory into long-term retention. If you sleep only five hours, your recall ability drops by nearly forty percent!
Student: What about drinking water and physical exercise?
Counselor: Dehydration causes fatigue, headaches, and sluggish thinking. I recommend drinking at least two liters of pure water daily. Furthermore, engaging in just thirty minutes of moderate exercise, such as brisk walking or cycling, boosts blood flow to your brain and immediately enhances alertness.""",
        "questions_json": json.dumps([
            {
                "type": "mcq",
                "question": "According to the counselor, what critical cognitive process happens during deep sleep?",
                "options": [
                    "The brain creates new muscles",
                    "The brain consolidates new vocabulary and transfers it into long-term memory",
                    "The brain forgets unnecessary grammar rules",
                    "The brain rests without any activity"
                ],
                "correct_answer": "The brain consolidates new vocabulary and transfers it into long-term memory",
                "explanation": "The counselor stated: 'During deep sleep, your brain consolidates new vocabulary words and transfers them from short-term memory into long-term retention.'"
            },
            {
                "type": "true_false",
                "question": "Sleeping only five hours a night has virtually no measurable impact on vocabulary recall.",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "The counselor noted that recall ability drops by nearly 40% when sleeping only five hours."
            },
            {
                "type": "fill_blank",
                "question": "The counselor recommends drinking at least _______ liters of pure water every day.",
                "options": ["two", "2"],
                "correct_answer": "two",
                "explanation": "The counselor explicitly recommends at least two liters of water daily."
            }
        ]),
        "order_index": 3
    },
    # Upper-Intermediate 1
    {
        "title": "Debating Remote Work vs Office Work",
        "difficulty_level": "Upper-intermediate",
        "topic_category": "Discussions & Opinions",
        "situation_description": "Two project managers engage in a structured debate examining the productivity advantages and interpersonal drawbacks of remote employment.",
        "audio_script": """Elena: In my view, full-time remote work has fundamentally revolutionized employee productivity. By eliminating arduous daily commutes in congested traffic, professionals save up to ten hours every week. They can utilize that reclaimed time for focused deep work, physical wellness, or continuing education like foreign language learning.
Marcus: While I acknowledge the commuting advantage, Elena, we cannot disregard the profound interpersonal deficits of total isolation. Spontaneous creative innovation rarely occurs in pre-scheduled video conference calls. It happens informally in hallway conversations, spontaneous whiteboard brainstorming sessions, and shared coffee breaks. Furthermore, junior employees often struggle to assimilate organizational culture without direct, physical mentorship.
Elena: That is a legitimate concern, Marcus. However, modern asynchronous collaboration platforms and well-structured virtual documentation can bridge that gap effectively. Companies that implement hybrid frameworks—requiring team presence only two days a week—enjoy the optimal balance of personal autonomy and collective synergy.
Marcus: I can certainly endorse a hybrid model. It honors individual flexibility while safeguarding the cohesion and camaraderie essential for long-term organizational health.""",
        "questions_json": json.dumps([
            {
                "type": "mcq",
                "question": "What primary advantage does Elena highlight regarding remote employment?",
                "options": [
                    "Employees receive higher corporate salaries",
                    "Reclaiming up to ten hours weekly by eliminating grueling commutes",
                    "Employees never have to interact with colleagues",
                    "Companies eliminate all office computers"
                ],
                "correct_answer": "Reclaiming up to ten hours weekly by eliminating grueling commutes",
                "explanation": "Elena emphasizes that eliminating arduous commutes saves up to ten hours a week for deep work and wellness."
            },
            {
                "type": "mcq",
                "question": "What is Marcus's main counter-argument against total remote work?",
                "options": [
                    "Internet bills are too expensive",
                    "The loss of spontaneous innovation and physical mentorship for junior team members",
                    "Workers dislike staying at home",
                    "Video calls have poor sound quality"
                ],
                "correct_answer": "The loss of spontaneous innovation and physical mentorship for junior team members",
                "explanation": "Marcus points out that spontaneous innovation occurs in informal physical interactions and junior staff need physical mentorship."
            },
            {
                "type": "true_false",
                "question": "Both Elena and Marcus agree that a hybrid work model provides a sensible middle ground.",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Elena proposes a hybrid model and Marcus responds: 'I can certainly endorse a hybrid model.'"
            },
            {
                "type": "fill_blank",
                "question": "In the proposed hybrid framework, team members would be physically present at the office _______ days each week.",
                "options": ["two", "2"],
                "correct_answer": "two",
                "explanation": "Elena specifies 'requiring team presence only two days a week'."
            }
        ]),
        "order_index": 4
    }
]

ACHIEVEMENTS = [
    {
        "slug": "first-steps",
        "title": "First Steps",
        "description": "Complete your very first grammar lesson and quiz.",
        "badge_icon": "fas fa-shoe-prints",
        "category": "Grammar",
        "requirement_type": "grammar_lessons_completed",
        "target_value": 1
    },
    {
        "slug": "grammar-explorer",
        "title": "Grammar Explorer",
        "description": "Complete five grammar lessons with quiz mastery.",
        "badge_icon": "fas fa-compass",
        "category": "Grammar",
        "requirement_type": "grammar_lessons_completed",
        "target_value": 5
    },
    {
        "slug": "grammar-master",
        "title": "Grammar Master",
        "description": "Complete all ten core grammar modules on the platform.",
        "badge_icon": "fas fa-crown",
        "category": "Grammar",
        "requirement_type": "grammar_lessons_completed",
        "target_value": 10
    },
    {
        "slug": "word-starter",
        "title": "Word Starter",
        "description": "Review at least 10 vocabulary words with spaced repetition.",
        "badge_icon": "fas fa-book-open",
        "category": "Vocabulary",
        "requirement_type": "vocab_reviewed",
        "target_value": 10
    },
    {
        "slug": "word-collector",
        "title": "Word Collector",
        "description": "Learn and review 50 vocabulary flashcards.",
        "badge_icon": "fas fa-gem",
        "category": "Vocabulary",
        "requirement_type": "vocab_reviewed",
        "target_value": 50
    },
    {
        "slug": "confident-speaker",
        "title": "Confident Speaker",
        "description": "Complete practice presentations for all four speaking topics.",
        "badge_icon": "fas fa-microphone-alt",
        "category": "Speaking",
        "requirement_type": "speaking_topics_completed",
        "target_value": 4
    },
    {
        "slug": "voice-prodigy",
        "title": "Voice Prodigy",
        "description": "Record and save 5 speech submissions in the platform.",
        "badge_icon": "fas fa-podcast",
        "category": "Speaking",
        "requirement_type": "speaking_submissions_total",
        "target_value": 5
    },
    {
        "slug": "sharp-listener",
        "title": "Sharp Listener",
        "description": "Complete at least 3 listening comprehension exercises.",
        "badge_icon": "fas fa-headphones-alt",
        "category": "Listening",
        "requirement_type": "listening_completed",
        "target_value": 3
    },
    {
        "slug": "mistake-conqueror",
        "title": "Mistake Conqueror",
        "description": "Review and mark 5 mistakes as 'Understood' in your notebook.",
        "badge_icon": "fas fa-check-double",
        "category": "Mistakes",
        "requirement_type": "mistakes_understood",
        "target_value": 5
    },
    {
        "slug": "writing-artisan",
        "title": "Writing Artisan",
        "description": "Draft and analyze 3 written passages in the Writing Workshop.",
        "badge_icon": "fas fa-pen-nib",
        "category": "Writing",
        "requirement_type": "writing_drafts_total",
        "target_value": 3
    },
    {
        "slug": "consistency",
        "title": "Consistency",
        "description": "Maintain an uninterrupted 7-day study streak.",
        "badge_icon": "fas fa-fire",
        "category": "Dedication",
        "requirement_type": "streak_days",
        "target_value": 7
    },
    {
        "slug": "placement-pioneer",
        "title": "Placement Pioneer",
        "description": "Complete the English Placement Test diagnostic assessment.",
        "badge_icon": "fas fa-graduation-cap",
        "category": "Placement",
        "requirement_type": "placement_test_completed",
        "target_value": 1
    }
]

def seed_all_data(db):
    """Inserts foundational educational data idempotently."""
    cursor = db.cursor()
    
    # 1. Grammar Lessons & Quizzes
    for lesson_data in GRAMMAR_LESSONS:
        cursor.execute("SELECT id FROM grammar_lessons WHERE slug = ?", (lesson_data['slug'],))
        existing = cursor.fetchone()
        if not existing:
            cursor.execute("""
                INSERT INTO grammar_lessons (slug, title, category, cefr_level, order_index, summary, formula, explanation_markdown, examples_json, common_mistakes_json, tips)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lesson_data['slug'], lesson_data['title'], lesson_data['category'], lesson_data['cefr_level'],
                lesson_data['order_index'], lesson_data['summary'], lesson_data['formula'],
                lesson_data['explanation_markdown'], lesson_data['examples_json'],
                lesson_data['common_mistakes_json'], lesson_data['tips']
            ))
            lesson_id = cursor.lastrowid
            
            # Quizzes
            for q in lesson_data.get('quizzes', []):
                cursor.execute("""
                    INSERT INTO grammar_quizzes (lesson_id, question, options_json, correct_answer, explanation, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    lesson_id, q['question'], json.dumps(q['options']), q['correct_answer'], q['explanation'], lesson_data['category']
                ))

    # 2. Speaking Topics
    for st in SPEAKING_TOPICS:
        cursor.execute("SELECT id FROM speaking_topics WHERE topic_number = ?", (st['topic_number'],))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO speaking_topics (topic_number, title, subtitle, duration_target, overview, structure_json, vocabulary_json, transition_phrases_json, sample_speech, guiding_questions_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                st['topic_number'], st['title'], st['subtitle'], st['duration_target'],
                st['overview'], st['structure_json'], st['vocabulary_json'],
                st['transition_phrases_json'], st['sample_speech'], st['guiding_questions_json']
            ))

    # 3. Vocabulary
    for v in VOCABULARY_ITEMS:
        cursor.execute("SELECT id FROM vocabulary WHERE word = ?", (v['word'],))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO vocabulary (word, part_of_speech, phonetic, definition_en, definition_km, example_sentence, difficulty_level, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                v['word'], v['pos'], v['phonetic'], v['definition_en'],
                v['definition_km'], v['example_sentence'], v['difficulty_level'], v['category']
            ))

    # 4. Pronunciation Items
    cursor.execute("SELECT COUNT(*) as count FROM pronunciation_items")
    if cursor.fetchone()['count'] == 0:
        for p in PRONUNCIATION_ITEMS:
            cursor.execute("""
                INSERT INTO pronunciation_items (target_text, item_type, phonetic, focus_sound, difficulty, tip)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (p['target_text'], p['item_type'], p['phonetic'], p['focus_sound'], p['difficulty'], p['tip']))

    # 5. Listening Exercises
    for le in LISTENING_EXERCISES:
        cursor.execute("SELECT id FROM listening_exercises WHERE title = ?", (le['title'],))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO listening_exercises (title, difficulty_level, topic_category, situation_description, audio_script, questions_json, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                le['title'], le['difficulty_level'], le['topic_category'],
                le['situation_description'], le['audio_script'], le['questions_json'], le['order_index']
            ))

    # 6. Achievements
    for ach in ACHIEVEMENTS:
        cursor.execute("SELECT id FROM achievements WHERE slug = ?", (ach['slug'],))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO achievements (slug, title, description, badge_icon, category, requirement_type, target_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ach['slug'], ach['title'], ach['description'],
                ach['badge_icon'], ach['category'], ach['requirement_type'], ach['target_value']
            ))

    db.commit()
