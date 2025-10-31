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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                    "👋 Привет! Я помогу определить твой тип личности по методике MBTI.\n\n"
                    "Тест состоит из 16 вопросов. Отвечай честно, чтобы получить точный результат!\n\n"
                    "Нажми /test чтобы начать тест!",
                    reply_markup=markup)

@bot.message_handler(commands=['test'])
def start_test(message):
    user_id = message.from_user.id
    user_states[user_id] = {
        'current_question': 0,
        'answers': [],
        'personality': ''
    }
    ask_question(message, 0)

def ask_question(message, question_num):
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
        
        bot.send_message(
            message.chat.id, 
            f"📊 {progress}\n\n{questions[question_num]['text']}",
            reply_markup=markup
        )
    else:
        # Все вопросы пройдены
        calculate_result(message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    # Проверяем, проходит ли пользователь тест
    if user_id not in user_states:
        handle_normal_message(message)
        return
    
    current_question_idx = user_states[user_id]['current_question']
    
    # Если тест завершен, но состояние еще не очищено
    if current_question_idx >= len(questions):
        handle_normal_message(message)
        return
    
    # Обработка отмены теста
    if message.text == "❌ Отменить тест":
        cancel_test(message)
        return
    
    current_question = questions[current_question_idx]
    
    # Проверяем валидность ответа
    if message.text not in current_question["options"]:
        bot.send_message(message.chat.id, 
                        "⚠️ Пожалуйста, выбери один из предложенных вариантов ответа.")
        return
    
    # Сохраняем ответ
    user_states[user_id]['answers'].append(message.text)
    
    # Переходим к следующему вопросу
    next_question_idx = current_question_idx + 1
    ask_question(message, next_question_idx)

def handle_normal_message(message):
    """Обработка обычных сообщений вне теста"""
    if message.text.lower() in ['привет', 'hello', 'hi']:
        bot.send_message(message.chat.id, "Привет! Нажми /test чтобы начать тест!")
    else:
        bot.send_message(message.chat.id, 
                        "Я бот для тестирования личности! 🧠\n"
                        "Используй команды:\n"
                        "/start - начать работу\n"
                        "/test - пройти тест\n"
                        "/cancel - отменить текущий тест\n"
                        "/help - помощь")

def cancel_test(message):
    """Отмена теста"""
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 
                    "Тест отменен. 😔\n"
                    "Если захочешь попробовать снова - нажми /test",
                    reply_markup=markup)

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
    markup = telebot.types.ReplyKeyboardRemove()
    
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
        f"Хочешь пройти еще раз? /test"
    )
    
    bot.send_message(message.chat.id, result_message, parse_mode='Markdown', reply_markup=markup)
    
    # Очищаем состояние пользователя
    if user_id in user_states:
        del user_states[user_id]

@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    cancel_test(message)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
                    "🤖 **Помощь по боту:**\n\n"
                    "/start - Начать работу с ботом\n"
                    "/test - Пройти тест на тип личности (16 вопросов)\n"
                    "/cancel - Отменить текущий тест\n"
                    "/help - Показать эту справку\n\n"
                    "Тест основан на методике MBTI и поможет лучше понять себя!",
                    parse_mode='Markdown')

if __name__ == "__main__":
    print("Бот запущен и готов к работе! 🤖")
    print("Для остановки бота нажми Ctrl+C")
    try:
        bot.polling(none_stop=True, interval=0)
    except KeyboardInterrupt:
        print("\nБот остановлен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
