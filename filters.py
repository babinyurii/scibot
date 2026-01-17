from aiogram import F, MagicFilter
from email_validator import validate_email, EmailNotValidError
from aiogram.filters import BaseFilter

from aiogram.types import Message
from string import ascii_letters
import re

REG_EXP = '^[A-Za-z0-9 -]*$'

class EmailFilter(BaseFilter):

    async def __call__(self, message: Message):
        try:
            validate_email(message.text)
            return True
        except EmailNotValidError as e:
            return False


class QueryKeywordsFilter(BaseFilter):
    
    async def __call__(self, message: Message):
       
        if ',' not in message.text:
            if re.match(REG_EXP, message.text):
                return True
            else:
                return False
        else:
            keywords = message.text.split(',')
            keywords = [keyword for keyword in keywords if keyword]
            for keyword in keywords:
                if re.match(REG_EXP, keyword):
                    continue
                else:
                    return False

            if len(keywords) <= 3:
                return True
            else:
                return False    

def clean_keywords(keywords):
    keywords = keywords.split(',')
    keywords = [keyword for keyword in keywords if keyword]
    keywords = [keyword.strip() for keyword in keywords]
    return keywords
