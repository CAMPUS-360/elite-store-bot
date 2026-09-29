import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '8838714463:AAGG4spzF68PJQVeEcxZ_d5dF6G7bBnyIyY'
ADMIN_USERNAME = 'Elitepanelstore_bot'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Main Menu Keyboard
def get_main_menu(user_name):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Shop Store", callback_data="shop_store")],
        [
            InlineKeyboardButton(text="💵 Add Balance", callback_data="add_balance"),
            InlineKeyboardButton(text="📦 My Orders", callback_data="my_orders")
        ],
        [
            InlineKeyboardButton(text="👤 My Profile", callback_data="my_profile"),
            InlineKeyboardButton(text="🎁 Referral", callback_data="referral")
        ],
        [
            InlineKeyboardButton(text="🔴 How To Use", callback_data="how_to_use"),
            InlineKeyboardButton(text="🎡 Lucky Spin", callback_data="lucky_spin")
        ],
        [
            InlineKeyboardButton(text="🔗 Share Bot", callback_data="share_bot"),
            InlineKeyboardButton(text="💼 Become Reseller", callback_data="become_reseller")
        ],
        [InlineKeyboardButton(text="💬 Support", callback_data="support")]
    ])
    return keyboard

def get_back_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")]
    ])
    return keyboard

# /start Command Handler
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"👋 Hello, {user_name}!\n\n"
        f"🔑 Premium digital keys, instant delivery.\n\n"
        f"— 🛍️ Wide product catalog\n"
        f"— ⚡ Instant key delivery\n"
        f"— 💳 Multiple payment gateways\n"
        f"— 🎁 Referrals & spin-to-win\n"
        f"— 🛡️ 24/7 admin support\n\n"
        f"👇 Choose an option below to continue."
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(user_name))

# Callback Query Handlers
@dp.callback_query(F.data == "shop_store")
async def cb_shop(callback: types.CallbackQuery):
    text = "🛍️ **Shop Store**\n\nAbhi koi product available nahi hai. Admin jald hi keys add karega."
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "add_balance")
async def cb_balance(callback: types.CallbackQuery):
    text = f"💵 **Add Balance**\n\nBalance add karne ke liye admin ko payment ka screenshot bhejein:\n👉 @{ADMIN_USERNAME}"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "my_orders")
async def cb_orders(callback: types.CallbackQuery):
    text = "📦 **My Orders**\n\nAapne abhi tak koi order nahi kiya hai."
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "my_profile")
async def cb_profile(callback: types.CallbackQuery):
    user = callback.from_user
    text = (
        f"👤 **My Profile**\n\n"
        f"🆔 User ID: `{user.id}`\n"
        f"👤 Name: {user.first_name}\n"
        f"💰 Balance: ₹0\n"
        f"💸 Total Spent: ₹0"
    )
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "referral")
async def cb_referral(callback: types.CallbackQuery):
    text = f"🎁 **Referral System**\n\nAapka referral link:\n`https://t.me/{ADMIN_USERNAME}?start=ref_{callback.from_user.id}`\n\nJab 5 dost isse buy karenge, toh 7 days ka panel free milega!"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "how_to_use")
async def cb_how(callback: types.CallbackQuery):
    text = "🔴 **How To Use**\n\nYahan par saare panels ke demo videos aur setup guide milenge."
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "lucky_spin")
async def cb_spin(callback: types.CallbackQuery):
    text = "🎡 **Lucky Spin**\n\nYeh feature jald hi aa raha hai! Stay tuned."
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "share_bot")
async def cb_share(callback: types.CallbackQuery):
    text = f"🔗 **Share Bot**\n\nApne doston ke sath bot share karein:\n`https://t.me/{ADMIN_USERNAME}`"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "become_reseller")
async def cb_reseller(callback: types.CallbackQuery):
    text = f"💼 **Become Reseller**\n\nReseller banne ke liye seedha admin se contact karein:\n👉 @{ADMIN_USERNAME}"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "support")
async def cb_support(callback: types.CallbackQuery):
    text = f"💬 **Support**\n\nKisi bhi madad ke liye yahan contact karein:\n👉 @{ADMIN_USERNAME}"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def cb_back(callback: types.CallbackQuery):
    user_name = callback.from_user.first_name
    welcome_text = (
        f"👋 Hello, {user_name}!\n\n"
        f"🔑 Premium digital keys, instant delivery.\n\n"
        f"— 🛍️ Wide product catalog\n"
        f"— ⚡ Instant key delivery\n"
        f"— 💳 Multiple payment gateways\n"
        f"— 🎁 Referrals & spin-to-win\n"
        f"— 🛡️ 24/7 admin support\n\n"
        f"👇 Choose an option below to continue."
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu(user_name), parse_mode="Markdown")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
