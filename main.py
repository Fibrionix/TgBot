import os
import telebot
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Подробные вопросы для теста (16 вопросов)
questions = [
    {
        "text": "1. После долгого рабочего дня вы предпочитаете:\n\n• Провести время с друзьями\n• Остаться дома в одиночестве",
        "options": ["С друзьями", "В одиночестве"],
        "scores": {"С друзьями": "E", "В одиночестве": "I"}
    },
    {
        "text": "2. При принятии важного решения вы больше доверяете:\n\n• Логике и фактам\n• Своим чувствам и интуиции",
        "options": ["Логике", "Чувствам"],
        "scores": {"Логике": "T", "Чувствам": "F"}
    },
    {
        "text": "3. В отпуске вы предпочитаете:\n\n• Четкий план на каждый день\n• Спонтанные решения",
        "options": ["План", "Спонтанность"],
        "scores": {"План": "J", "Спонтанность": "P"}
    },
    {
        "text": "4. В работе вы больше обращаете внимание на:\n\n• Конкретные детали\n• Общую картину и идеи",
        "options": ["Детали", "Общую картину"],
        "scores": {"Детали": "S", "Общую картину": "N"}
    },
    {
        "text": "5. На вечеринке вы обычно:\n\n• Активно общаетесь со многими людьми\n• Беседуете с 1-2 близкими друзьями",
        "options": ["Со многими", "С 1-2 друзьями"],
        "scores": {"Со многими": "E", "С 1-2 друзьями": "I"}
    },
    {
        "text": "6. При конфликте вы склонны:\n\n• Анализировать объективные факты\n• Учитывать чувства людей",
        "options": ["Анализировать факты", "Учитывать чувства"],
        "scores": {"Анализировать факты": "T", "Учитывать чувства": "F"}
    },
    {
        "text": "7. Ваши рабочие задачи обычно:\n\n• Четко распланированы\n• Выполняются по настроению",
        "options": ["Распланированы", "По настроению"],
        "scores": {"Распланированы": "J", "По настроению": "P"}
    },
    {
        "text": "8. Вы больше цените:\n\n• Практический опыт\n• Творческие идеи",
        "options": ["Практический опыт", "Творческие идеи"],
        "scores": {"Практический опыт": "S", "Творческие идеи": "N"}
    },
    {
        "text": "9. Новые знакомства даются вам:\n\n• Легко и естественно\n• Требуют усилий",
        "options": ["Легко", "Требуют усилий"],
        "scores": {"Легко": "E", "Требуют усилий": "I"}
    },
    {
        "text": "10. При критике вы сначала:\n\n• Анализируете ее справедливость\n• Ощущаете эмоциональную реакцию",
        "options": ["Анализирую", "Эмоционально реагирую"],
        "scores": {"Анализирую": "T", "Эмоционально реагирую": "F"}
    },
    {
        "text": "11. Ваши выходные обычно:\n\n• Распланированы заранее\n• Складываются спонтанно",
        "options": ["Распланированы", "Спонтанные"],
        "scores": {"Распланированы": "J", "Спонтанные": "P"}
    },
    {
        "text": "12. В обучении вам интереснее:\n\n• Конкретные факты и методы\n• Теории и концепции",
        "options": ["Факты и методы", "Теории и концепции"],
        "scores": {"Факты и методы": "S", "Теории и концепции": "N"}
    },
    {
        "text": "13. В большой компании вы чувствуете себя:\n\n• Бодрым и энергичным\n• Уставшим и перегруженным",
        "options": ["Энергичным", "Уставшим"],
        "scores": {"Энергичным": "E", "Уставшим": "I"}
    },
    {
        "text": "14. При выборе работы важнее:\n\n• Перспективы роста и зарплата\n• Атмосфера в коллективе",
        "options": ["Перспективы и зарплата", "Атмосфера в коллективе"],
        "scores": {"Перспективы и зарплата": "T", "Атмосфера в коллективе": "F"}
    },
    {
        "text": "15. При выполнении задач вы:\n\n• Завершаете одну задачу перед началом следующей\n• Работаете над несколькими задачами параллельно",
        "options": ["Одну задачу", "Несколько задач"],
        "scores": {"Одну задачу": "J", "Несколько задач": "P"}
    },
    {
        "text": "16. Вы чаще думаете о:\n\n• Реальном положении дел\n• Возможностях и перспективах",
        "options": ["Реальном положении", "Возможностях"],
        "scores": {"Реальном положении": "S", "Возможностях": "N"}
    }
]

