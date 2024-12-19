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

OWNER_IDS = {6965147961, 7710262210}  
C_HANDLER = ["/", "nezuko", "Nezuko", "."]

@app.on_message(filters.command(["stats"], C_HANDLER), group=9696)
async def get_stats(_, m: Message):
    if m.from_user.id not in OWNER_IDS:
        await m.reply_text("This command is only for the owner, baka.", quote=True)
        return

    
    bldb = Blacklist()
    gbandb = GBan()
    notesdb = Notes()
    grtdb = Greetings()
    rulesdb = Rules()
    userdb = Users()
    dsbl = Disabling()
    appdb = Approve()
    chatdb = Chats()
    fldb = Filters()
    pinsdb = Pins()
    notesettings_db = NotesSettings()
    warns_db = Warns()
    warns_settings_db = WarnSettings()

    stats = (
        f"System Statistics:\n\n"
        f"System Start Time: 2024-10-26 16:57:36\n"
        f"System: Linux\n"
        f"Node Name: Management\n"
        f"Release: 5.15.0-113-generic\n"
        f"Machine: x86_64\n"
        f"CPU: 0.0 %\n"
        f"RAM: 22.3 %\n"
        f"Storage: 3.7 %\n\n"
        f"Bot Statistics:\n\n"
        f"Users: {userdb.count_users()} across {chatdb.count_chats()} chats\n"
        f"Global Banned Users: {gbandb.count_gbans()}\n"
        f"Blacklist Stickers: {bldb.count_blacklists_all()} across {bldb.count_blackists_chats()} chats\n"
        f"Notes: {notesdb.count_all_notes()} across {notesdb.count_notes_chats()} chats\n"
        f"Filters: {fldb.count_filters_all()} across {fldb.count_filters_chats()} chats\n"
        f"Disabled Items: {dsbl.count_disabled_all()} across {dsbl.count_disabling_chats()} chats\n"
        f"Rules Set: {rulesdb.count_chats_with_rules()} chats\n"
        f"Total Users: {userdb.count_users()} in {chatdb.count_chats()} chats\n"
        f"Warns: {warns_db.count_warns_total()} across {warns_db.count_all_chats_using_warns()} chats\n"
    )

    await m.reply_text(
        "Click the button below to view the stats.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("View Stats", callback_data=f"view_stats")]]
        ),
        quote=True,
    )

@app.on_callback_query(filters.regex(r"view_stats"))
async def show_stats(_, query):
    if query.from_user.id not in OWNER_IDS:
        await query.answer("Only the owner can view this.", show_alert=True)
        return

    
    bldb = Blacklist()
    gbandb = GBan()
    notesdb = Notes()
    grtdb = Greetings()
    rulesdb = Rules()
    userdb = Users()
    dsbl = Disabling()
    appdb = Approve()
    chatdb = Chats()
    fldb = Filters()
    pinsdb = Pins()
    notesettings_db = NotesSettings()
    warns_db = Warns()
    warns_settings_db = WarnSettings()

    stats = (
        f"System Statistics:\n\n"
        f"System Start Time: 2024-10-26 16:57:36\n"
        f"System: Linux\n"
        f"Node Name: Management\n"
        f"Release: 5.15.0-113-generic\n"
        f"Machine: x86_64\n"
        f"CPU: 0.0 %\n"
        f"RAM: 22.3 %\n"
        f"Storage: 3.7 %\n\n"
        f"Bot Statistics:\n\n"
        f"Users: {userdb.count_users()} across {chatdb.count_chats()} chats\n"
        f"Global Banned Users: {gbandb.count_gbans()}\n"
        f"Blacklist Stickers: {bldb.count_blacklists_all()} across {bldb.count_blackists_chats()} chats\n"
        f"Notes: {notesdb.count_all_notes()} across {notesdb.count_notes_chats()} chats\n"
        f"Filters: {fldb.count_filters_all()} across {fldb.count_filters_chats()} chats\n"
        f"Disabled Items: {dsbl.count_disabled_all()} across {dsbl.count_disabling_chats()} chats\n"
        f"Rules Set: {rulesdb.count_chats_with_rules()} chats\n"
        f"Total Users: {userdb.count_users()} in {chatdb.count_chats()} chats\n"
        f"Warns: {warns_db.count_warns_total()} across {warns_db.count_all_chats_using_warns()} chats\n"
    )

    await query.answer(stats, show_alert=True)
