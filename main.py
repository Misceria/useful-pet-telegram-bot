

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio
import logging
from datetime import datetime

from password_generator import generate_password
from settings_reader import read_settings

# Включаем логирование работы бота
logging.basicConfig(level=logging.INFO)

# Получаем настройки из файла
settings = read_settings() 

bot=Bot(token=settings["BOT_TOKEN"])
bot_dispather = Dispatcher()
bot_dispather["started_at"] = datetime.now()

# Обработка команды /start для ознакомления пользователя с функционалом и командами
@bot_dispather.message(Command("start"))
async def user_greetings(message: types.Message):
    await message.answer("""Привет-привет, я полезный питомец бот, но можешь называть меня <b>Тьюри</b>!
Мой функционал пока в разработке, но предположительно Ты можешь воспользоваться следующими функциями:
    1) **IN PROGRESS** Создание сложного пароля (Не волнуйся я его запомню и подскажу тебе, если ты его забудешь) 
    2) **IN PROGRESS** Поиск слов и предложений в файлах и архивах
    3) **IN PROGRESS** Поиск ссылок по вебстранице
    4) **IN PROGRESS** и т.д.""", parse_mode="HTML")


# Данная функция создаёт надёжный пароль по требованиям пользователя
@bot_dispather.message(Command('generate_password'))
async def generate_password(message: types.Message, length=16, special_symbols=True, 
                            digits=True, Upper=True, Lower=True, personal_alphabet=""):
    await message.answer(f"""<u>Настройки:</u>
Длина: {length} символов
Специальные символы: {special_symbols}
Цифры: {digits}
<u>Буквы:</u>
Верхний регистр: {Upper}
Нижний регистр: {Lower}
<u>Дополнительные символы:</u> {personal_alphabet}""", parse_mode="HTML")
    
@bot_dispather.message(Command('info'))
async def info(message: types.message, started_at: str):
    await message.answer(f"""Бот запущен <b>{started_at.strftime("%d-%b-%Y %H:%M:%S")}</b>
Он работает уже {datetime.now()-started_at}""", parse_mode="HTML")


# Основной цикл бота
async def main():
    await bot_dispather.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())







