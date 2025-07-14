from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


interval_options = [('on mondays', 'mondays',),
                     ('on fridays', 'fridays'), 
                     ('last friday of the month',
                     'last_friday'),]


def create_interval_choose_keyboard():
    builder = InlineKeyboardBuilder()
    for opt in interval_options:
        builder.add(
            types.InlineKeyboardButton(
                text=opt[0],
                callback_data=opt[1]
                                      )
                )
    return builder