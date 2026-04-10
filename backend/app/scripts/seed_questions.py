"""
Скрипт для заполнения базы данных вопросами
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db import SessionLocal
from backend.app.models.question import Question

# Создаем вопросы для разных режимов и сложностей
questions_data = [
    # Режим "Столицы" - Легкий
    {"question_text": "Париж - столица какой страны?", "target_type": "capital", "target_name": "Франция", "correct_lat": 48.8566, "correct_lng": 2.3522, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Лондон - столица какой страны?", "target_type": "capital", "target_name": "Великобритания", "correct_lat": 51.5074, "correct_lng": -0.1278, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Берлин - столица какой страны?", "target_type": "capital", "target_name": "Германия", "correct_lat": 52.5200, "correct_lng": 13.4050, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Рим - столица какой страны?", "target_type": "capital", "target_name": "Италия", "correct_lat": 41.9028, "correct_lng": 12.4964, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Мадрид - столица какой страны?", "target_type": "capital", "target_name": "Испания", "correct_lat": 40.4168, "correct_lng": -3.7038, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Токио - столица какой страны?", "target_type": "capital", "target_name": "Япония", "correct_lat": 35.6762, "correct_lng": 139.6503, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Москва - столица какой страны?", "target_type": "capital", "target_name": "Россия", "correct_lat": 55.7558, "correct_lng": 37.6173, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Пекин - столица какой страны?", "target_type": "capital", "target_name": "Китай", "correct_lat": 39.9042, "correct_lng": 116.4074, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Вашингтон - столица какой страны?", "target_type": "capital", "target_name": "США", "correct_lat": 38.9072, "correct_lng": -77.0369, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Оттава - столица какой страны?", "target_type": "capital", "target_name": "Канада", "correct_lat": 45.4215, "correct_lng": -75.6972, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Вена - столица какой страны?", "target_type": "capital", "target_name": "Австрия", "correct_lat": 48.2082, "correct_lng": 16.3738, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Афины - столица какой страны?", "target_type": "capital", "target_name": "Греция", "correct_lat": 37.9838, "correct_lng": 23.7275, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Прага - столица какой страны?", "target_type": "capital", "target_name": "Чехия", "correct_lat": 50.0755, "correct_lng": 14.4378, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Будапешт - столица какой страны?", "target_type": "capital", "target_name": "Венгрия", "correct_lat": 47.4979, "correct_lng": 19.0402, "mode": "capitals", "difficulty": "easy", "is_active": True},
    {"question_text": "Стокгольм - столица какой страны?", "target_type": "capital", "target_name": "Швеция", "correct_lat": 59.3293, "correct_lng": 18.0686, "mode": "capitals", "difficulty": "easy", "is_active": True},
    
    # Режим "Столицы" - Средний
    {"question_text": "Осло - столица какой страны?", "target_type": "capital", "target_name": "Норвегия", "correct_lat": 59.9139, "correct_lng": 10.7522, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Копенгаген - столица какой страны?", "target_type": "capital", "target_name": "Дания", "correct_lat": 55.6761, "correct_lng": 12.5683, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Хельсинки - столица какой страны?", "target_type": "capital", "target_name": "Финляндия", "correct_lat": 60.1699, "correct_lng": 24.9384, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Дублин - столица какой страны?", "target_type": "capital", "target_name": "Ирландия", "correct_lat": 53.3498, "correct_lng": -6.2603, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Варшава - столица какой страны?", "target_type": "capital", "target_name": "Польша", "correct_lat": 52.2297, "correct_lng": 21.0122, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Киев - столица какой страны?", "target_type": "capital", "target_name": "Украина", "correct_lat": 50.4501, "correct_lng": 30.5234, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Стамбул - столица какой страны?", "target_type": "capital", "target_name": "Турция", "correct_lat": 41.0082, "correct_lng": 28.9784, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Каир - столица какой страны?", "target_type": "capital", "target_name": "Египет", "correct_lat": 30.0444, "correct_lng": 31.2357, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Нью-Дели - столица какой страны?", "target_type": "capital", "target_name": "Индия", "correct_lat": 28.6139, "correct_lng": 77.2090, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Бангкок - столица какой страны?", "target_type": "capital", "target_name": "Таиланд", "correct_lat": 13.7563, "correct_lng": 100.5018, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Сеул - столица какой страны?", "target_type": "capital", "target_name": "Южная Корея", "correct_lat": 37.5665, "correct_lng": 126.9780, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Канберра - столица какой страны?", "target_type": "capital", "target_name": "Австралия", "correct_lat": -35.2809, "correct_lng": 149.1300, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Веллингтон - столица какой страны?", "target_type": "capital", "target_name": "Новая Зеландия", "correct_lat": -41.2866, "correct_lng": 174.7762, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Буэнос-Айрес - столица какой страны?", "target_type": "capital", "target_name": "Аргентина", "correct_lat": -34.6037, "correct_lng": -58.3816, "mode": "capitals", "difficulty": "medium", "is_active": True},
    {"question_text": "Бразилиа - столица какой страны?", "target_type": "capital", "target_name": "Бразилия", "correct_lat": -15.7975, "correct_lng": -47.8919, "mode": "capitals", "difficulty": "medium", "is_active": True},

    # Режим "Столицы" - Сложный
    {"question_text": "Никосия - столица какой страны?", "target_type": "capital", "target_name": "Кипр", "correct_lat": 35.1856, "correct_lng": 33.3823, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Рейкьявик - столица какой страны?", "target_type": "capital", "target_name": "Исландия", "correct_lat": 64.1466, "correct_lng": -21.9426, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Таллин - столица какой страны?", "target_type": "capital", "target_name": "Эстония", "correct_lat": 59.4370, "correct_lng": 24.7536, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Рига - столица какой страны?", "target_type": "capital", "target_name": "Латвия", "correct_lat": 56.9496, "correct_lng": 24.1052, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Вильнюс - столица какой страны?", "target_type": "capital", "target_name": "Литва", "correct_lat": 54.6872, "correct_lng": 25.2797, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Загреб - столица какой страны?", "target_type": "capital", "target_name": "Хорватия", "correct_lat": 45.8150, "correct_lng": 15.9819, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Любляна - столица какой страны?", "target_type": "capital", "target_name": "Словения", "correct_lat": 46.0569, "correct_lng": 14.5058, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Братислава - столица какой страны?", "target_type": "capital", "target_name": "Словакия", "correct_lat": 48.1486, "correct_lng": 17.1077, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Подгорица - столица какой страны?", "target_type": "capital", "target_name": "Черногория", "correct_lat": 42.4304, "correct_lng": 19.2594, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Тбилиси - столица какой страны?", "target_type": "capital", "target_name": "Грузия", "correct_lat": 41.7151, "correct_lng": 44.8271, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Ереван - столица какой страны?", "target_type": "capital", "target_name": "Армения", "correct_lat": 40.1792, "correct_lng": 44.4991, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Баку - столица какой страны?", "target_type": "capital", "target_name": "Азербайджан", "correct_lat": 40.4093, "correct_lng": 49.8671, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Нукуалофа - столица какой страны?", "target_type": "capital", "target_name": "Тонга", "correct_lat": -21.1393, "correct_lng": -175.2170, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Паликир - столица какой страны?", "target_type": "capital", "target_name": "Микронезия", "correct_lat": 6.9248, "correct_lng": 158.1610, "mode": "capitals", "difficulty": "hard", "is_active": True},
    {"question_text": "Ярен - столица какой страны?", "target_type": "capital", "target_name": "Науру", "correct_lat": -0.5228, "correct_lng": 166.9315, "mode": "capitals", "difficulty": "hard", "is_active": True},

    # Режим "Страны" - Легкий
    {"question_text": "Где находится Эйфелева башня?", "target_type": "country", "target_name": "Франция", "correct_lat": 48.8584, "correct_lng": 2.2945, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Колизей?", "target_type": "country", "target_name": "Италия", "correct_lat": 41.8902, "correct_lng": 12.4922, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Биг-Бен?", "target_type": "country", "target_name": "Великобритания", "correct_lat": 51.5007, "correct_lng": -0.1246, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Статуя Свободы?", "target_type": "country", "target_name": "США", "correct_lat": 40.6892, "correct_lng": -74.0445, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Рейхстаг?", "target_type": "country", "target_name": "Германия", "correct_lat": 52.5186, "correct_lng": 13.3761, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Тадж-Махал?", "target_type": "country", "target_name": "Индия", "correct_lat": 27.1751, "correct_lng": 78.0421, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Мачу-Пикчу?", "target_type": "country", "target_name": "Перу", "correct_lat": -13.1631, "correct_lng": -72.5450, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Пирамида Хеопса?", "target_type": "country", "target_name": "Египет", "correct_lat": 29.9792, "correct_lng": 31.1342, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Сиднейский оперный театр?", "target_type": "country", "target_name": "Австралия", "correct_lat": -33.8568, "correct_lng": 151.2153, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Токийская башня?", "target_type": "country", "target_name": "Япония", "correct_lat": 35.6586, "correct_lng": 139.7454, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Кремль?", "target_type": "country", "target_name": "Россия", "correct_lat": 55.7520, "correct_lng": 37.6175, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Эйфелева башня?", "target_type": "country", "target_name": "Франция", "correct_lat": 48.8584, "correct_lng": 2.2945, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Собор Святого Петра?", "target_type": "country", "target_name": "Ватикан", "correct_lat": 41.9022, "correct_lng": 12.4539, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Запретный город?", "target_type": "country", "target_name": "Китай", "correct_lat": 39.9163, "correct_lng": 116.3972, "mode": "countries", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Храм Василия Блаженного?", "target_type": "country", "target_name": "Россия", "correct_lat": 55.7539, "correct_lng": 37.6208, "mode": "countries", "difficulty": "easy", "is_active": True},

    # Режим "Страны" - Средний
    {"question_text": "Где находится Гранд-Каньон?", "target_type": "country", "target_name": "США", "correct_lat": 36.0544, "correct_lng": -112.1401, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Башня Бурдж-Халифа?", "target_type": "country", "target_name": "ОАЭ", "correct_lat": 25.1972, "correct_lng": 55.2744, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Петра?", "target_type": "country", "target_name": "Иордания", "correct_lat": 30.3285, "correct_lng": 35.4444, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Ангкор-Ват?", "target_type": "country", "target_name": "Камбоджа", "correct_lat": 13.4125, "correct_lng": 103.8670, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Шанхайская башня?", "target_type": "country", "target_name": "Китай", "correct_lat": 31.2304, "correct_lng": 121.4737, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Миланский собор?", "target_type": "country", "target_name": "Италия", "correct_lat": 45.4642, "correct_lng": 9.1900, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Остров Свободы?", "target_type": "country", "target_name": "Куба", "correct_lat": 23.1136, "correct_lng": -82.3666, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Трафальгарская площадь?", "target_type": "country", "target_name": "Великобритания", "correct_lat": 51.5081, "correct_lng": -0.1281, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Пизанская башня?", "target_type": "country", "target_name": "Италия", "correct_lat": 43.7230, "correct_lng": 10.3966, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Долина царей?", "target_type": "country", "target_name": "Египет", "correct_lat": 25.7402, "correct_lng": 32.6014, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Оперный театр Сиднея?", "target_type": "country", "target_name": "Австралия", "correct_lat": -33.8568, "correct_lng": 151.2153, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Космическая игла?", "target_type": "country", "target_name": "Япония", "correct_lat": 35.6297, "correct_lng": 139.7941, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Мечеть шейха Зайда?", "target_type": "country", "target_name": "ОАЭ", "correct_lat": 24.4125, "correct_lng": 54.4741, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Римский форум?", "target_type": "country", "target_name": "Италия", "correct_lat": 41.8925, "correct_lng": 12.4853, "mode": "countries", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Плато Улуру?", "target_type": "country", "target_name": "Австралия", "correct_lat": -25.3444, "correct_lng": 131.0369, "mode": "countries", "difficulty": "medium", "is_active": True},

    # Режим "Страны" - Сложный
    {"question_text": "Где находится Карнакский храм?", "target_type": "country", "target_name": "Египет", "correct_lat": 25.6872, "correct_lng": 32.6565, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Чжуншань?", "target_type": "country", "target_name": "Китай", "correct_lat": 32.3632, "correct_lng": 119.1352, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Остров Аруба?", "target_type": "country", "target_name": "Аруба", "correct_lat": 12.5211, "correct_lng": -69.9683, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Калгари?", "target_type": "country", "target_name": "Канада", "correct_lat": 51.0447, "correct_lng": -114.0719, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Гданьск?", "target_type": "country", "target_name": "Польша", "correct_lat": 54.3520, "correct_lng": 18.6466, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Марианская впадина?", "target_type": "country", "target_name": "Тихий океан", "correct_lat": 11.3493, "correct_lng": 142.1996, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Кхерм?" , "target_type": "country", "target_name": "Камбоджа", "correct_lat": 13.3674, "correct_lng": 103.8442, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится город Хойан?", "target_type": "country", "target_name": "Вьетнам", "correct_lat": 15.8794, "correct_lng": 108.3381, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Томбуктю?", "target_type": "country", "target_name": "Мали", "correct_lat": 16.8661, "correct_lng": -3.0026, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится город Уюни?", "target_type": "country", "target_name": "Боливия", "correct_lat": -20.1344, "correct_lng": -67.4891, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Национальный парк Катманду?", "target_type": "country", "target_name": "Непал", "correct_lat": 27.8500, "correct_lng": 86.0500, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится город Бразилиа?", "target_type": "country", "target_name": "Бразилия", "correct_lat": -15.7975, "correct_lng": -47.8919, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится остров Крит?", "target_type": "country", "target_name": "Греция", "correct_lat": 35.2401, "correct_lng": 25.4300, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится город Гранада?", "target_type": "country", "target_name": "Испания", "correct_lat": 37.1773, "correct_lng": -3.5986, "mode": "countries", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Сидней?", "target_type": "country", "target_name": "Австралия", "correct_lat": -33.8688, "correct_lng": 151.2093, "mode": "countries", "difficulty": "hard", "is_active": True},

    # Режим "Достопримечательности" - Легкий
    {"question_text": "Где находится Эйфелева башня?", "target_type": "landmark", "target_name": "Эйфелева башня", "correct_lat": 48.8584, "correct_lng": 2.2945, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Статуя Свободы?", "target_type": "landmark", "target_name": "Статуя Свободы", "correct_lat": 40.6892, "correct_lng": -74.0445, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Тадж-Махал?", "target_type": "landmark", "target_name": "Тадж-Махал", "correct_lat": 27.1751, "correct_lng": 78.0421, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Биг-Бен?", "target_type": "landmark", "target_name": "Биг-Бен", "correct_lat": 51.5007, "correct_lng": -0.1246, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Пирамида Хеопса?", "target_type": "landmark", "target_name": "Пирамида Хеопса", "correct_lat": 29.9792, "correct_lng": 31.1342, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Колизей?", "target_type": "landmark", "target_name": "Колизей", "correct_lat": 41.8902, "correct_lng": 12.4922, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Сиднейский оперный театр?", "target_type": "landmark", "target_name": "Сиднейский оперный театр", "correct_lat": -33.8568, "correct_lng": 151.2153, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Мачу-Пикчу?", "target_type": "landmark", "target_name": "Мачу-Пикчу", "correct_lat": -13.1631, "correct_lng": -72.5450, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Кремль?", "target_type": "landmark", "target_name": "Кремль", "correct_lat": 55.7520, "correct_lng": 37.6175, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Токийская башня?", "target_type": "landmark", "target_name": "Токийская башня", "correct_lat": 35.6586, "correct_lng": 139.7454, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Пизанская башня?", "target_type": "landmark", "target_name": "Пизанская башня", "correct_lat": 43.7230, "correct_lng": 10.3966, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Храм Василия Блаженного?", "target_type": "landmark", "target_name": "Храм Василия Блаженного", "correct_lat": 55.7539, "correct_lng": 37.6208, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Запретный город?", "target_type": "landmark", "target_name": "Запретный город", "correct_lat": 39.9163, "correct_lng": 116.3972, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Мост Золотые ворота?", "target_type": "landmark", "target_name": "Мост Золотые ворота", "correct_lat": 37.8199, "correct_lng": -122.4783, "mode": "landmarks", "difficulty": "easy", "is_active": True},
    {"question_text": "Где находится Собор Святого Петра?", "target_type": "landmark", "target_name": "Собор Святого Петра", "correct_lat": 41.9022, "correct_lng": 12.4539, "mode": "landmarks", "difficulty": "easy", "is_active": True},

    # Режим "Достопримечательности" - Средний
    {"question_text": "Где находится Гранд-Каньон?", "target_type": "landmark", "target_name": "Гранд-Каньон", "correct_lat": 36.0544, "correct_lng": -112.1401, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Башня Бурдж-Халифа?", "target_type": "landmark", "target_name": "Башня Бурдж-Халифа", "correct_lat": 25.1972, "correct_lng": 55.2744, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Петра?", "target_type": "landmark", "target_name": "Петра", "correct_lat": 30.3285, "correct_lng": 35.4444, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Ангкор-Ват?", "target_type": "landmark", "target_name": "Ангкор-Ват", "correct_lat": 13.4125, "correct_lng": 103.8670, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Эверест?", "target_type": "landmark", "target_name": "Эверест", "correct_lat": 27.9881, "correct_lng": 86.9250, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Ниагарский водопад?", "target_type": "landmark", "target_name": "Ниагарский водопад", "correct_lat": 43.0962, "correct_lng": -79.0377, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Водопад Виктория?", "target_type": "landmark", "target_name": "Водопад Виктория", "correct_lat": -17.9243, "correct_lng": 25.8567, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Айя-София?", "target_type": "landmark", "target_name": "Айя-София", "correct_lat": 41.0086, "correct_lng": 28.9802, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Шанхайская башня?", "target_type": "landmark", "target_name": "Шанхайская башня", "correct_lat": 31.2304, "correct_lng": 121.4737, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Римский Колизей?", "target_type": "landmark", "target_name": "Римский Колизей", "correct_lat": 41.8902, "correct_lng": 12.4922, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Эйфелева башня?", "target_type": "landmark", "target_name": "Эйфелева башня", "correct_lat": 48.8584, "correct_lng": 2.2945, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Храм Солнца?", "target_type": "landmark", "target_name": "Храм Солнца", "correct_lat": -13.4942, "correct_lng": -71.9672, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Монастырь Такцанг?", "target_type": "landmark", "target_name": "Монастырь Такцанг", "correct_lat": 27.4881, "correct_lng": 89.2708, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Капелла Сикстинская?", "target_type": "landmark", "target_name": "Капелла Сикстинская", "correct_lat": 41.9029, "correct_lng": 12.4545, "mode": "landmarks", "difficulty": "medium", "is_active": True},
    {"question_text": "Где находится Прага?", "target_type": "landmark", "target_name": "Пражская площадь", "correct_lat": 50.0875, "correct_lng": 14.4214, "mode": "landmarks", "difficulty": "medium", "is_active": True},

    # Режим "Достопримечательности" - Сложный
    {"question_text": "Где находится Башня Крейсерская?", "target_type": "landmark", "target_name": "Башня Крейсерская", "correct_lat": 55.7520, "correct_lng": 37.6175, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Стоунхендж?", "target_type": "landmark", "target_name": "Стоунхендж", "correct_lat": 51.1789, "correct_lng": -1.8262, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Гора Килиманджаро?", "target_type": "landmark", "target_name": "Гора Килиманджаро", "correct_lat": -3.0674, "correct_lng": 37.3556, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Остров Пасхи?", "target_type": "landmark", "target_name": "Остров Пасхи", "correct_lat": -27.1127, "correct_lng": -109.3497, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Эребус?", "target_type": "landmark", "target_name": "Вулкан Эребус", "correct_lat": -77.5258, "correct_lng": 167.1533, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Озеро Байкал?", "target_type": "landmark", "target_name": "Озеро Байкал", "correct_lat": 53.5000, "correct_lng": 108.0000, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Залив Халонг?", "target_type": "landmark", "target_name": "Залив Халонг", "correct_lat": 20.9101, "correct_lng": 107.1971, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Вади-Рам?", "target_type": "landmark", "target_name": "Вади-Рам", "correct_lat": 29.5726, "correct_lng": 35.4208, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Метеоры?", "target_type": "landmark", "target_name": "Метеоры", "correct_lat": 39.7217, "correct_lng": 21.6306, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Каппадокия?", "target_type": "landmark", "target_name": "Каппадокия", "correct_lat": 38.6431, "correct_lng": 34.8289, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Плитвицкие озёра?", "target_type": "landmark", "target_name": "Плитвицкие озёра", "correct_lat": 44.8654, "correct_lng": 15.5820, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Гёреме?", "target_type": "landmark", "target_name": "Гёреме", "correct_lat": 38.6428, "correct_lng": 34.8301, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Намчхон?", "target_type": "landmark", "target_name": "Намчхон", "correct_lat": 27.4265, "correct_lng": 89.0883, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Висячие сады Семирамиды?", "target_type": "landmark", "target_name": "Висячие сады", "correct_lat": 32.5361, "correct_lng": 44.4275, "mode": "landmarks", "difficulty": "hard", "is_active": True},
    {"question_text": "Где находится Акрополь?", "target_type": "landmark", "target_name": "Акрополь", "correct_lat": 37.9715, "correct_lng": 23.7257, "mode": "landmarks", "difficulty": "hard", "is_active": True},
]

def seed_questions():
    db = SessionLocal()
    try:
        # Удаляем существующие вопросы
        db.query(Question).delete()
        db.commit()
        
        # Добавляем новые вопросы
        for q_data in questions_data:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        print(f"Успешно добавлено {len(questions_data)} вопросов в базу данных!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()