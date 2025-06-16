
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from dotenv import load_dotenv
import os

load_dotenv()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

"""
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("hijack"))
async def cmd_answer(message: types.Message):
    await message.answer("Это простой ответ")


@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')

"""

# here we put two buttons
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
        types.KeyboardButton(text="вариант 1"),
        types.KeyboardButton(text="вариант 2"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,  
                                        resize_keyboard=True,
                                        input_field_placeholder="выберите переход")
    await message.answer("куда переходить?", reply_markup=keyboard, 
                                               )

# here we react to the text of buttons
@dp.message(F.text.lower() == "вариант 1")
async def var_1(message: types.Message):
    await message.reply("переходим на 1", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "вариант 2")
async def var_2(message: types.Message):
    await message.reply("переходим на 2!", reply_markup=types.ReplyKeyboardRemove())

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())