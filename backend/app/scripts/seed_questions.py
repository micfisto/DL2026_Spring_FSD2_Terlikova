from backend.app.models.question import Question
from sqlalchemy import text
from sqlalchemy.orm import Session

CAPITALS = {
    "easy": {
        "Франция": ("Париж", 48.8566, 2.3522),
        "Германия": ("Берлин", 52.52, 13.405),
        "Италия": ("Рим", 41.9028, 12.4964),
        "Япония": ("Токио", 35.6762, 139.6503),
        "США": ("Вашингтон", 38.9072, -77.0369),
        "Великобритания": ("Лондон", 51.5072, -0.1276),
        "Испания": ("Мадрид", 40.4168, -3.7038),
        "Канада": ("Оттава", 45.4215, -75.6972),
        "Бразилия": ("Бразилиа", -15.8267, -47.9218),
        "Австралия": ("Канберра", -35.2809, 149.13),
    },
    "medium": {
        "Норвегия": ("Осло", 59.9139, 10.7522),
        "Польша": ("Варшава", 52.2297, 21.0122),
        "Таиланд": ("Бангкок", 13.7563, 100.5018),
        "Турция": ("Анкара", 39.9334, 32.8597),
        "Аргентина": ("Буэнос-Айрес", -34.6037, -58.3816),
        "ЮАР": ("Претория", -25.7479, 28.2293),
        "Египет": ("Каир", 30.0444, 31.2357),
    },
    "hard": {
        "Исландия": ("Рейкьявик", 64.1466, -21.9426),
        "Словакия": ("Братислава", 48.1486, 17.1077),
        "Микронезия": ("Паликир", 6.9248, 158.1610),
        "Бутан": ("Тхимпху", 27.4728, 89.6390),
        "Мальта": ("Валлетта", 35.8989, 14.5146),
        "Люксембург": ("Люксембург", 49.6116, 6.1319),
        "Словения": ("Любляна", 46.0569, 14.5058),
    }
}

LANDMARKS = {
    "easy": [
        ("Эйфелева башня", "Франция", 48.8584, 2.2945),
        ("Статуя Свободы", "США", 40.6892, -74.0445),
        ("Колизей", "Италия", 41.8902, 12.4922),
        ("Биг-Бен", "Великобритания", 51.5007, -0.1246),
        ("Тадж-Махал", "Индия", 27.1751, 78.0421),
    ],
    "medium": [
        ("Ангкор-Ват", "Камбоджа", 13.4125, 103.8670),
        ("Петра", "Иордания", 30.3285, 35.4444),
        ("Мачу-Пикчу", "Перу", -13.1631, -72.5450),
        ("Саграда Фамилия", "Испания", 41.4036, 2.1744),
        ("Сиднейский оперный театр", "Австралия", -33.8568, 151.2153),
    ],
    "hard": [
        ("Монастырь Такцанг", "Бутан", 27.4881, 89.2708),
        ("Томбукту", "Мали", 16.8661, -3.0026),
        ("Остров Пасхи (моаи)", "Чили", -27.1127, -109.3497),
        ("Кейптаун Столовая гора", "ЮАР", -33.9628, 18.4098),
    ]
}


def generate_capitals():
    questions = []

    for difficulty, data in CAPITALS.items():
        for country, (capital, lat, lng) in data.items():
            questions.append({
                "question_text": f"{capital} — столица какой страны?",
                "target_type": "capital",
                "target_name": country,
                "correct_lat": lat,
                "correct_lng": lng,
                "mode": "capitals",
                "difficulty": difficulty,
                "is_active": True
            })

    return questions


def generate_countries():
    questions = []

    for difficulty, data in LANDMARKS.items():
        for name, country, lat, lng in data:
            questions.append({
                "question_text": f"В какой стране находится {name}?",
                "target_type": "country",
                "target_name": country,
                "correct_lat": lat,
                "correct_lng": lng,
                "mode": "countries",
                "difficulty": difficulty,
                "is_active": True
            })

    return questions


def generate_landmarks():
    questions = []

    for difficulty, data in LANDMARKS.items():
        for name, country, lat, lng in data:
            questions.append({
                "question_text": f"Найди на карте: {name}",
                "target_type": "landmark",
                "target_name": name,
                "correct_lat": lat,
                "correct_lng": lng,
                "mode": "landmarks",
                "difficulty": difficulty,
                "is_active": True
            })

    return questions


