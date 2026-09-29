import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# --- CONFIGURATION ---
API_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Yahan apna BotFather wala token daal dena
ADMIN_ID = 7812593375  # Teri Admin ID set hai

USDT_ADDRESS = "TPdV8QRBQqFis8BnH4mFrFvRYensZzJrJH"
SUPPORT_USERNAME = "@ElitePanelSupport"

# Logging setup
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# In-memory mock database for users and balances
user_balances = {}

# States for Admin balance management
class AdminStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_amount = State()

# --- KEYBOARDS ---
def main_menu_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🛒 Buy Free Fire Max Keys", callback_data="buy_keys"),
        types.InlineKeyboardButton("💰 Add Balance (USDT)", callback_data="add_balance"),
    )
    keyboard.add(
        types.InlineKeyboardButton("👤 My Profile", callback_data="profile"),
        types.InlineKeyboardButton("🤝 Reseller Program", callback_data="reseller"),
    )
    keyboard.add(
        types.InlineKeyboardButton("🎧 Support / Help", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}")
    )
    return keyboard

def payment_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("💎 Pay via USDT (TRC20)", callback_data="pay_usdt"),
        types.InlineKeyboardButton("⚠️ Having Issues? Contact Support", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}"),
        types.InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
    )
    return keyboard

def admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("➕ Add/Update User Balance", callback_data="admin_add_balance"),
        types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    )
    return keyboard

# --- HANDLERS ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    welcome_text = (
        f"🔥 *Welcome to Free Fire Max Key Store* 🔥\n\n"
        f"Get instant automated keys securely and anonymously worldwide using Crypto (USDT).\n\n"
        f"Select an option below:"
    )
    await message.reply(welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def process_main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    welcome_text = (
        f"🔥 *Free Fire Max Key Store* 🔥\n\n"
        f"Select an option below:"
    )
    await bot.edit_message_text(
        welcome_text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'add_balance')
async def process_add_balance(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = (
        f"💳 *Add Balance Instructions*\n\n"
        f"We accept international payments securely via **USDT (TRC20)** to protect your privacy and avoid any regional banking blocks.\n\n"
        f"Click below to view payment details or if you face any issues during checkout."
    )
    await bot.edit_message_text(
        text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        parse_mode="Markdown",
        reply_markup=payment_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'pay_usdt')
async def process_pay_usdt(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = (
        f"💎 *USDT (TRC20) Payment Details*\n\n"
        f"Send your USDT (TRC20) payment to the wallet address below:\n\n"
        f"`{USDT_ADDRESS}`\n\n"
        f"📌 **Instructions:**\n"
        f"1. Send the exact amount of USDT.\n"
        f"2. Take a screenshot of the completed transaction or copy the TxID (Transaction Hash).\n"
        f"3. Send the proof directly to our support manager: {SUPPORT_USERNAME}\n"
        f"4. Your balance will be credited instantly after confirmation!\n\n"
        f"⚠️ *If you encounter any payment issues or delays, contact {SUPPORT_USERNAME} immediately.*"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("🎧 Contact Support for Help", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}"),
        types.InlineKeyboardButton("🔙 Back", callback_data="add_balance")
    )
    
    await bot.edit_message_text(
        text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'profile')
async def process_profile(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    balance = user_balances.get(user_id, 0.0)
    
    text = (
        f"👤 *Your Profile*\n\n"
        f"🆔 *User ID:* `{user_id}`\n"
        f"💰 *Current Balance:* `${balance:.2f} USDT`\n\n"
        f"Need assistance? Contact {SUPPORT_USERNAME}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))
    
    await bot.edit_message_text(
        text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'reseller')
async def process_reseller(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = (
        f"🤝 *Reseller Program*\n\n"
        f"Want to sell Free Fire Max keys at wholesale rates in your region?\n"
        f"Contact our manager directly at {SUPPORT_USERNAME} to get special reseller pricing and custom panel options!"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("💬 Contact Manager", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}"),
        types.InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
    )
    await bot.edit_message_text(
        text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'buy_keys')
async def process_buy_keys(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = (
        f"🛒 *Free Fire Max Keys Store*\n\n"
        f"Please add balance to your account first using the **Add Balance (USDT)** option to purchase keys automatically."
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("💰 Add Balance", callback_data="add_balance"),
        types.InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")
    )
    await bot.edit_message_text(
        text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# --- ADMIN PANEL COMMANDS ---
@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("❌ You are not authorized to use the admin panel.")
        return
    
    await message.reply(
        "🛠 *Admin Control Panel*\n\nManage user balances and keys below:",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'admin_add_balance')
async def admin_add_balance_start(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.reply("Send me the **Telegram User ID** of the customer:")
    await AdminStates.waiting_for_user_id.set()

@dp.message_handler(state=AdminStates.waiting_for_user_id)
async def admin_received_user_id(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        target_user_id = int(message.text.strip())
        async with state.proxy() as data:
            data['target_user_id'] = target_user_id
        await message.reply("Now send the **amount in USDT** to add (e.g., `10` or `5.5`):")
        await AdminStates.waiting_for_amount.set()
    except ValueError:
        await message.reply("❌ Invalid User ID. Please send a valid numeric Telegram ID:")

@dp.message_handler(state=AdminStates.waiting_for_amount)
async def admin_received_amount(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        amount = float(message.text.strip())
        async with state.proxy() as data:
            target_user_id = data['target_user_id']
        
        current_bal = user_balances.get(target_user_id, 0.0)
        user_balances[target_user_id] = current_bal + amount
        
        await message.reply(f"✅ Successfully added `{amount} USDT` to User `{target_user_id}`.\nNew Balance: `{user_balances[target_user_id]} USDT`", parse_mode="Markdown")
        await state.finish()
    except ValueError:
        await message.reply("❌ Invalid amount. Please enter a valid number:")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
