from aiogram.fsm.state import StatesGroup, State


class CreateQuery(StatesGroup):
    entering_email = State()
    entering_query_keywords = State()
    choosing_query_interval = State()