import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from db import get_records_by_schedule_interval


load_dotenv()

scheduler = AsyncIOScheduler()

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())

async def search_pubmed_on_monday(dp: Dispatcher):
    records = get_records_by_schedule_interval('mondays')
    print('*' * 100)
    for record in records:
        print('id: ', record.user_id)
        print('query_words: ', record.query_words)
        print('interval: ', record.schedule_interval)
    


def shedule_jobs():
    # scheduler.add_job(send_mes_test, 'interval', seconds=10, args=(dp,))
    scheduler.add_job(search_pubmed_on_monday,'interval', seconds=5, args=(dp, ))    
    

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp.include_router(router)
    shedule_jobs() # call func of sheduling
    scheduler.start() # start here

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())