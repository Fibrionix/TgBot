
import telebot
import os
import logging
from datetime import datetime, timedelta
from functools import wraps


# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота (замените на реальный)
TOKEN = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Вопросы теста (16 шт. — по 4 на каждую шкалу)
QUESTIONS = [
    # E/I (Экстраверсия/Интроверсия)
    "Мне легче общаться с людьми, чем проводить время в одиночестве",
    "Я получаю энергию от нахождения в компании",
    "Я предпочитаю говорить, а не молчать в группе",
    "Мне комфортно быть в центре внимания",
    # S/N (Ощущение/Интуиция)
    "Я обращаю внимание на детали и факты",
    "Мне важно иметь чёткие инструкции",
    "Я предпочитаю абстрактные идеи конкретным примерам",
    "Я часто думаю о будущем и возможностях",
    # T/F (Мышление/Чувство)
    "Я принимаю решения на основе логики, а не эмоций",
    "Мне важно быть объективным в оценках",
    "Я легко понимаю чувства других людей",
    "Я стараюсь учитывать эмоции при принятии решений",
    # J/P (Суждение/Восприятие)
    "Я люблю планировать и следовать расписанию",
    "Мне некомфортно без чёткого плана",
    "Я предпочитаю гибкость и спонтанность",
    "Я легко адаптируюсь к изменениям"
]

# Шкалы и их направления
SCALES = {
    "EI": {"E": 0, "I": 0},
    "SN": {"S": 0, "N": 0},
    "TF": {"T": 0, "F": 0},
    "JP": {"J": 0, "P": 0}
}

# Текущий вопрос
current_question = 0

def get_mbti_type():
    """Определяет тип личности на основе шкал"""
    type_code = ""
    type_code += "E" if SCALES["EI"]["E"] > SCALES["EI"]["I"] else "I"
    type_code += "S" if SCALES["SN"]["S"] > SCALES["SN"]["N"] else "N"
    type_code += "T" if SCALES["TF"]["T"] > SCALES["TF"]["F"] else "F"
    type_code += "J" if SCALES["JP"]["J"] > SCALES["JP"]["P"] else "P"
    return type_code

# Описание типов (кратко)
MBTI_DESCRIPTIONS = {
    "ENTJ": "Командир: стратегический мыслитель, лидер, любит вызовы",
    "ENFJ": "Педагог: вдохновляющий, эмпатичный, организатор",
    "ENTP": "Новатор: любопытный, креативный, любит дискуссии",
    "ENFP": "Борец: энтузиаст, харизматичный, ищет смысл",
    "INTJ": "Архитектор: аналитический, независимый, стратег",
    "INFJ": "Активист: идеалист, глубокий, помогает другим",
    "INTP": "Логик: исследователь, любит теории, скептик",
    "INFP": "Посредник: мечтатель, ценит гармонию, творческий",
    "ESTJ": "Администратор: практичный, организованный, лидер",
    "ESFJ": "Консул: дружелюбный, заботливый, социальный",
    "ESTP": "Предприниматель: энергичный, адаптивный, любит действие",
    "ESFP": "Артист: жизнерадостный, спонтанный, любит внимание",
    "ISTJ": "Защитник: надёжный, дисциплинированный, практичный",
    "ISFJ": "Защитник: заботливый, преданный, традиционный",
    "ISTP": "Мастер: логичный, независимый, любит механизмы",
    "ISFP": "Художник: чувствительный, добрый, ценит красоту"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start — начало теста"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n\n"
        "Давай определим твой тип личности по MBTI.\n"
        "Отвечай на вопросы по шкале от 1 до 5:\n"
        "1 — полностью не согласен\n"
        "3 — нейтрально\n"
        "5 — полностью согласен\n\n"
        "Нажми «Начать», чтобы приступить:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Начать", callback_data="start_test")]
        ])
    )

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск теста"""
    global current_question, SCALES
    current_question = 0
    SCALES = {k: {kk: 0 for kk in v} for k, v in SCALES.items()}
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Задать текущий вопрос"""
    if current_question < len(QUESTIONS):
        question = QUESTIONS[current_question]
        await update.callback_query.message.reply_text(
            f"Вопрос {current_question + 1}/{len(QUESTIONS)}:\n{question}\n\n"
            "Оцените по шкале:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("1", callback_data="ans_1")],
                [InlineKeyboardButton("2", callback_data="ans_2")],
                [InlineKeyboardButton("3", callback_data="ans_3")],
                [InlineKeyboardButton("4", callback_data="ans_4")],
                [InlineKeyboardButton("5", callback_data="ans_5")]
            ])
        )
    else:
        await show_result(update, context)

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка ответа (1–5)"""
    global current_question

    # Извлекаем значение ответа из callback_data
    try:
        value = int(update.callback_query.data.replace("ans_", ""))
    except ValueError:
        await update.callback_query.answer()
        return

    # Определяем шкалу для текущего вопроса
    scale_index = current_question // 4  # 0=EI, 1=SN, 2=TF, 3=JP
    scale_key = list(SCALES.keys())[scale_index]

    # Распределяем баллы по направлениям шкалы
    if scale_key == "EI":
        SCALES[scale_key]["E"] += value
        SCALES[scale_key]["I"] += (6 - value)
    elif scale_key == "SN":
        SCALES[scale_key]["S"] += value
        SCALES[scale_key]["N"] += (6 - value)
    elif scale_key == "TF":
        SCALES[scale_key]["T"] += value
        SCALES[scale_key]["F"] += (6 - value)
    elif scale_key == "JP":
        SCALES[scale_key]["J"] += value
        SCALES[scale_key]["P"] += (6 - value)

    current_question += 1
    await ask_question(update, context)

async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать результат и кнопку «Пройти тест заново?»"""
    mbti_type = get_mbti_type()
    description = MBTI_DESCRIPTIONS.get(mbti_type, "Описание не найдено")

    result_text = (
        f"Ваш тип личности: *{mbti_type}*\n\n"
        f"{description}\n\n"
        "Ваши показатели по шкалам:\n"
    )
    for scale, values in SCALES.items():
        if scale == "EI":
            result_text += f"{scale}: E={values['E']}, I={values['I']}\n"
        elif scale == "SN":
            result_text += f"{scale}: S={values['S']}, N={values['N']}\n"
        elif scale == "TF":
            result_text += f"{scale}: T={values['T']}, F={values['F']}\n"
        elif scale == "JP":
            result_text += f"{scale}: J={values['J']}, P={values['P']}\n"

    await update.callback_query.message.reply_text(
        result_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Пройти тест заново?", callback_data="start_test")]
        ]),
        parse_mode="Markdown"
    )

def main() -> None:
    """Основная функция запуска бота"""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start_test, pattern="^start_test$"))
    application.add_handler(CallbackQueryHandler(answer, pattern="^ans_[1-5]$"))

    application.run_polling()

if __name__ == "__main__":
    main()
