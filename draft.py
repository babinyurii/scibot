
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from sqlalchemy.orm import Session
from aiogram import F
from dotenv import load_dotenv
import os
from db import engine, PubMedSearch


load_dotenv()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
        types.KeyboardButton(text="ввести ключевые слова для поиска"),
        types.KeyboardButton(text="вариант 2"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,  
                                        resize_keyboard=True,
                                        input_field_placeholder="нажмите на кнопку ниже, чтоб выбрать вариант")
    await message.answer("выберите вариант действий", reply_markup=keyboard, )

# here we react to the text of buttons
@dp.message(F.text.contains(","))
async def var_1(message: types.Message):
    await message.reply("записано")
    print(type(message.text))
    add_query(int(message.from_user.id), message.text)
    print('done')

@dp.message(F.text.contains("ввести ключевые слова для поиска"))
async def var_1(message: types.Message):
    await message.reply("введите ключевые слова", reply_markup=types.ReplyKeyboardRemove())
    print(message.from_user.id)
   

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


def add_query(user, query):
    with Session(engine) as session:
        query_record = PubMedSearch(user_id=user, query_words=query)
        session.add(query_record)
        session.commit()


if __name__ == "__main__":
    asyncio.run(main())