from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram import F
from db import (engine, 
                PubMedSearch, 
                get_record_keywords, 
                get_record_email,
                get_record_schedule_interval,
                create_query, 
                update_email, 
                update_schedule_interval, 
                update_keywords, 
                check_record_exists,)
from pubmed_search import search, fetch_details
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from fsm_states import CreateQuery
from filters import EmailFilter, QueryKeywordsFilter, update_keywords
from keybords import create_inline_keyboard


interval_options = [('on mondays', 'mondays',),
                     ('on fridays', 'fridays'), 
                     ('last friday of the month',
                     'last_friday'),]

edit_query_options = [('email', 'edit_email',),
                     ('keywords', 'edit_query_keywords'), 
                     ('schedule', 'edit_schedule_interval'),]


router = Router()


@router.message(StateFilter(None), Command(commands=['cancel']))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text='нечего отменять',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=['cancel']))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='действие отменено',
    )


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
async def show_editing_options(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if 'editing_data' not in user_data.keys():
        await state.update_data(editing_data=True)
    builder = create_inline_keyboard(edit_query_options)
    await message.answer(
        text='choose what you want to edit',
        reply_markup=builder.as_markup()
    )


@router.callback_query(StateFilter(None),
                F.data.in_(['edit_email', 'edit_query_keywords', 'edit_schedule_interval']))
async def edit_user_record(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == 'edit_email':
        previous_email = get_record_email(user=callback.from_user.id,)
        await callback.message.answer(f'your previous email is: <b>{previous_email}</b>.\nsend me message with your new email')
        await state.set_state(CreateQuery.entering_email)

    elif callback.data == 'edit_query_keywords':
        previous_keywords = get_record_keywords(user=callback.from_user.id,)
        await callback.message.answer(f'your previous keywords are: <b>{previous_keywords}</b>.\nsend me message with your new keywords')
        await state.set_state(CreateQuery.entering_query_keywords)

    else:
        previous_interval = get_record_schedule_interval(user=callback.from_user.id,)
        builder = create_inline_keyboard(interval_options)
        await callback.message.answer(f'your previous schedule is: <b>{previous_interval}</b>.\nchoose your new schedule:', reply_markup=builder.as_markup())
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
        await message.answer(text='editing email')
        await state.clear()
    else:
        await message.answer(text='email valid. now enter query keywords')
        await state.set_state(CreateQuery.entering_query_keywords)
    

@router.message(CreateQuery.entering_email)
async def invalid_email_entered(message: Message):
    await message.answer(text='no valid email. try again')


@router.message(
    CreateQuery.entering_query_keywords,
    QueryKeywordsFilter()
)
async def choose_query_interval(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text.lower()) # TODO call validate_email to get normalized see docs:

    user_data = await state.get_data()

    if user_data['editing_data']:
        keywords = clean_keywords(user_data['keywords'])
        update_keywords(user=message.from_user.id, query_words=keywords)
        await message.answer(text='editing keywords')
        await state.clear() 

    else:
        builder = create_inline_keyboard(interval_options)

        await message.answer(text='keywords valid. now choose interval',
                            reply_markup=builder.as_markup())
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
    if user_query['editing_data']:
        update_schedule_interval(user=callback.from_user.id, schedule_interval=user_query['interval'])
        await callback.message.answer(f"ok, проверяем так: {user_query['interval']}")

    else:
        await callback.message.answer(f"ok, проверяем так: {user_query['interval']}")
        await callback.message.answer(f"your data: {user_query['email']} \
                                    {user_query['keywords']} \
                                        {user_query['interval']}")
        
        create_query(user=callback.from_user.id,
                user_query=user_query)

    await callback.message.delete()
    await state.clear()
  
    

@router.message(CreateQuery.choosing_query_interval)
async def invalid_query_interval_entered(message: Message):
    await message.answer(text='not valid interval. please use buttons')



@router.message(F.text)
async def invalid_any_message(message: Message):
    await message.answer(text='dont know such commands. please use the menu')





    
    
    



    