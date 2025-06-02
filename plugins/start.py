# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.

from shared_client import app
from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOG_GROUP, OWNER_ID, FORCE_SUB

async def subscribe(app, message):
    if FORCE_SUB:
        try:
            user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
            if str(user.status) == "ChatMemberStatus.BANNED":
                await message.reply_text("You are Banned. Contact -- @Aublic")
                return 1
        except UserNotParticipant:
            link = await app.export_chat_invite_link(FORCE_SUB)
            caption = f"Join our channel to use the bot"
            await message.reply_photo(
                photo="https://graph.org/file/d44f024a08ded19452152.jpg",
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Now...", url=f"{link}")]]
                )
            )
            return 1
        except Exception as ggn:
            await message.reply_text(f"Something Went Wrong. Contact admins... with message: {ggn}")
            return 1

@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("❌ You are not authorized to use this command.")
        return

    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("setbot", "🧸 Add your bot for handling files"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("rembot", "🤨 Remove your custom bot"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel login/batch/settings process"),
        BotCommand("stop", "🚫 Cancel batch process"),
        BotCommand("get", "📄 Get all user IDs (owner)"),
        BotCommand("lock", "🔒 Lock channel (owner)"),
        BotCommand("stats", "📊 Bot statistics"),
        BotCommand("speedtest", "⚡ Check speed"),
        BotCommand("myplan", "💎 View plan details"),
        BotCommand("session", "🔐 Generate session string")
    ])

    await message.reply("✅ All commands configured successfully!")

# Help Pagination
help_pages = [
    (
        "📝 **Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n> Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n> Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n> Transfer premium to others (Premium only)\n\n"
        "4. **/get**\n> Get all user IDs (Owner only)\n\n"
        "5. **/lock**\n> Lock channel from extraction (Owner only)\n\n"
        "6. **/dl link**\n> Download videos\n\n"
        "7. **/adl link**\n> Download audio\n\n"
        "8. **/login**\n> Log into the bot\n\n"
        "9. **/batch**\n> Bulk extraction for posts\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n> Logout from the bot\n\n"
        "11. **/stats**\n> Get bot stats\n\n"
        "12. **/speedtest**\n> Test server speed\n\n"
        "13. **/cancel**\n> Cancel ongoing batch\n\n"
        "14. **/myplan**\n> Get your plan details\n\n"
        "15. **/session**\n> Generate session string\n\n"
        "16. **/settings**\n> Personalize settings like rename, caption, etc.\n\n"
        "**__Powered by Aublicx_Robot__**"
    )
]

async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return

    buttons = []
    if page_number > 0:
        buttons.append(InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}"))
    if page_number < len(help_pages) - 1:
        buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}"))

    keyboard = InlineKeyboardMarkup([buttons]) if buttons else None

    await message.delete()
    await message.reply(help_pages[page_number], reply_markup=keyboard)

@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
    await send_or_edit_help_page(client, message, 0)

@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
    page_number += -1 if action == "prev" else 1
    await send_or_edit_help_page(client, callback_query.message, page_number)
    await callback_query.answer()
