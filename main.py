
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F
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

generate_password_settings= {
    'length':16,
    'special_symbols':True,
    'digits':True, 
    'Upper':True,
    'Lower':True,
    'personal_alphabet':""
}

class Generation(StatesGroup):
    alphabet = State()
    length = State()

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
async def generate_password(message: types.Message, 
                            length=generate_password_settings['length'], 
                            special_symbols=generate_password_settings["special_symbols"], 
                            digits=generate_password_settings["digits"], 
                            Upper=generate_password_settings["Upper"], 
                            Lower=generate_password_settings["Lower"], 
                            personal_alphabet=generate_password_settings["personal_alphabet"]):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Изменить название длины",
        callback_data="change_length")
    )
    if special_symbols:
        builder.add(types.InlineKeyboardButton(
            text="Отключить спец. символы",
            callback_data="change_special")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить спец. символы",
            callback_data="change_special")
        )

    if digits:
        builder.add(types.InlineKeyboardButton(
            text="Отключить цифры",
            callback_data="change_digits")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить цифры",
            callback_data="change_digits")
        )

    if Upper:
        builder.add(types.InlineKeyboardButton(
            text="Отключить заглавные",
            callback_data="change_upper")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить заглавные",
            callback_data="change_upper")
        )
 
    if Lower:
        builder.add(types.InlineKeyboardButton(
            text="Отключить прописные",
            callback_data="change_lower")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить прописные",
            callback_data="change_lower")
        )

    builder.add(types.InlineKeyboardButton(
        text="Добавить доп. символы",
        callback_data="change_alphabet")
    )

    builder.add(types.InlineKeyboardButton(
        text="Сгенерировать",
        callback_data="change_generate")
    )

    await message.answer(f"""<u>Настройки:</u>
Длина: {length} символов
Специальные символы: {special_symbols}
Цифры: {digits}
<u>Буквы:</u>
Верхний регистр: {Upper}
Нижний регистр: {Lower}
<u>Дополнительные символы:</u> {personal_alphabet}""", parse_mode="HTML", reply_markup=builder.as_markup())
    

@bot_dispather.callback_query(F.data.startswith("change_"))
async def callbacks_num(message: types.message, callback: types.CallbackQuery, state: FSMContext):
    #user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "special":
        generate_password_settings["special_symbols"] = not generate_password_settings["special_symbols"]
        #await update_num_text(callback.message, user_value+1)
    elif action == "digits":
        generate_password_settings['digits'] = not generate_password_settings['digits']
        #await update_num_text(callback.message, user_value-1)
    elif action == "upper":
        generate_password_settings['Upper'] = not generate_password_settings['Upper']
        #await callback.message.edit_text(f"Итого: {user_value}")
    elif action == "lower":
        generate_password_settings['Lower'] = not generate_password_settings['Lower']
    elif action == 'alphabet':
        await state.set_state(Generation.alphabet)
        await message.answer("Введите без пробелов в одну строчку все необходимые символы\nПример:\nабвгд:1238,")
         #await update_num_text(callback.message, user_value+1)
    elif action == "length":
        await state.set_state(Generation.length)
        await message.answer("Напишите необходимую длину пароля")
    elif action == 'generate':
        generate_password(length=generate_password_settings["length"], 
                          special=generate_password_settings["special_symbols"], 
                          digits=generate_password_settings["digits"], 
                          Upper=generate_password_settings["Upper"], 
                          Lower=generate_password_settings["Lower"], 
                          personal_alphabet=generate_password_settings["personal_alphabet"])
    await callback.answer()
    

@bot_dispather.message(Generation.alphabet)
async def process_name(message: types.Message, callback: types.CallbackQuery, state: FSMContext):
    generate_password_settings['alphabet'] = message.text
    print(generate_password_settings)
    state.clear()
    await state.finish()


@bot_dispather.message(Generation.length)
async def process_name(message: types.Message, callback: types.CallbackQuery, state: FSMContext):
    generate_password_settings['length'] = message.text
    print(generate_password_settings)
    state.clear()
    await state.finish()

# Вывод общей информации о боте
@bot_dispather.message(Command('info'))
async def info(message: types.message, started_at: str):
    await message.answer(f"""Бот запущен <b>{started_at.strftime("%d-%b-%Y %H:%M:%S")}</b>
Он работает уже {datetime.now()-started_at}""", parse_mode="HTML")


# Скачка отправленного фото
@bot_dispather.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"C:\\Users\\USER\\GitHub-repos\\useful-pu-telegram-bot\\photos\\{message.photo[-1].file_id}.jpg"
    )


# Основной цикл бота
async def main():
    await bot_dispather.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())







