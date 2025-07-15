from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram import F
from db import engine, PubMedSearch, get_query, create_query, update_email, edit_schedule_interval, update_query_keywords, check_record_exists
from pubmed_search import search, fetch_details
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from fsm_states import CreateQuery, EditQuery
from filters import EmailFilter, QueryKeywordsFilter
from keybords import create_inline_keyboard


interval_options = [('on mondays', 'mondays',),
                     ('on fridays', 'fridays'), 
                     ('last friday of the month',
                     'last_friday'),]

edit_query_options = [('email', 'edit_email',),
                     ('keywords', 'edit_query_keywords'), 
                     ('schedule', 'edit_schedule_interval'),]


router = Router()

@router.message(Command(commands=['start']))
async def start(message: Message, state: FSMContext):
    await state.clear()
    
    if check_record_exists(user=message.from_user.id):
        await message.answer(
            text="edit query (/edit_query) to edit your existing search config"
        )
        await state.update_data(editing_data=True)

    else:
        await message.answer(
            text="choose create query (/create_query) "
        )
        await state.update_data(editing_data=False)


@router.message(StateFilter(None), Command('edit_query'))
async def enter_email(message: Message, state: FSMContext):
    builder = create_inline_keyboard(edit_query_options)
    await message.answer(
        text='choose what you want to edit',
        reply_markup=builder.as_markup()
    )


@router.callback_query(StateFilter(None),
                F.data.in_(['edit_email', 'edit_query_keywords', 'edit_schedule_interval']))
async def edit_email(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == 'edit_email':
        # get email from db
        await callback.message.answer('enter email')
        await state.set_state(CreateQuery.entering_email)
    elif callback.data == 'edit_query_keywords':
        # get keywords from db
        await callback.message.answer('edit keywords')
        await state.set_state(CreateQuery.entering_query_keywords)
    else:
        # get schedule from db
        await callback.message.answer('edit shedule')
        await state.set_state(CreateQuery.choosing_query_interval)

@router.message(StateFilter(None), Command('create_query'))
async def enter_email(message: Message, state: FSMContext):
    await message.answer(
        text='enter your email'
    )
    await state.set_state(CreateQuery.entering_email)


@router.message(CreateQuery.entering_email,
                EmailFilter())
async def enter_query_keywords(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    user_data = await state.get_data()

    if user_data['editing_data']:
        update_email(user=message.from_user.id, email=user_data['email'])
        await message.answer(
            text='editing email'
        )
        await state.clear()

    else:
        await message.answer(
            text='email valid. now enter query keywords'
        )
        await state.set_state(CreateQuery.entering_query_keywords)
    


@router.message(CreateQuery.entering_email)
async def invalid_email_entered(message: Message):
    await message.answer(
        text='no valid email. try again'
    )



@router.message(
    CreateQuery.entering_query_keywords,
    QueryKeywordsFilter()
)
async def choose_query_interval(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text.lower())
   
    ######################333
    # call func to create keyboard
    ###############3333
    builder = create_inline_keyboard(interval_options)

    await message.answer(
        text='keywords valid. now choose interval',
        reply_markup=builder.as_markup(),
    )


    await state.set_state(CreateQuery.choosing_query_interval)


@router.message(CreateQuery.entering_query_keywords)
async def invalid_keywords_entered(message: Message):
    await message.answer(
        text='not valid keywords. try again'
    )


@router.callback_query(CreateQuery.choosing_query_interval,
                F.data.in_(['mondays', 'fridays', 'last_friday']))
async def finish_creating_query(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(interval=callback.data)
    user_query = await state.get_data()

    await callback.message.answer("ok, проверяем раз в месяц")
    await callback.message.answer(f"your data: {user_query['email']} \
                                   {user_query['keywords']} \
                                       {user_query['interval']}")
    await callback.message.delete()
    create_query(user=callback.from_user.id,
              user_query=user_query)
    await state.clear()
    # clear state
    # write into db
    

@router.message(CreateQuery.choosing_query_interval)
async def invalid_query_interval_entered(message: Message):
    await message.answer(
        text='not valid interval. try again'
    )



    
    
    



    