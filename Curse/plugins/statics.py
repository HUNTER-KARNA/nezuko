from pyrogram import enums,filters
from pyrogram.types import Message

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
from Curse.utils.custom_filters import command
from Curse.supports import get_support_staff

SUPPORT_STAFF = get_support_staff()
C_HANDLER = ["/", "komi ", "Komi ", "."]

@app.on_message(filters.command(["stats"], C_HANDLER), group=9696)
async def get_stats(_, m: Message):
    if m.from_user.id not in SUPPORT_STAFF:
        return
    # initialise
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

    replymsg = await m.reply_text("<b><i>Fetching Stats...</i></b>", quote=True)
    rply = (
        "📊 𝗞𝗢𝗠𝗜 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦 📊\n\n"
        "<b>Here are the statistics of the bot:</b>\n\n"
        f"<b>👥 Users:</b> <code>{(userdb.count_users())}</code> in <code>{(chatdb.count_chats())}</code> chats\n"
        f"<b>🚫 Anti Channel Pin:</b> <code>{(pinsdb.count_chats('antichannelpin'))}</code> enabled chats\n"
        f"<b>🧹 Clean Linked:</b> <code>{(pinsdb.count_chats('cleanlinked'))}</code> enabled chats\n"
        f"<b>🔍 Filters:</b> <code>{(fldb.count_filters_all())}</code> in <code>{(fldb.count_filters_chats())}</code> chats\n"
        f"<b>📝 Aliases:</b> <code>{(fldb.count_filter_aliases())}</code>\n"
        f"<b>⛔️ Blacklists:</b> <code>{(bldb.count_blacklists_all())}</code> in <code>{(bldb.count_blackists_chats())}</code> chats\n"
        f"    <b>🔧 Action Specific:</b>\n"
        f"        <b>- None:</b> <code>{(bldb.count_action_bl_all('none'))}</code> chats\n"
        f"        <b>- Kick</b> <code>{(bldb.count_action_bl_all('kick'))}</code> chats\n"
        f"        <b>- Warn:</b> <code>{(bldb.count_action_bl_all('warn'))}</code> chats\n"
        f"        <b>- Ban</b> <code>{(bldb.count_action_bl_all('ban'))}</code> chats\n"
        f"<b>📜 Rules:</b> Set in <code>{(rulesdb.count_chats_with_rules())}</code> chats\n"
        f"<b>🔒 Private Rules:</b> <code>{(rulesdb.count_privrules_chats())}</code> chats\n"
        f"<b>⚠️ Warns:</b> <code>{(warns_db.count_warns_total())}</code> in <code>{(warns_db.count_all_chats_using_warns())}</code> chats\n"
        f"<b>👤 Users Warned:</b> <code>{(warns_db.count_warned_users())}</code> users\n"
        f"    <b>🔧 Action Specific:</b>\n"
        f"        <b>- Kick</b>: <code>{(warns_settings_db.count_action_chats('kick'))}</code>\n"
        f"        <b>- Mute</b>: <code>{(warns_settings_db.count_action_chats('mute'))}</code>\n"
        f"        <b>- Ban</b>: <code>{warns_settings_db.count_action_chats('ban')}</code>\n"
        f"<b>📝 Notes:</b> <code>{(notesdb.count_all_notes())}</code> in <code>{(notesdb.count_notes_chats())}</code> chats\n"
        f"<b>🔒 Private Notes:</b> <code>{(notesettings_db.count_chats())}</code> chats\n"
        f"<b>🚫 GBanned Users:</b> <code>{(gbandb.count_gbans())}</code>\n"
        f"<b>🌟 Welcoming Users in:</b> <code>{(grtdb.count_chats('welcome'))}</code> chats\n"
        f"<b>👍 Approved People</b>: <code>{(appdb.count_all_approved())}</code> in <code>{(appdb.count_approved_chats())}</code> chats\n"
        f"<b>🗝 Disabling:</b> <code>{(dsbl.count_disabled_all())}</code> items in <code>{(dsbl.count_disabling_chats())}</code> chats.\n"
        "     <b>🔧 Action:</b>\n"
        f"        <b>- ❌ Del:</b> Applied in <code>{(dsbl.count_action_dis_all('del'))}</code> chats.\n\n"
        "<a href='https://t.me/hunter_association'>𝙐𝙋𝘿𝘼𝙏𝙀𝙎</a> | "
        "<a href='https://t.me/hunterXsupport'>𝙎𝙐𝙋𝙋𝙊𝙍𝙏</a>\n\n"
        f"「 𝙈𝘼𝘿𝙀 𝘽𝙔 <a href='t.me/hunter_karna'>𝑲𝒂𝒓𝒂𝒏</a> 」\n"
    )
    await replymsg.edit_text(
        rply, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
    )
    return

