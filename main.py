import os
import telebot
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Вопросы и варианты ответов
questions = [
    {
        "text": "1. Вы предпочитаете проводить время в большой компании или наедине с собой?",
        "options": ["В компании", "Наедине"],
        "scores": {"В компании": "E", "Наедине": "I"}
    },
    {
        "text": "2. Вы чаще принимаете решения на основе логики или чувств?",
        "options": ["Логика", "Чувства"],
        "scores": {"Логика": "T", "Чувства": "F"}
    },
    {
        "text": "3. Вы любите планировать всё заранее или действовать спонтанно?",
        "options": ["Планировать", "Спонтанно"],
        "scores": {"Планировать": "J", "Спонтанно": "P"}
    },
    {
        "text": "4. Вы больше ориентированы на детали или на общую картину?",
        "options": ["Детали", "Общая картина"],
        "scores": {"Детали": "S", "Общая картина": "N"}
    }
]

# Хранилище состояния пользователей
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                    "👋 Привет! Я помогу определить твой тип личности по методике MBTI.\n\n"
                    "Ответь на 4 простых вопроса, и я скажу, кто ты!\n\n"
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
        
        bot.send_message(
            message.chat.id, 
            questions[question_num]["text"],
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
                        "/cancel - отменить текущий тест")

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
    
    # Собираем тип личности
    personality = ""
    for i, answer in enumerate(answers):
        personality += questions[i]["scores"][answer]
    
    # Описания типов личности (MBTI)
    type_descriptions = {
        "ISTJ": "📊 Ответственный и организованный реалист",
        "ISFJ": "🛡️ Преданный и заботливый защитник", 
        "INFJ": "💭 Глубокий и вдохновляющий советчик",
        "INTJ": "🎯 Стратегический и независимый новатор",
        "ISTP": "🔧 Прагматичный и смелый исследователь",
        "ISFP": "🎨 Чуткий и гармоничный художник",
        "INFP": "🌟 Идеалистичный и творческий мечтатель",
        "INTP": "🤔 Логичный и любознательный мыслитель",
        "ESTP": "⚡ Энергичный и предприимчивый деятель",
        "ESFP": "🎭 Жизнерадостный и спонтанный артист",
        "ENFP": "💫 Энтузиастичный и креативный вдохновитель",
        "ENTP": "💡 Изобретательный и любознательный полемист",
        "ESTJ": "💪 Решительный и практичный организатор",
        "ESFJ": "🤝 Заботливый и общительный помощник",
        "ENFJ": "🗣️ Харизматичный и убедительный наставник",
        "ENTJ": "👑 Решительный и стратегический лидер"
    }
    
    description = type_descriptions.get(personality, "🤔 Уникальная личность!")
    
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                    f"🎉 **Твой результат теста:**\n\n"
                    f"**Тип личности:** {personality}\n"
                    f"**Описание:** {description}\n\n"
                    f"Спасибо за прохождение теста! ✨\n"
                    f"Хочешь пройти еще раз? /test",
                    parse_mode='Markdown',
                    reply_markup=markup)
    
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
                    "/test - Пройти тест на тип личности\n"
                    "/cancel - Отменить текущий тест\n"
                    "/help - Показать эту справку\n\n"
                    "Просто нажми /test чтобы начать!",
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
