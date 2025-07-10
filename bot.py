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

scheduler = AsyncIOScheduler()
load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='ввести поисковые слова',
        callback_data='query_words'
    ))

    await message.answer(
        'нажмите на кнопку, чтоб ввести поисковые слова',
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "query_words")
async def get_query_words_input(callback: types.CallbackQuery):
    await callback.message.reply("введите ключевые слова для поиска в PubMed. Не более 3 слов, разделенных запятой", )
                        #reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.contains(",") and MagicFilter.len(F.text.split(',')) <= 3)
async def var_1(message: types.Message):
    with Session(engine) as session:
        if not session.query(PubMedSearch).filter_by(user_id=message.from_user.id).first():
            add_query(int(message.from_user.id), message.text)
            await message.reply("записано")
            await send_message_to_user(user_id=message.from_user.id)
        else:
            await message.reply("запись уже существует")


@dp.message(F.text.contains(",") and MagicFilter.len(F.text.split(',')) > 3)
async def var_1(message: types.Message):
    await message.reply("неверный ввод. попробуйте снова. Не более 3 слов, разделенных запятой")




#################################3
@dp.message(F.text.contains("ввести ключевые слова для поиска"))
async def var_1(message: types.Message):
    await message.reply("введите ключевые слова для поиска в PubMed. Не более 3 слов, разделенных запятой", 
                        reply_markup=types.ReplyKeyboardRemove())

"""
@dp.message(F.text.contains(","))
async def var_1(message: types.Message):
    add_query(int(message.from_user.id), message.text)
    await message.reply("записано")
    await send_message_to_user(user_id=message.from_user.id)
    
    # it'll be the query by shedule
    q_words= get_query(message.from_user.id).split(',')
    results = search(q_words[0])
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
    
"""
####################################################
# this will be function to send digest
# placeholder to see it works
async def send_message_to_user(user_id):
    try:
        await bot.send_message(chat_id=user_id, text='i send you message by your id')
        print(f"Message sent to user {user_id}")
    except Exception as e:
        print(f"Error sending message to user {user_id}: {e}")
#
##########################################################################

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