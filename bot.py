import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router

load_dotenv()

scheduler = AsyncIOScheduler()

logging.basicConfig(level=logging.INFO)

def shedule_jobs():
    # scheduler.add_job(send_mes_test, 'interval', seconds=10, args=(dp,))
    #scheduler.add_job(check_pubmed_on_monday, args=(dp, ))    
    pass


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp.include_router(router)
    shedule_jobs() # call func of sheduling
    scheduler.start() # start here

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())