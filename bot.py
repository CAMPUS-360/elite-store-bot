import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Tera API Token aur Username update kar diya gaya hai
API_TOKEN = '8838714463:AAGG4spzF68PJQVeEcxZ_d5dF6G7bBnyIyY'
ADMIN_USERNAME = 'Elitepanelstore_bot'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Main Menu Keyboard (Jaisa screenshot mein hai)
def get_main_menu(user_name):
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Row 1
    keyboard.add(InlineKeyboardButton("🟢 Shop Store", callback_data="shop_store"))
    
    # Row 2
    keyboard.add(
        InlineKeyboardButton("💵 Add Balance", callback_data="add_balance"),
        InlineKeyboardButton("📦 My Orders", callback_data="my_orders")
    )
    
    # Row 3
    keyboard.add(
        InlineKeyboardButton("👤 My Profile", callback_data="my_profile"),
        InlineKeyboardButton("🎁 Referral", callback_data="referral")
    )
    
    # Row 4
    keyboard.add(
        InlineKeyboardButton("🔴 How To Use", callback_data="how_to_use"),
        InlineKeyboardButton("🎡 Lucky Spin", callback_data="lucky_spin")
    )
    
    # Row 5
    keyboard.add(
        InlineKeyboardButton("🔗 Share Bot", callback_data="share_bot"),
        InlineKeyboardButton("💼 Become Reseller", callback_data="become_reseller")
    )
    
    # Row 6
    keyboard.add(InlineKeyboardButton("💬 Support", callback_data="support"))
    
    return keyboard

# /start Command Handler
@dp.message_handler(commands=['start'])
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

# Back button markup
def get_back_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_main"))
    return keyboard

# Callback Query Handlers (Buttons Action)
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    code = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    
    if code == "shop_store":
        text = "🛍️ **Shop Store**\n\nAbhi koi product available nahi hai. Admin jald hi keys add karega."
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "add_balance":
        text = f"💵 **Add Balance**\n\nBalance add karne ke liye admin ko payment ka screenshot bhejein:\n👉 @{ADMIN_USERNAME}"
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "my_orders":
        text = "📦 **My Orders**\n\nAapne abhi tak koi order nahi kiya hai."
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "my_profile":
        user = callback_query.from_user
        text = (
            f"👤 **My Profile**\n\n"
            f"🆔 User ID: `{user.id}`\n"
            f"👤 Name: {user.first_name}\n"
            f"💰 Balance: ₹0\n"
            f"💸 Total Spent: ₹0"
        )
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "referral":
        text = f"🎁 **Referral System**\n\nAapka referral link:\n`https://t.me/{ADMIN_USERNAME}?start=ref_" + str(callback_query.from_user.id) + "`\n\nJab 5 dost isse buy karenge, toh 7 days ka panel free milega!"
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "how_to_use":
        text = "🔴 **How To Use**\n\nYahan par saare panels ke demo videos aur setup guide milenge."
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "lucky_spin":
        text = "🎡 **Lucky Spin**\n\nYeh feature jald hi aa raha hai! Stay tuned."
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "share_bot":
        text = f"🔗 **Share Bot**\n\nApne doston ke sath bot share karein:\n`https://t.me/{ADMIN_USERNAME}`"
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "become_reseller":
        text = f"💼 **Become Reseller**\n\nReseller banne ke liye seedha admin se contact karein:\n👉 @{ADMIN_USERNAME}"
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "support":
        text = f"💬 **Support**\n\nKisi bhi madad ke liye yahan contact karein:\n👉 @{ADMIN_USERNAME}"
        await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_back_keyboard(), parse_mode="Markdown")
        
    elif code == "back_to_main":
        user_name = callback_query.from_user.first_name
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
        await bot.edit_message_text(welcome_text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=get_main_menu(user_name), parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
