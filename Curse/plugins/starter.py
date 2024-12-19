import os
import re
from random import choice
from time import gmtime, strftime, time

from pyrogram import enums, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType
from pyrogram.errors import (MediaCaptionTooLong, MessageNotModified,
                             QueryIdInvalid, UserIsBlocked)
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from Curse import (HELP_COMMANDS, LOGGER, PYROGRAM_VERSION, PYTHON_VERSION,
                    UPTIME, VERSION)
from Curse.bot_class import app
from Curse.utils.custom_filters import command
from Curse.utils.extras import StartPic
from Curse.utils.kbhelpers import ikb
from Curse.utils.start_utils import (gen_cmds_kb, gen_start_kb, get_help_msg,
                                      get_private_note, get_private_rules)
from Curse.vars import Config
from Curse.utils.paginate import paginate_modules

C_HANDLER = ["/", "nezuko ", "Nezuko ", "."]

@app.on_callback_query(filters.regex("^donate$"))
async def handle_donate_callback(_, query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
      """
Hᴇʏ Tʜᴀɴᴋs ғᴏʀ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛ ᴏғ ᴅᴏɴᴀᴛɪɴɢ ᴍᴇ!
Wʜᴇɴ ʏᴏᴜ ᴅᴏɴᴀᴛᴇ, ᴀʟʟ ᴛʜᴇ ғᴜɴᴅ ɢᴏᴇs ᴛᴏᴡᴀʀᴅs ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ ᴡʜɪᴄʜ ᴍᴀᴋᴇs ᴏɴ ғᴀsᴛ ᴀɴᴅ ʀᴇsᴘᴏɴsɪᴠᴇ.
Yᴏᴜʀ ᴅᴏɴᴀᴛɪᴏɴ ᴍɪɢʜᴛ ᴀʟsᴏ ᴍᴇ ɢᴇᴛ ᴍᴇ ᴀ ɴᴇᴡ ғᴇᴀᴛᴜʀᴇ ᴏʀ ᴛᴡᴏ, ᴡʜɪᴄʜ I ᴡᴀsɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ɢᴇᴛ ᴅᴜᴇ ᴛᴏ sᴇʀᴠᴇʀ ʟɪᴍɪᴛᴀᴛɪᴏɴs.

Aʟʟ ᴛʜᴇ ғᴜɴᴅ ᴡᴏᴜʟᴅ ʙᴇ ᴘᴜᴛ ɪɴᴛᴏ ᴍʏ sᴇʀᴠɪᴄᴇs sᴜᴄʜ ᴀs ᴅᴀᴛᴀʙᴀsᴇ, sᴛᴏʀᴀɢᴇ ᴀɴᴅ ʜᴏsᴛɪɴɢ!

Yᴏᴜ ᴄᴀɴ ᴅᴏɴᴀᴛᴇ ʙʏ ᴄᴏɴᴛᴀᴄᴛɪɴɢ ᴍʏ ᴏᴡɴᴇʀ: [𝑲𝒂𝒓𝒂𝒏](https://t.me/hunter_karna)
     """,
  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝗗𝗢𝗡𝗔𝗧𝗘 𝗡𝗢𝗪", url="https://t.me/hunter_karan"),
                ],
                [InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="start_back")],
            ],
        ),
    ),

    LOGGER.info(f"{m.from_user.id} fetched donation text in {m.chat.id}")
    await m.reply_photo(photo=str(choice(StartPic)), caption=cpt)
    return

@app.on_callback_query(filters.regex("^close_admin$"))
async def close_admin_callback(_, q: CallbackQuery):
    user_id = q.from_user.id
    user_status = (await q.message.chat.get_member(user_id)).status
    if user_status not in {CMS.OWNER, CMS.ADMINISTRATOR}:
        await q.answer(
            "Yᴏᴜ'ʀᴇ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴛʀʏ ᴛʜɪs ᴇxᴘʟᴏsɪᴠᴇ sʜɪᴛ!",
            show_alert=True,
        )
        return
    if user_status != CMS.OWNER:
        await q.answer(
            "You're just an admin, not owner\nStay in your limits!",
            show_alert=True,
        )
        return
    await q.message.edit_text("Closed!")
    await q.answer("Closed menu!", show_alert=True)
    return


