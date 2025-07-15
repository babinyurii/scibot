from aiogram import F, MagicFilter
from email_validator import validate_email, EmailNotValidError
from aiogram.filters import BaseFilter

from aiogram.types import Message

class EmailFilter(BaseFilter):

    async def __call__(self, message: Message):
        try:
            validate_email(message.text)
            return True
        except EmailNotValidError as e:
            return False


class QueryKeywordsFilter(BaseFilter):
    
    async def __call__(self, message: Message):
        # add if ',' not in text:
        # if text in this case is one word only still write it into db
        # if user puts only single word or expression
        if ',' not in  message.text:
            return False
        keywords = message.text.split(',')
        keywords = [keyword for keyword in keywords if keyword]
        if len(keywords) <= 3:
            return True
        else:
            return False        