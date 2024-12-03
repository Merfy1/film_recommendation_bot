import os
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from handlers import register_handlers


# Загружаем переменные из .env файла
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Создаем экземпляры бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Регистрируем обработчики
register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
