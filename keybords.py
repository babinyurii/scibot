from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types




def create_inline_keyboard(opts):
    builder = InlineKeyboardBuilder()
    for opt in opts:
        builder.add(
            types.InlineKeyboardButton(
                text=opt[0],
                callback_data=opt[1]
                                      )
                )
    return builder