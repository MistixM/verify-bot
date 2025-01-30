# Import required dependencies
from aiogram import Bot, Router, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties

from app.keyboard.inline import get_verification_keyboard

import app.const.config as config
import asyncio

# Initialize bot with token
bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

# Create dispatcher and router
dp = Dispatcher()
router = Router()

dp.include_router(router)


# Define start command handler
# Get bot and user info and send the welcome message
@router.message(Command(commands=['start']))
async def on_message(message: types.Message):
    bot_info = await bot.get_me()
    user_info = message.from_user

    await message.answer(f"Hello, {user_info.full_name}! I'm {bot_info.full_name} and I'm here to verify you before you continue your journey!",
                         reply_markup=get_verification_keyboard())


# Define callback handler
@router.callback_query(lambda d: d.data)
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data

    # If user ready to pay, send an invoice
    if data == 'start_verify':
        await callback.message.answer(f"Alright. You have to pay {config.displayed_price}$ to get channel access")
        await callback.message.answer_invoice(title='Channel access', 
                                              description='Provides channel access', 
                                              payload='channel_access', 
                                              currency='USD', 
                                              prices=[types.LabeledPrice(label='Channel accces', amount=config.price)], 
                                              provider_token=config.PAYMENT_TOKEN)

# Just before payment, check if the product is available
@router.pre_checkout_query()
async def check_payment(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)


# Filter successful payment and send a message with a private link
@router.message(F.successful_payment)
async def on_payment(message: types.Message):
    await message.answer(f"Payment successful! You can now join our channel: {config.LINK}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot started")
    
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        print("An error occurred (SystemExit or KeyboardInterrupt)")
    
    print("Bot stopped")