@app.on_message(filters.command(["start"], C_HANDLER), group=696969)
async def start(c: app, m: Message):

    if m.chat.type == ChatType.PRIVATE:
        if len(m.text.strip().split()) > 1:
            help_option = (m.text.split(None, 1)[1]).lower()

            if help_option.startswith("note") and (
                help_option not in ("note", "notes")
            ):
                await get_private_note(c, m, help_option)
                return
    
            if help_option.startswith("rules"):
                LOGGER.info(f"{m.from_user.id} fetched privaterules in {m.chat.id}")
                await get_private_rules(c, m, help_option)
                return

            help_msg, help_kb = await get_help_msg(m, help_option)

            if not help_msg:
                return
            elif help_msg:
                await m.reply_photo(
                    photo=str(choice(StartPic)),
                    caption=help_msg,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=help_kb,
                    quote=True,
                )
                return
            if len(help_option.split("_",1)) == 2:
                if help_option.split("_")[1] == "help":
                    await m.reply_photo(
                        photo=str(choice(StartPic)),
                        caption=help_msg,
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=help_kb,
                        quote=True,
                    )
                    return
                
        try:
            cpt = f"""
Hᴇʟʟᴏ [{m.from_user.first_name}](http://t.me/{m.from_user.username}), Mʏsᴇʟғ ɴᴇᴢᴜᴋᴏ ᴋᴀᴍᴀᴅᴏ 🫧✨ 🌸 

•𝐌𝐲 𝐈𝐧𝐟𝐨  ➲  ʜᴇʏ ' ᴅᴇᴀʀ ɪᴍ ɴᴇᴢᴜᴋᴏ Kᴀᴍᴀᴅᴏ, ᴀɴ ᴀɴɪᴍᴇ ᴛʜᴇᴍᴇᴅ ʙᴀsᴇᴅ ᴀᴅᴠᴀɴᴄᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.🫧

•𝐌𝐲 𝐉𝐨𝐛  ➲ I ᴀᴍ ᴛʜᴇ ᴘᴏᴡᴇʀғᴜʟʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡɪᴛʜ ᴀɪ ᴀʀᴛɪғɪᴄɪᴀʟ ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ . Mʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ғᴜɴᴄᴛɪᴏɴs ᴀʀᴇ ᴘᴇʀғᴇᴄᴛ ғᴏʀ ᴋᴇᴇᴘɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀɢᴀɴɪᴢᴇᴅ, ᴇɴɢᴀɢᴇᴅ, ᴀɴᴅ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ sᴘᴀᴍ-ғʀᴇᴇ! Wɪᴛʜ ʟᴏᴛs ᴏғ ғᴇᴀᴛᴜʀᴇs ✨

➖➖➖➖➖➖➖➖➖➖➖➖➖➖🫧✨🌸💗

• Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ!💗
 """

            await m.reply_photo(
                photo=str(choice(StartPic)),
                caption=cpt,
                reply_markup=(await gen_start_kb(m)),
                quote=True,
            )
        except UserIsBlocked:
            LOGGER.warning(f"Bot blocked by {m.from_user.id}")
    else:
      kb = InlineKeyboardMarkup(
        [
          [
            InlineKeyboardButton(
              "Connect me to pm", 
              url=f"https://{Config.BOT_USERNAME}.t.me/",
            ),
          ],
        ],
      )
        
      await m.reply_photo(
        photo=str(choice(StartPic)),
        caption="I'm alive :3",
        reply_markup=kb,
        quote=True,
      )
    return


@app.on_callback_query(filters.regex("^start_back$"))
async def start_back(_, q: CallbackQuery):
    try:
        cpt = f"""
Hᴇʟʟᴏ [{m.from_user.first_name}](http://t.me/{m.from_user.username}), Mʏsᴇʟғ ɴᴇᴢᴜᴋᴏ ᴋᴀᴍᴀᴅᴏ 🫧✨ 🌸 

•𝐌𝐲 𝐈𝐧𝐟𝐨  ➲  ʜᴇʏ ' ᴅᴇᴀʀ ɪᴍ ɴᴇᴢᴜᴋᴏ Kᴀᴍᴀᴅᴏ, ᴀɴ ᴀɴɪᴍᴇ ᴛʜᴇᴍᴇᴅ ʙᴀsᴇᴅ ᴀᴅᴠᴀɴᴄᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.🫧

•𝐌𝐲 𝐉𝐨𝐛  ➲ I ᴀᴍ ᴛʜᴇ ᴘᴏᴡᴇʀғᴜʟʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡɪᴛʜ ᴀɪ ᴀʀᴛɪғɪᴄɪᴀʟ ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ . Mʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ғᴜɴᴄᴛɪᴏɴs ᴀʀᴇ ᴘᴇʀғᴇᴄᴛ ғᴏʀ ᴋᴇᴇᴘɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀɢᴀɴɪᴢᴇᴅ, ᴇɴɢᴀɢᴇᴅ, ᴀɴᴅ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ sᴘᴀᴍ-ғʀᴇᴇ! Wɪᴛʜ ʟᴏᴛs ᴏғ ғᴇᴀᴛᴜʀᴇs ✨

➖➖➖➖➖➖➖➖➖➖➖➖➖➖🫧✨🌸💗

• Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ!💗
 """

        await q.edit_message_caption(
            caption=cpt,
            reply_markup=(await gen_start_kb(q.message)),
        )
    except MessageNotModified:
        pass
    await q.answer()
    return


