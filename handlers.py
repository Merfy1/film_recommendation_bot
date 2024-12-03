# Paste this into your `handlers.py` file
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from kino_api import KinoAPI
import random

# Создаем экземпляр класса KinoAPI
kino_api = KinoAPI()

# Переменная для отслеживания текущей функции
search_mode = 0

# Обработчик команды /start
async def start_command_handler(message: types.Message):
    global search_mode
    search_mode = 0  # Сбрасываем переменную
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Помощь"),
        KeyboardButton("Поиск по жанру"),
        KeyboardButton("Поиск по названию"),
        KeyboardButton("Случайный фильм"),
        KeyboardButton("Поиск по году"),
        KeyboardButton("Поиск по человеку")
    )
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

# Обработчик команды "Помощь"
async def help_command_handler(message: types.Message):
    global search_mode
    search_mode = 0  # Сбрасываем переменную
    help_text = (
        "Вот что я могу сделать:\n"
        "1️⃣ Помощь: узнать о доступных функциях(/help).\n"
        "2️⃣ Поиск по жанру: выбрать жанр фильма и получить рекомендацию(/recommend).\n"
        "3️⃣ Поиск по названию: найти фильм по названию(/search).\n"
        "4️⃣ Случайный фильм: получить случайный фильм(/random).\n"
        "5️⃣ Поиск по году: найти фильм, указав год (/year).\n"
        "6️⃣ Поиск по человеку: найти фильмы по имени актера или режиссера (/person)."
    )
    await message.answer(help_text)

# Обработчик команды "Поиск по жанру"
async def recommend_genre_handler(message: types.Message):
    global search_mode
    search_mode = 0  # Сбрасываем переменную
    genre_buttons = [
        "драма", "комедия", "боевик", "фантастика", "триллер", "ужасы", "мелодрама", "аниме", "документальный",
        "фэнтези", "приключения", "криминал", "семейный", "детектив", "музыка", "история", "спорт", "реальное ТВ",
        "мультфильм", "военный", "детский", "биография", "вестерн", "фильм-нуар", "короткометражка", "мюзикл", 
        "ток-шоу", "игра"
    ]
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*(InlineKeyboardButton(text=genre, callback_data=f"genre_{genre}") for genre in genre_buttons))
    await message.answer("Выберите жанр фильма:", reply_markup=keyboard)

# Обработчик выбора жанра через callback
async def process_genre_selection(callback_query: types.CallbackQuery):
    genre_name = callback_query.data.split("_")[1]
    movie = kino_api.get_movies_by_genre(genre_name)
    await callback_query.message.answer(movie)
    await callback_query.answer()

# Обработчик команды "Поиск по году"
async def search_by_year_handler(message: types.Message):
    global search_mode
    search_mode = 1  # Устанавливаем режим поиска по году
    await message.answer("Введите год (цифрами), чтобы найти фильм:")

# Обработчик команды "Поиск по человеку"
async def person_search_handler(message: types.Message):
    global search_mode
    search_mode = 2  # Устанавливаем режим поиска по человеку
    await message.answer("Введите имя режиссера или актера:")

# Обработчик команды "Поиск по названию"
async def search_command_handler(message: types.Message):
    global search_mode
    search_mode = 3  # Устанавливаем режим поиска по названию
    await message.answer("Введите название фильма:")

# Обработчик текстового ввода
async def text_input_handler(message: types.Message):
    global search_mode

    if search_mode == 1:  # Поиск по году
        try:
            year = int(message.text.strip())
            movie_info = kino_api.get_movie_by_year(year)
            search_mode = 0  # Сбрасываем режим
            await message.answer(movie_info)
        except ValueError:
            await message.answer("Пожалуйста, введите год цифрами (например, 2021).")

    elif search_mode == 2:  # Поиск по человеку
        person_name = message.text.strip()
        movie_info = kino_api.get_movie_by_person(person_name)
        search_mode = 0  # Сбрасываем режим
        await message.answer(movie_info)

    elif search_mode == 3:  # Поиск по названию
        movie_name = message.text.strip()
        movie_info = kino_api.get_movie_by_name(movie_name)
        search_mode = 0  # Сбрасываем режим
        await message.answer(movie_info)

    else:
        await message.answer("Пожалуйста, выберите действие из меню.")

# Обработчик команды "Случайный фильм"
async def random_movie_handler(message: types.Message):
    global search_mode
    search_mode = 0  # Сбрасываем переменную
    await message.answer("Генерирую случайный фильм, подождите...")
    movie_info = kino_api.get_random_movie()
    await message.answer(movie_info)

# Функция для регистрации всех обработчиков
def register_handlers(dp):
    dp.register_message_handler(start_command_handler, commands=["start"])
    dp.register_message_handler(help_command_handler, text="Помощь")
    dp.register_message_handler(help_command_handler, commands=["help"])
    dp.register_message_handler(recommend_genre_handler, text="Поиск по жанру")
    dp.register_message_handler(recommend_genre_handler, commands=["recommend"])
    dp.register_message_handler(search_by_year_handler, text="Поиск по году")
    dp.register_message_handler(search_by_year_handler, commands=["year"])
    dp.register_message_handler(person_search_handler, text="Поиск по человеку")
    dp.register_message_handler(person_search_handler, commands=["person"])
    dp.register_message_handler(search_command_handler, text="Поиск по названию")
    dp.register_message_handler(search_command_handler, commands=["search"])
    dp.register_message_handler(random_movie_handler, text="Случайный фильм")
    dp.register_message_handler(random_movie_handler, commands=["random"])
    dp.register_message_handler(text_input_handler)
    dp.register_callback_query_handler(process_genre_selection, lambda c: c.data and c.data.startswith('genre_'))