def generate_test_questions():
    """Generate test questions for UI edge cases."""
    return [
        {
            "question_text": "В какой стране находится очень длинное и специально перегруженное название достопримечательности, которое должно проверить, как интерфейс справляется с переполнением текста и переносами строк в карточке?",
            "target_type": "country",
            "target_name": "Япония",
            "correct_lat": 35.6762,
            "correct_lng": 139.6503,
            "mode": "countries",
            "difficulty": "medium",
            "is_active": True
        },
        {
            "question_text": "Где находится точка с экстремальными координатами?",
            "target_type": "landmark",
            "target_name": "Null Island",
            "correct_lat": 0.0,
            "correct_lng": 0.0,
            "mode": "landmarks",
            "difficulty": "easy",
            "is_active": True
        },
        {
            "question_text": "Где находится Сиднейский оперный театр?",
            "target_type": "landmark",
            "target_name": "Сиднейский оперный театр",
            "correct_lat": -33.8568,
            "correct_lng": 151.2153,
            "mode": "landmarks",
            "difficulty": "easy",
            "is_active": True
        },
        {
            "question_text": "Редактируемый тестовый вопрос (проверь edit flow)",
            "target_type": "country",
            "target_name": "Франция",
            "correct_lat": 48.8566,
            "correct_lng": 2.3522,
            "mode": "capitals",
            "difficulty": "hard",
            "is_active": True
        },
        {
            "question_text": "Скрытый вопрос для проверки состояния UI",
            "target_type": "capital",
            "target_name": "Германия",
            "correct_lat": 52.52,
            "correct_lng": 13.405,
            "mode": "capitals",
            "difficulty": "medium",
            "is_active": False
        },
    ]

def generate_all_questions():
    all_q = (
            generate_capitals() +
            generate_countries() +
            generate_landmarks() +
            generate_test_questions()
    )

    seen = set()
    unique = []

    for q in all_q:
        key = (q["question_text"], q["mode"])

        if key in seen:
            continue

        seen.add(key)
        unique.append(q)

    return unique


def seed_questions(db: Session, force_recreate: bool = False):
    """
    Seed questions with upsert logic.
    
    Args:
        db: Database session
        force_recreate: If True, deletes all existing questions before seeding.
                     If False (default), updates existing and adds new ones.
    """
    questions = generate_all_questions()

    if force_recreate:
        # Delete all existing questions (careful - this breaks foreign keys)
        db.execute(text("DELETE FROM session_questions"))
        db.execute(text("DELETE FROM answers"))
        db.execute(text("DELETE FROM questions"))
        print("Deleted all existing questions")
    else:
        # Get existing question texts for update check
        existing = db.query(Question).all()
        existing_map = {
            (q.question_text, q.mode): q 
            for q in existing
        }
        
        # Track which questions we've updated
        updated_texts = set()
        
        for q in questions:
            key = (q["question_text"], q["mode"])
            
            if key in existing_map:
                # Update existing question
                existing_q = existing_map[key]
                existing_q.target_type = q["target_type"]
                existing_q.target_name = q["target_name"]
                existing_q.correct_lat = q["correct_lat"]
                existing_q.correct_lng = q["correct_lng"]
                existing_q.difficulty = q["difficulty"]
                existing_q.is_active = q["is_active"]
                updated_texts.add(key)
            else:
                # Add new question
                db.add(Question(**q))
        
        # Optionally deactivate questions that are not in the seed data anymore
        # (commented out to preserve custom questions)
        # for key, q in existing_map.items():
        #     if key not in updated_texts:
        #         q.is_active = False
        
        print(f"Updated {len(updated_texts)} existing questions")

    # Add any new questions that weren't in the existing set
    if not force_recreate:
        existing_texts = db.query(Question).all()
        existing_keys = {(q.question_text, q.mode) for q in existing_texts}
        
        new_questions = [q for q in questions if (q["question_text"], q["mode"]) not in existing_keys]
        
        for q in new_questions:
            db.add(Question(**q))
        
        if new_questions:
            print(f"Added {len(new_questions)} new questions")

    db.commit()

    # Get final count
    total = db.query(Question).count()
    active = db.query(Question).filter_by(is_active=True).count()
    print(f"Total questions in DB: {total} (active: {active})")


if __name__ == "__main__":
    import sys
    
    force = "--force" in sys.argv or "-f" in sys.argv
    
    from backend.app.db import SessionLocal

    db = SessionLocal()
    try:
        seed_questions(db, force_recreate=force)
    finally:
        db.close()