@app.on_callback_query(filters.regex("^commands$"))
async def commands_menu(_, q: CallbackQuery):
    # ou = await gen_cmds_kb(q.message)
    # keyboard = ikb(ou, True)
    # try:
        cpt = f"""
 🌸𝗡𝗲𝘇𝘂𝗸𝗼 🌸 
 
☉ 𝗗𝗶𝘀𝗰𝗼𝘃𝗲𝗿 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘂𝘀𝗲 𝗲𝗳𝗳𝗼𝗿𝘁𝗹𝗲𝘀𝘀𝗹𝘆.                 

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /

Yᴏᴜ ᴄᴀɴ ᴜsᴇ`$` ᴀɴᴅ `!` ɪɴ ᴘʟᴀᴄᴇᴄ ᴏғ / ᴀs ʏᴏᴜʀ ᴘʀᴇғɪx ʜᴀɴᴅʟᴇʀ
"""

        await q.edit_message_caption(
            caption=cpt,
            reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELP_COMMANDS, "help")
                ),
        )
    # except MessageNotModified:
    #     pass
    # except QueryIdInvalid:
    #     await q.message.reply_photo(
    #         photo=str(choice(StartPic)), caption=cpt, reply_markup=keyboard
    #     )

    # await q.answer()
    # return


@app.on_message(filters.command(["help"], C_HANDLER), group=1001)
async def help_menu(_, m: Message):
    if len(m.text.split()) >= 2:
        textt = m.text.replace(" ","_",).replace("_"," ",1)
        help_option = (textt.split(None)[1]).lower()
        help_msg, help_kb = await get_help_msg(m, help_option)

        if not help_msg:
            LOGGER.error(f"No help_msg found for help_option - {help_option}!!")
            return

        LOGGER.info(
            f"{m.from_user.id} fetched help for '{help_option}' text in {m.chat.id}",
        )

        if m.chat.type == ChatType.PRIVATE:
            if len(help_msg) >= 1026:
                await m.reply_text(
                    help_msg, parse_mode=enums.ParseMode.MARKDOWN, quote=True
                )
            await m.reply_photo(
                photo=str(choice(StartPic)),
                caption=help_msg,
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=help_kb,
                quote=True,
            )
        else:

            await m.reply_photo(
                photo=str(choice(StartPic)),
                caption=f"Press the button below to get help for <i>{help_option}</i>",
                reply_markup=InlineKeyboardMarkup(
                  [
                    [
                      InlineKeyboardButton(
                        "Help",
                        url=f"t.me/{Config.BOT_USERNAME}?start={help_option}",
                        ),
                    ],
                  ],
                ),
            )
    else:

        if m.chat.type == ChatType.PRIVATE:
            msg = f"""
🌸𝗡𝗲𝘇𝘂𝗸𝗼 🌸 
 
☉ 𝗗𝗶𝘀𝗰𝗼𝘃𝗲𝗿 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘂𝘀𝗲 𝗲𝗳𝗳𝗼𝗿𝘁𝗹𝗲𝘀𝘀𝗹𝘆.                 

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /"""
        else:
            keyboard = InlineKeyboardMarkup(
              [
                [
                  InlineKeyboardButton(
                    "Help", 
                    url=f"t.me/{Config.BOT_USERNAME}?start=start_help",
                  ),
                ],
              ],
            )
            msg = "Contact me in PM to get the list of possible commands."

        await m.reply_photo(
            photo=str(choice(StartPic)),
            caption=msg,
            reply_markup = InlineKeyboardMarkup(
                    paginate_modules(0, HELP_COMMANDS, "help")
                ),
        )

    return

@app.on_callback_query(filters.regex("^bot_curr_info$"))
async def give_curr_info(c: app, q: CallbackQuery):
    start = time()
    up = strftime("%Hh %Mm %Ss", gmtime(time() - UPTIME))
    x = await c.send_message(q.message.chat.id, "Pinging..")
    delta_ping = time() - start
    await x.delete()
    txt = f"""
🏓 Pɪɴɢ: {delta_ping * 1000:.3f} ms
📈 Uᴘᴛɪᴍᴇ : {up}
🤖 Bᴏᴛ's ᴠᴇʀsɪᴏɴ: {VERSION}
🐍 Pʏᴛʜᴏɴ's ᴠᴇʀsɪᴏɴ : {PYTHON_VERSION}
🔥 Pʏʀᴏɢʀᴀᴍ's ᴠᴇʀsɪᴏɴ : {PYROGRAM_VERSION}
    """
    await q.answer(txt, show_alert=True)
    return

