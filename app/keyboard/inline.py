from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_verification_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Let's move on", callback_data='start_verify')]])

    return keyboard


