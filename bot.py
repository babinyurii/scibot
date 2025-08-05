import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from db import get_records_by_schedule_interval
from pubmed_search import get_articles
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import json


load_dotenv()

scheduler = AsyncIOScheduler()

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),)



async def search_pubmed_on_schedule(interval):
    print('#' * 100)
    print('interval from search function: ', interval)
    records = get_records_by_schedule_interval(interval)
    # is there need to check if records from db are empty
    for record in records:
        print('id: ' * 100, '\n', record.user_id)
        print('query_words: ' * 100, '\n', record.query_words)
        print('interval: ', record.schedule_interval)
        articles = ''
        query_words = json.loads(record.query_words)
        #print(query_words.split(','))
        #query_words = query_words.split(',')
        #query_words = query_words[0:2]
        for query_word in query_words:
            
            try:
                print(query_word)
                articles += get_articles(query_words=query_word)
                #articles = get_articles(query_words=query_word)
            except Exception as e:
                print ('error: ' * 100, e)
                pass
                # into log
        
        # TODO: add check somewhere for message len: 4096 utf chars
        await bot.send_message(chat_id=record.user_id, text=articles)


async def search_pubmed_last_fri(dp: Dispatcher,):
    await search_pubmed_on_schedule(interval='last_friday')

async def search_pubmed_mon(dp: Dispatcher,):
    await search_pubmed_on_schedule(interval='mondays')

async def search_pubmed_fri(dp: Dispatcher,):
    await search_pubmed_on_schedule(interval='fridays')


def shedule_jobs():
    #scheduler.add_job(search_pubmed_on_schedule, 'interval', seconds=15, args=(dp, ))    
    
    #scheduler.add_job(search_pubmed_last_fri, "cron", day="last fri", args=(dp, ))
    #scheduler.add_job(search_pubmed_mon, 'cron', day_of_week='mon', hour=12, args=(dp, ) )
    #scheduler.add_job(search_pubmed_fri, 'cron', day_of_week='fri', hour=12,  args=(dp, ))
    
    # test funcs
    #scheduler.add_job(search_pubmed_last_fri, 'interval', seconds=30,  args=(dp, ))
    scheduler.add_job(search_pubmed_mon, 'interval', seconds=30, args=(dp, ) )
    #scheduler.add_job(search_pubmed_fri, 'interval', minutes=15,   args=(dp, ))
    
    

async def main():
    
    dp.include_router(router)
    shedule_jobs() # call func of sheduling
    scheduler.start() # start here

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())