@app.on_callback_query(filters.regex("^plugins."))
async def get_module_info(c: app, q: CallbackQuery):
    module = q.data.split(".", 1)[1]

    help_msg = HELP_COMMANDS[f"plugins.{module}"]["help_msg"]

    help_kb = HELP_COMMANDS[f"plugins.{module}"]["buttons"]
    try:
      await q.edit_message_caption(
          caption=help_msg,
          parse_mode=enums.ParseMode.MARKDOWN,
          reply_markup=ikb(help_kb, True, todo="commands"),
      )
    except MediaCaptionTooLong:
      await c.send_message(chat_id=q.message.chat.id,text=help_msg,)
    await q.answer()
    return

@app.on_callback_query(filters.regex("^details$"))
async def handle_details_callback(_, query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
     """ʜᴇʟʟᴏ ᴛʜɪs ɪs Kᴏᴍɪ.
     
     Cʟɪᴄᴋ ᴏɴ Dᴏɴᴀᴛᴇ 💸 ᴛᴏ Sᴜᴘᴘᴏʀᴛ Mʏ Tᴇᴀᴍ.
     I'ᴍ Hᴇʀᴇ ᴛᴏ Mᴀɴᴀɢᴇ Yᴏᴜʀ Gʀᴏᴜᴘs ɪɴ ᴀ Hᴏʀɴʏ ᴀɴᴅ Eᴀsʏ Wᴀʏ
     Aɴʏ Issᴜᴇs ᴏʀ Nᴇᴇᴅ Hᴇʟᴘ Rᴇʟᴀᴛᴇᴅ ᴛᴏ Mᴇ Vɪsɪᴛ Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ.""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘", callback_data="how_to_use"),
                ],
                [
                    InlineKeyboardButton("🖥 𝗜𝗡𝗦𝗜𝗗𝗘𝗥", callback_data="bot_curr_info"),
                    InlineKeyboardButton("🤑 𝗗𝗢𝗡𝗔𝗧𝗘", callback_data="donate"),
                ],
                [InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="start_back")],
            ],
        ),
    )

@app.on_callback_query(filters.regex("^how_to_use$"))
async def handle_how_to_use_callback(_, query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
     """Nᴇᴡ ᴛᴏ Kᴏᴍɪ! Hᴇʀᴇ ɪs ᴛʜᴇ Qᴜɪᴄᴋ Sᴛᴀʀᴛ Gᴜɪᴅᴇ
     Wʜɪᴄʜ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ ᴛᴏ Uɴᴅᴇʀsᴛᴀɴᴅ Wʜᴀᴛ ɪs Kᴏᴍɪ 
     ᴀɴᴅ Hᴏᴡ ᴛᴏ Usᴇ Iᴛ.
     Cʟɪᴄᴋ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴ ᴛᴏ Aᴅᴅ Bᴏᴛ ɪɴ Yᴏᴜʀ Gʀᴏᴜᴘ.
     Bᴀsɪᴄ Tᴏᴜʀ Sᴛᴀʀᴛᴇᴅ ᴛᴏ Kɴᴏᴡ Aʙᴏᴜᴛ Hᴏᴡ ᴛᴏ Usᴇ ME
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝗔𝗗𝗗 𝗠𝗘 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣", url="https://t.me/{Config.BOT_USERNAME}?startgroup=new"),
                ],
                [InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="start_back")],
            ],
        ),
    )

@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(_,query):  
    HELP_STRINGS = f"""
🌸𝗡𝗲𝘇𝘂𝗸𝗼 🌸 
 
☉ 𝗗𝗶𝘀𝗰𝗼𝘃𝗲𝗿 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘂𝘀𝗲 𝗲𝗳𝗳𝗼𝗿𝘁𝗹𝗲𝘀𝘀𝗹𝘆.                 

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /

Yᴏᴜ ᴄᴀɴ ᴜsᴇ`$` ᴀɴᴅ `!` ɪɴ ᴘʟᴀᴄᴇᴄ ᴏғ / ᴀs ʏᴏᴜʀ ᴘʀᴇғɪx ʜᴀɴᴅʟᴇʀ"""
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data) 
    try:
        if back_match:
           await query.message.edit_caption(
                HELP_STRINGS,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELP_COMMANDS, "help")
                ),
            )            
        elif mod_match:
            module = mod_match.group(1)
            text = (
                "» **ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ** **{}** :\n".format(
                    module.title()
                )
                + HELP_COMMANDS[f"plugins.{module}"]["help_msg"]
            )
            await query.message.edit_caption(
                text,               
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="𝗕𝗔𝗖𝗞", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_caption(
                HELP_STRINGS,
                reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELP_COMMANDS, "help")
             ),
          )
                                   
        elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_caption(
                HELP_STRINGS,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELP_COMMANDS, "help")
                ),
            )                   

        return await _.answer_callback_query(query.id)

    except errors.BadRequest as e:
        print(e)
        # pass
