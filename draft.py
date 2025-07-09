
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from sqlalchemy.orm import Session
from aiogram import F
from dotenv import load_dotenv
import os
from db import engine, PubMedSearch
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pubmed_search import search, fetch_details


scheduler = AsyncIOScheduler()

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

    #######################
    # here search in pubmed without schedule
    ########################

    # calling func to send your his query digest
    await send_message_to_user(user_id=message.from_user.id)
    q_words= get_query(message.from_user.id).split(',')
    results = search(q_words[0])
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))

@dp.message(F.text.contains("ввести ключевые слова для поиска"))
async def var_1(message: types.Message):
    await message.reply("введите ключевые слова", reply_markup=types.ReplyKeyboardRemove())
    print(message.from_user.id)




####################################################
# this will be function to send digest
async def send_message_to_user(user_id):
    try:
        await bot.send_message(chat_id=user_id, text='i send you message by your id')
        print(f"Message sent to user {user_id}")
    except Exception as e:
        print(f"Error sending message to user {user_id}: {e}")
#
##########################################################################



# Запуск процесса поллинга новых апдейтов
async def main():
    #shedule_jobs() # call func of sheduling
    #scheduler.start() # start here
    
    await dp.start_polling(bot)






@dp.message()
async def send_mes_test(dp: Dispatcher):
    await bot.send_message(chat_id=5497349882, text='message by shedule')


def shedule_jobs():
    scheduler.add_job(send_mes_test, 'interval', seconds=5, args=(dp,))    

#############################
# db methods
############################
def add_query(user, query):
    with Session(engine) as session:
        query_record = PubMedSearch(user_id=user, query_words=query)
        session.add(query_record)
        session.commit()

def get_query(user):
    with Session(engine) as session:
        search_query = session.query(PubMedSearch).filter_by(user_id=user).first()
        print(type(search_query))
        print(dir(search_query))
        return search_query.query_words


if __name__ == "__main__":
    
    
    asyncio.run(main())