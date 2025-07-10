import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F, MagicFilter
from dotenv import load_dotenv
import os
from db import engine, PubMedSearch, get_query, add_query
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pubmed_search import search, fetch_details
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError


scheduler = AsyncIOScheduler()
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(text='введите ключевые слова для поиска в PubMed. Не более 3 слов, разделенных запятой')


@dp.message(Command("edit"))
async def edit_query(message: types.Message):
    with Session(engine) as session:
        if session.query(PubMedSearch).filter_by(user_id=message.from_user.id).first():
            builder = InlineKeyboardBuilder()
    
            builder.add(types.InlineKeyboardButton(
                text='ключевые слова для поискового запроса',
                callback_data='edit_query_keywords'
            ))
            builder.add(types.InlineKeyboardButton(
                text='email',
                callback_data='edit_email'
            ))

            builder.add(types.InlineKeyboardButton(
                text='частоту проверки базы',
                callback_data='edit_pubmed_check_interval'
            ))

            await message.answer(
                text='выберите, что вы хотите отредактировать:',
                reply_markup=builder.as_markup()
            )
        else:
            await message.answer("вы еще не создавали поисковый запрос. выберите команду /start из меню, чтоб его создать")


@dp.message(F.text.contains("@"))
async def validate_and_add_email(message: types.Message):
    print('EMAIL MESSAGE TEXT: ', message.text)
    try:
        email = validate_email(message.text)
        await message.reply('good email')
        await choose_pubmed_check(message)
    except EmailNotValidError as e:
        print(e)
        await message.reply('BAD email')


@dp.message(F.text.contains(",") and MagicFilter.len(F.text.split(',')) <= 3)
async def add_keywords_to_db(message: types.Message):
    with Session(engine) as session:
        if not session.query(PubMedSearch).filter_by(user_id=message.from_user.id).first():
            add_query(int(message.from_user.id), message.text)
            await message.reply("записано")
            await input_email(message)
        else:
            await message.reply("запись уже существует. выберите команду /edit - отредактировать запись из меню")


@dp.message(F.text.contains(",") and MagicFilter.len(F.text.split(',')) > 3)
async def invalid_query_handler(message: types.Message):
    await message.reply("неверный ввод. попробуйте снова. Не более 3 слов, разделенных запятой")


@dp.message()
async def input_email(message: types.Message):
    await message.answer(text='введите email')


@dp.message()
async def choose_pubmed_check(message: types.Message):
    builder = InlineKeyboardBuilder()
    
    builder.add(types.InlineKeyboardButton(
        text='по понедельникам',
        callback_data='mondays'
    ))
    builder.add(types.InlineKeyboardButton(
        text='по пятницам',
        callback_data='fridays'
    ))

    builder.add(types.InlineKeyboardButton(
        text='в последнюю пятницу месяца',
        callback_data='month_last_friday'
    ))

    await message.answer(
        text='выберите день проверки PubMed',
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "mondays")
async def add_check_mondays(callback: types.CallbackQuery):
    await callback.message.answer("ok, проверяем по понедельникам", )
    await callback.message.delete()
    # func to add to db


@dp.callback_query(F.data == "fridays")
async def add_check_fridays(callback: types.CallbackQuery):
    await callback.message.answer("ok, проверяем по пятницам", )
    await callback.message.delete()
    # func to add to db



@dp.callback_query(F.data == "month_last_friday")
async def add_check_fridays(callback: types.CallbackQuery):
    await callback.message.answer("ok, проверяем раз в месяц", )
    await callback.message.delete()
    # func to add to db



@dp.message()
async def send_mes_test(dp: Dispatcher):
    q_words = get_query() # new
    await bot.send_message(chat_id=5497349882, text='message by shedule') # old
    await bot.send_message(chat_id=5497349882, text=q_words)

def shedule_jobs():
    scheduler.add_job(send_mes_test, 'interval', seconds=10, args=(dp,))    


# Запуск процесса поллинга новых апдейтов
async def main():
    #shedule_jobs() # call func of sheduling
    #scheduler.start() # start here
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())