# Хранилище состояния пользователей
user_states = {}

def create_test_keyboard():
    """Создает клавиатуру с кнопкой начала теста"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧠 Пройти тест личности")
    markup.add("ℹ️ О боте", "📊 Моя статистика")
    return markup

def create_cancel_keyboard():
    """Создает клавиатуру с кнопкой отмены теста"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("❌ Отменить тест")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я бот для определения типа личности по методике MBTI.\n\n"
        "Я помогу тебе лучше понять себя, твои сильные стороны и подходящие профессии!\n\n"
        "🎯 <b>Что я умею:</b>\n"
        "• Проводить подробный тест из 16 вопросов\n"
        "• Определять твой тип личности MBTI\n"
        "• Показывать сильные стороны и карьерные рекомендации\n\n"
        "Просто нажми кнопку ниже чтобы начать! 🚀"
    )
    
    bot.send_message(message.chat.id, welcome_text, 
                     parse_mode='HTML', 
                     reply_markup=create_test_keyboard())

@bot.message_handler(commands=['test'])
def start_test(message):
    start_test_handler(message)

def start_test_handler(message):
    """Обработчик начала теста"""
    user_id = message.from_user.id
    
    # Проверяем, не проходит ли пользователь уже тест
    if user_id in user_states:
        bot.send_message(message.chat.id, 
                        "⚠️ Ты уже проходишь тест! Продолжай отвечать на вопросы.",
                        reply_markup=create_cancel_keyboard())
        return
    
    user_states[user_id] = {
        'current_question': 0,
        'answers': [],
        'personality': '',
        'username': message.from_user.first_name
    }
    
    start_text = (
        f"Отлично, {message.from_user.first_name}! 🌟\n\n"
        "Сейчас я задам тебе 16 вопросов о твоих предпочтениях и поведении.\n\n"
        "📝 <b>Как проходить тест:</b>\n"
        "• Отвечай честно, не задумываясь слишком долго\n"
        "• Выбирай вариант, который больше соответствует тебе\n"
        "• Не пропускай вопросы для точного результата\n\n"
        "Готов начать? Поехали! 🚀"
    )
    
    bot.send_message(message.chat.id, start_text, 
                     parse_mode='HTML',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    
    # Задаем первый вопрос с небольшой задержкой
    import time
    time.sleep(2)
    ask_question(message, 0)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обрабатывает все сообщения от пользователя"""
    user_id = message.from_user.id
    
    # Если пользователь проходит тест
    if user_id in user_states and user_states[user_id]['current_question'] < len(questions):
        handle_test_message(message)
        return
    
    # Обработка текстовых команд от пользователя
    text = message.text.lower()
    
    if text in ['привет', 'hello', 'hi', 'хай', 'здаров', 'начать']:
        send_welcome(message)
    
    elif text in ['🧠 пройти тест личности', 'тест', 'пройти тест', 'начать тест']:
        start_test_handler(message)
    
    elif text in ['ℹ️ о боте', 'о боте', 'помощь', 'help']:
        show_help(message)
    
    elif text in ['📊 моя статистика', 'статистика']:
        show_statistics(message)
    
    elif text in ['❌ отменить тест', 'отменить', 'отмена']:
        cancel_test(message)
    
    else:
        # На любое другое сообщение предлагаем пройти тест
        suggest_test(message)

def suggest_test(message):
    """Предлагает пройти тест на любое сообщение пользователя"""
    suggest_text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я вижу, ты хочешь пообщаться! Я специализируюсь на тестировании личности.\n\n"
        "🎯 <b>Давай узнаем твой тип личности?</b>\n"
        "Всего 16 вопросов - и ты узнаешь много нового о себе!\n\n"
        "Нажми кнопку ниже чтобы начать тест! 🔍"
    )
    
    bot.send_message(message.chat.id, suggest_text,
                     parse_mode='HTML',
                     reply_markup=create_test_keyboard())

def handle_test_message(message):
    """Обрабатывает сообщения во время прохождения теста"""
    user_id = message.from_user.id
    current_question_idx = user_states[user_id]['current_question']
    
    # Обработка отмены теста
    if message.text == "❌ Отменить тест":
        cancel_test(message)
        return
    
    current_question = questions[current_question_idx]
    
    # Проверяем валидность ответа
    if message.text not in current_question["options"]:
        bot.send_message(message.chat.id, 
                        "⚠️ Пожалуйста, выбери один из предложенных вариантов ответа.",
                        reply_markup=create_cancel_keyboard())
        return
    
    # Сохраняем ответ
    user_states[user_id]['answers'].append(message.text)
    
    # Переходим к следующему вопросу
    next_question_idx = current_question_idx + 1
    ask_question(message, next_question_idx)

def ask_question(message, question_num):
    """Задает вопрос пользователю"""
    user_id = message.from_user.id
    
    if question_num < len(questions):
        # Обновляем текущий вопрос
        user_states[user_id]['current_question'] = question_num
        
        # Создаем клавиатуру с вариантами ответов
        markup = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True, 
            one_time_keyboard=True
        )
        
        for option in questions[question_num]["options"]:
            markup.add(option)
        
        # Добавляем кнопку отмены
        markup.add("❌ Отменить тест")
        
        # Показываем прогресс
        progress = f"Вопрос {question_num + 1} из {len(questions)}"
        progress_bar = "🟩" * (question_num + 1) + "⬜" * (len(questions) - question_num - 1)
        
        question_text = (
            f"📊 {progress}\n"
            f"{progress_bar}\n\n"
            f"{questions[question_num]['text']}"
        )
        
        bot.send_message(message.chat.id, question_text, reply_markup=markup)
    else:
        # Все вопросы пройдены
        calculate_result(message)

def calculate_result(message):
    """Расчет и вывод результатов"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        bot.send_message(message.chat.id, "Что-то пошло не так. Начни заново: /test")
        return
    
    answers = user_states[user_id]['answers']
    
    if len(answers) != len(questions):
        bot.send_message(message.chat.id, "Не все вопросы были отвечены. Начни заново: /test")
        return
    
    # Подсчет баллов для каждого признака
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    for i, answer in enumerate(answers):
        score_type = questions[i]["scores"][answer]
        scores[score_type] += 1
    
    # Определение типа личности
    personality = ""
    personality += "E" if scores["E"] > scores["I"] else "I"
    personality += "S" if scores["S"] > scores["N"] else "N"
    personality += "T" if scores["T"] > scores["F"] else "F"
    personality += "J" if scores["J"] > scores["P"] else "P"
    
    # Сохраняем тип личности в состоянии пользователя
    user_states[user_id]['personality'] = personality
    
    # Подробные описания типов личности
    type_descriptions = {
        "ISTJ": {
            "name": "📊 Администратор",
            "description": "Ответственный и организованный реалист. Ценит порядок, традиции и надежность.",
            "strengths": "Надежный, практичный, организованный, внимательный к деталям",
            "careers": "Бухгалтер, администратор, логист, аналитик"
        },
        "ISFJ": {
            "name": "🛡️ Защитник", 
            "description": "Преданный и заботливый помощник. Всегда готов поддержать близких.",
            "strengths": "Заботливый, ответственный, практичный, преданный",
            "careers": "Врач, учитель, социальный работник, библиотекарь"
        },
        "INFJ": {
            "name": "💭 Советчик",
            "description": "Глубокий и вдохновляющий идеалист. Стремится помочь другим реализовать потенциал.",
            "strengths": "Проницательный, творческий, принципиальный, страстный",
            "careers": "Психолог, писатель, архитектор, консультант"
        },
        "INTJ": {
            "name": "🎯 Стратег",
            "description": "Стратегический и независимый новатор. Видит возможности для улучшений везде.",
            "strengths": "Стратегический, независимый, решающий проблемы, уверенный",
            "careers": "Ученый, инженер, программист, предприниматель"
        },
        "ISTP": {
            "name": "🔧 Мастер",
            "description": "Прагматичный и смелый исследователь. Мастер в решении практических проблем.",
            "strengths": "Адаптивный, практичный, спонтанный, технически подкованный",
            "careers": "Инженер, механик, пилот, криминалист"
        },
        "ISFP": {
            "name": "🎨 Художник",
            "description": "Чуткий и гармоничный эстет. Ценит красоту и помогает другим.",
            "strengths": "Чуткий, творческий, гибкий, преданный",
            "careers": "Дизайнер, художник, музыкант, ветеринар"
        },
        "INFP": {
            "name": "🌟 Идеалист",
            "description": "Идеалистичный и творческий мечтатель. Ищет смысл во всем.",
            "strengths": "Творческий, идеалистичный, чуткий, преданный ценностям",
            "careers": "Писатель, психолог, дизайнер, активист"
        },
        "INTP": {
            "name": "🤔 Мыслитель",
            "description": "Логичный и любознательный философ. Постоянно ищет закономерности.",
            "strengths": "Аналитический, оригинальный, любознательный, независимый",
            "careers": "Ученый, математик, программист, философ"
        },
        "ESTP": {
            "name": "⚡ Делец",
            "description": "Энергичный и предприимчивый деятель. Живет настоящим моментом.",
            "strengths": "Энергичный, практичный, наблюдательный, адаптивный",
            "careers": "Предприниматель, продавец, маркетолог, спортсмен"
        },
        "ESFP": {
            "name": "🎭 Развлекатель",
            "description": "Жизнерадостный и спонтанный артист. Любит веселить других.",
            "strengths": "Энергичный, дружелюбный, практичный, спонтанный",
            "careers": "Актер, организатор мероприятий, учитель, консультант"
        },
        "ENFP": {
            "name": "💫 Вдохновитель",
            "description": "Энтузиастичный и креативный вдохновитель. Видит потенциал во всем.",
            "strengths": "Энергичный, творческий, общительный, оптимистичный",
            "careers": "Журналист, актер, консультант, предприниматель"
        },
        "ENTP": {
            "name": "💡 Полемист",
            "description": "Изобретательный и любознательный новатор. Обожает интеллектуальные дебаты.",
            "strengths": "Изобретательный, умный, энергичный, стратегический",
            "careers": "Изобретатель, предприниматель, юрист, консультант"
        },
        "ESTJ": {
            "name": "💪 Руководитель",
            "description": "Решительный и практичный организатор. Прекрасный администратор.",
            "strengths": "Организованный, практичный, ответственный, решительный",
            "careers": "Менеджер, администратор, судья, военный"
        },
        "ESFJ": {
            "name": "🤝 Помощник",
            "description": "Заботливый и общительный гармонизатор. Всегда помогает другим.",
            "strengths": "Заботливый, общительный, ответственный, практичный",
            "careers": "Учитель, медсестра, социальный работник, менеджер"
        },
        "ENFJ": {
            "name": "🗣️ Наставник",
            "description": "Харизматичный и убедительный лидер. Вдохновляет других на рост.",
            "strengths": "Харизматичный, убедительный, чуткий, организованный",
            "careers": "Учитель, психолог, политик, коуч"
        },
        "ENTJ": {
            "name": "👑 Командир",
            "description": "Решительный и стратегический лидер. Прирожденный руководитель.",
            "strengths": "Решительный, стратегический, уверенный, организованный",
            "careers": "CEO, юрист, консультант, инвестиционный банкир"
        }
    }
    
    result = type_descriptions.get(personality, {
        "name": "🤔 Уникальная личность",
        "description": "Ваша личность уникальна и не поддается стандартной классификации!",
        "strengths": "Разносторонний, адаптивный, уникальный",
        "careers": "Любая сфера, где можно проявить многогранность"
    })
    
    # Формируем подробный результат
    markup = create_test_keyboard()
    
    result_message = (
        f"🎉 **ТВОЙ РЕЗУЛЬТАТ ТЕСТА** 🎉\n\n"
        f"**Тип личности:** {personality}\n"
        f"**Название:** {result['name']}\n\n"
        f"**📝 Описание:**\n{result['description']}\n\n"
        f"**💪 Сильные стороны:**\n{result['strengths']}\n\n"
        f"**💼 Подходящие профессии:**\n{result['careers']}\n\n"
        f"**📊 Ваши баллы:**\n"
        f"Экстраверсия (E): {scores['E']} | Интроверсия (I): {scores['I']}\n"
        f"Сенсорика (S): {scores['S']} | Интуиция (N): {scores['N']}\n"
        f"Мышление (T): {scores['T']} | Чувство (F): {scores['F']}\n"
        f"Суждение (J): {scores['J']} | Восприятие (P): {scores['P']}\n\n"
        f"Спасибо за прохождение теста! ✨\n"
        f"Хочешь пройти еще раз или узнать больше о своем типе?"
    )
    
    bot.send_message(message.chat.id, result_message, 
                     parse_mode='Markdown', 
                     reply_markup=markup)
    
    # Очищаем состояние пользователя (но сохраняем тип личности для статистики)
    user_states[user_id]['current_question'] = -1  # Помечаем как завершенный

def show_help(message):
    """Показывает справку о боте"""
    help_text = (
        "🤖 <b>О боте:</b>\n\n"
        "Я определяю тип личности по методике MBTI (Myers-Briggs Type Indicator).\n\n"
        "🎯 <b>Что такое MBTI?</b>\n"
        "Это популярная методика, которая определяет 16 типов личности на основе 4 параметров:\n"
        "• E/I - Экстраверсия/Интроверсия\n"
        "• S/N - Сенсорика/Интуиция\n"
        "• T/F - Мышление/Чувство\n"
        "• J/P - Суждение/Восприятие\n\n"
        "📊 <b>Как проходит тест:</b>\n"
        "16 вопросов → Анализ ответов → Подробный результат\n\n"
        "💡 <b>Создатель:</b>\n"
        "Этот бот был создан DeepSeek AI Assistant - искусственным интеллектом от компании DeepSeek!\n\n"
        "🚀 <b>Начать тест:</b>\n"
        "Просто нажми '🧠 Пройти тест личности' чтобы начать!"
    )
    
    bot.send_message(message.chat.id, help_text, 
                     parse_mode='HTML',
                     reply_markup=create_test_keyboard())

def show_statistics(message):
    """Показывает статистику пользователя"""
    user_id = message.from_user.id
    stats_text = (
        f"📊 <b>Статистика</b>\n\n"
        f"Привет, {message.from_user.first_name}!\n\n"
    )
    
    if user_id in user_states and user_states[user_id].get('personality'):
        personality = user_states[user_id]['personality']
        stats_text += f"🎯 <b>Твой тип личности:</b> {personality}\n"
        stats_text += f"📅 <b>Последний тест:</b> пройден\n\n"
    else:
        stats_text += "Ты еще не проходил тест личности.\n\n"
    
    stats_text += "Хочешь пройти тест еще раз или узнать свой тип?"
    
    bot.send_message(message.chat.id, stats_text,
                     parse_mode='HTML',
                     reply_markup=create_test_keyboard())

def cancel_test(message):
    """Отмена теста"""
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    cancel_text = (
        "Тест отменен. 😔\n\n"
        "Если захочешь попробовать снова - просто нажми кнопку ниже! "
        "Я всегда готов помочь тебе узнать себя лучше! 🌟"
    )
    
    bot.send_message(message.chat.id, cancel_text,
                     reply_markup=create_test_keyboard())

if __name__ == "__main__":
    print("Бот запущен и готов к работе! 🤖")
    print("Для остановки бота нажми Ctrl+C")
    try:
        bot.polling(none_stop=True, interval=0)
    except KeyboardInterrupt:
        print("\nБот остановлен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
