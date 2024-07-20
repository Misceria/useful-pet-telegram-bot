
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import logging
from datetime import datetime


from password_generator import generate_password_on_set_parameters
from settings_reader import read_settings

# Включаем логирование работы бота
logging.basicConfig(level=logging.INFO)

# Получаем настройки из файла
settings = read_settings() 

bot=Bot(token=settings["BOT_TOKEN"])
bot_dispatcher = Dispatcher()
bot_dispatcher["started_at"] = datetime.now()

generate_password_settings= {
    'length':16,
    'special_symbols':True,
    'digits':True, 
    'Upper':True,
    'Lower':True,
    'personal_alphabet':""
}

class Generation(StatesGroup):
    default_mode = State()
    adding_alphabet_pass_gen = State()
    choosing_password_length = State()

# Обработка команды /start для ознакомления пользователя с функционалом и командами
@bot_dispatcher.message(Command("start"))
async def user_greetings(message: types.Message):
    await message.answer("""Привет-привет, я полезный питомец бот, но можешь называть меня <b>Тьюри</b>!
Мой функционал пока в разработке, но предположительно Ты можешь воспользоваться следующими функциями:
    1) **IN PROGRESS** Создание сложного пароля (Не волнуйся я его запомню и подскажу тебе, если ты его забудешь) 
    2) **IN PROGRESS** Поиск слов и предложений в файлах и архивах
    3) **IN PROGRESS** Поиск ссылок по вебстранице
    4) **IN PROGRESS** и т.д.""", parse_mode="HTML")

def create_inline_for_generate_password():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Изменить название длины",
        callback_data="change_length")
    )
    if generate_password_settings['special_symbols']:
        builder.add(types.InlineKeyboardButton(
            text="Отключить спец. символы",
            callback_data="change_special")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить спец. символы",
            callback_data="change_special")
        )

    if generate_password_settings['digits']:
        builder.add(types.InlineKeyboardButton(
            text="Отключить цифры",
            callback_data="change_digits")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить цифры",
            callback_data="change_digits")
        )

    if generate_password_settings['Upper']:
        builder.add(types.InlineKeyboardButton(
            text="Отключить заглавные",
            callback_data="change_upper")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="Включить заглавные",
            callback_data="change_upper")
        )
 
    if generate_password_settings['Lower']:
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
    return builder


# Данная функция создаёт надёжный пароль по требованиям пользователя
@bot_dispatcher.message(Command('generate_password'))
async def generate_password(message: types.Message, state: FSMContext):
    builder = create_inline_for_generate_password()
    message_generate_password = await message.answer(f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""", parse_mode="HTML", reply_markup=builder.as_markup())
    

@bot_dispatcher.callback_query(lambda c: c.data.startswith('change_'))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    #user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "special":
        generate_password_settings["special_symbols"] = not generate_password_settings["special_symbols"]
        builder = create_inline_for_generate_password()
        await bot.edit_message_text(
                text=f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""",
                parse_mode="HTML",
                chat_id = callback.message.chat.id,
                message_id = callback.message.message_id,
                reply_markup = builder.as_markup()
            )
    elif action == "digits":
        generate_password_settings['digits'] = not generate_password_settings['digits']
        builder = create_inline_for_generate_password()
        await bot.edit_message_text(
                text=f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""",
                parse_mode="HTML",
                chat_id = callback.message.chat.id,
                message_id = callback.message.message_id,
                reply_markup = builder.as_markup()
            )
    elif action == "upper":
        generate_password_settings['Upper'] = not generate_password_settings['Upper']
        builder = create_inline_for_generate_password()
        await bot.edit_message_text(
                text=f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""",
                parse_mode="HTML",
                chat_id = callback.message.chat.id,
                message_id = callback.message.message_id,
                reply_markup = builder.as_markup()
            )
    elif action == "lower":
        generate_password_settings['Lower'] = not generate_password_settings['Lower']
        builder = create_inline_for_generate_password()
        await bot.edit_message_text(
                text=f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""",
                parse_mode="HTML",
                chat_id = callback.message.chat.id,
                message_id = callback.message.message_id,
                reply_markup = builder.as_markup()
            )
    elif action == 'alphabet':
        await state.set_state(Generation.adding_alphabet_pass_gen)
        await callback.message.answer("Введите без пробелов в одну строчку все необходимые символы\nПример:\nабвгд:1238,")
        await state.update_data(message_id = callback.message.message_id)
    elif action == "length":
        await state.set_state(Generation.choosing_password_length)
        await callback.message.answer("Напишите необходимую длину пароля")
        await state.update_data(message_id = callback.message.message_id)
    elif action == 'generate':
        password = generate_password_on_set_parameters(length=generate_password_settings["length"], 
                                                        special=generate_password_settings["special_symbols"], 
                                                        digits=generate_password_settings["digits"], 
                                                        Upper=generate_password_settings["Upper"], 
                                                        Lower=generate_password_settings["Lower"], 
                                                        personal_alphabet=generate_password_settings["personal_alphabet"])
        await callback.message.answer(f"Надёжный пароль: {password}")
    await callback.answer()
    

@bot_dispatcher.message(Generation.adding_alphabet_pass_gen)
async def process_name(message: types.Message, state: FSMContext):
    generate_password_settings['personal_alphabet'] = message.text
    builder = create_inline_for_generate_password()
    data = await state.get_data()
    await bot.edit_message_text(
            text=f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""",
            parse_mode="HTML",
            chat_id = message.chat.id,
            message_id = data['message_id'],
            reply_markup = builder.as_markup()
        )
    await state.set_state(Generation.default_mode)
    

@bot_dispatcher.message(Generation.choosing_password_length)
async def process_name(message: types.Message, state: FSMContext):
    generate_password_settings['length'] = int(message.text)
    builder = create_inline_for_generate_password()
    data = await state.get_data()
    await bot.edit_message_text(
            text=f"""<u>Настройки:</u>
Длина: {generate_password_settings["length"]} символов
Специальные символы: {generate_password_settings["special_symbols"]}
Цифры: {generate_password_settings["digits"]}
<u>Буквы:</u>
Верхний регистр: {generate_password_settings["Upper"]}
Нижний регистр: {generate_password_settings["Lower"]}
<u>Дополнительные символы:</u> {generate_password_settings["personal_alphabet"]}""",
            parse_mode="HTML",
            chat_id = message.chat.id,
            message_id = data['message_id'],
            reply_markup = builder.as_markup()
        )
    await state.set_state(Generation.default_mode)

# Вывод общей информации о боте
@bot_dispatcher.message(Command('info'))
async def info(message: types.message, started_at: str):
    await message.answer(f"""Бот запущен <b>{started_at.strftime("%d-%b-%Y %H:%M:%S")}</b>
Он работает уже {datetime.now()-started_at}""", parse_mode="HTML")


# Скачка отправленного фото
@bot_dispatcher.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"C:\\Users\\USER\\GitHub-repos\\useful-pu-telegram-bot\\photos\\{message.photo[-1].file_id}.jpg"
    )


# Основной цикл бота
async def main():
    await bot_dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())







