from pyrogram import enums, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Curse.bot_class import app
from Curse.database.antispam_db import GBan
from Curse.database.approve_db import Approve
from Curse.database.blacklist_db import Blacklist
from Curse.database.chats_db import Chats
from Curse.database.disable_db import Disabling
from Curse.database.filters_db import Filters
from Curse.database.greetings_db import Greetings
from Curse.database.notes_db import Notes, NotesSettings
from Curse.database.pins_db import Pins
from Curse.database.rules_db import Rules
from Curse.database.users_db import Users
from Curse.database.warns_db import Warns, WarnSettings

OWNER_ID = 7282828
C_HANDLER = ["/", "nuezko ", "nuezko ", "."]

@app.on_message(filters.command(["stats"], C_HANDLER), group=9696)
async def get_stats(_, m: Message):
    
    if m.from_user.id != OWNER_ID:
        await m.reply_text("This command is only for the owner baka.", quote=True)
        return

    bldb = Blacklist
    gbandb = GBan()
    notesdb = Notes()
    grtdb = Greetings
    rulesdb = Rules
    userdb = Users
    dsbl = Disabling
    appdb = Approve
    chatdb = Chats
    fldb = Filters()
    pinsdb = Pins
    notesettings_db = NotesSettings()
    warns_db = Warns
    warns_settings_db = WarnSettings

    stats = (
        f"╒═══「 <b>System Statistics</b> 」\n\n"
        f"➢ <b>System Start Time:</b> 2024-10-26 16:57:36\n"
        f"➢ <b>System:</b> Linux\n"
        f"➢ <b>Node Name:</b> Management\n"
        f"➢ <b>Release:</b> 5.15.0-113-generic\n"
        f"➢ <b>Machine:</b> x86_64\n"
        f"➢ <b>CPU:</b> 0.0 %\n"
        f"➢ <b>RAM:</b> 22.3 %\n"
        f"➢ <b>Storage:</b> 3.7 %\n\n"
        f"➢ <b>Python Version:</b> 3.10.12\n"
        f"➢ <b>python-Telegram-Bot:</b> 13.13\n"
        f"➢ <b>Uptime:</b> 11h:31m:30s\n\n"
        "╒═══「 <b>Bot Statistics</b> 」\n\n"
        f"• <b>Users:</b> <code>{userdb.count_users()}</code> across <code>{chatdb.count_chats()}</code> chats\n"
        f"• <b>Global Banned Users:</b> {gbandb.count_gbans()}\n"
        f"• <b>Blacklist Stickers:</b> {bldb.count_blacklists_all()} across {bldb.count_blackists_chats()} chats\n"
        f"• <b>Notes:</b> {notesdb.count_all_notes()} across {notesdb.count_notes_chats()} chats\n"
        f"• <b>Filters:</b> {fldb.count_filters_all()} across {fldb.count_filters_chats()} chats\n"
        f"• <b>Disabled Items:</b> {dsbl.count_disabled_all()} across {dsbl.count_disabling_chats()} chats\n"
        f"• <b>Rules Set:</b> {rulesdb.count_chats_with_rules()} chats\n"
        f"• <b>Total Users:</b> <code>{userdb.count_users()}</code> in <code>{chatdb.count_chats()}</code> chats\n"
        f"• <b>Warns:</b> {warns_db.count_warns_total()} across {warns_db.count_all_chats_using_warns()} chats\n\n"
        "🔗 <a href='https://t.me/hunter_association'>Updates</a> | "
        "<a href='https://t.me/hunterXsupport'>Support</a>\n\n"
        f"「 <b>Made by</b> <a href='t.me/hunter_karna'>𝑲𝒂𝒓𝒂𝒏</a> 」\n"
    )

    
    await m.reply_text(
        "Click the button below to view the stats.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("View Stats", callback_data="view_stats")]]
        ),
        quote=True,
    )

@app.on_callback_query(filters.regex("view_stats"))
async def show_stats(_, query):
    if query.from_user.id != OWNER_ID:
        await query.answer("Only the owner can view this.", show_alert=True)
        return
    await query.message.edit_text(
        stats,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )
