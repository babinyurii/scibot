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

def search_pubmed_on_monday():
    records = get_records_by_schedule_interval('mondays')
    print(records)
    pass


def shedule_jobs():
    # scheduler.add_job(send_mes_test, 'interval', seconds=10, args=(dp,))
    #scheduler.add_job(search_pubmed_on_monday,'interval', seconds=60, args=(dp, ))    
    pass

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp.include_router(router)
    shedule_jobs() # call func of sheduling
    scheduler.start() # start here

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())