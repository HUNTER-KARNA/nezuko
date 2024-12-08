from pyrogram import Client, filters
from pyrogram.types import Message

from Curse.bot_class import app
from Curse.database.sangmata_db import *
from Curse.extras.localization import use_chat_lang
from Curse.utils.custom_filters import admin_filter
from Curse.vars import Config


# Check user that change first_name, last_name, and username
@app.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=5,
)
@use_chat_lang()
async def cek_mataa(self: Client, ctx: Message, strings):
    if ctx.sender_chat or not await is_sangmata_on(ctx.chat.id):
        return
    if not await cek_userdata(ctx.from_user.id):
        return await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(ctx.from_user.id)
    msg = ""
    if (
        usernamebefore != ctx.from_user.username
        or first_name != ctx.from_user.first_name
        or lastname_before != ctx.from_user.last_name
    ):
        msg += f"<b>➼ 𝐊𝐎𝐌𝐈 𝐌𝐄𝐓𝐀</b>\n\n🧑‍💼 User: {ctx.from_user.mention} [<code>{ctx.from_user.id}</code>]\n"
    if usernamebefore != ctx.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else strings("no_uname")
        usernameafter = (
            f"@{ctx.from_user.username}"
            if ctx.from_user.username
            else strings("no_uname")
        )
        msg += strings("uname_change_msg").format(bef=usernamebefore, aft=usernameafter)
        await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    if first_name != ctx.from_user.first_name:
        msg += strings("firstname_change_msg").format(
            bef=first_name, aft=ctx.from_user.first_name
        )
        await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    if lastname_before != ctx.from_user.last_name:
        lastname_before = lastname_before or strings("no_last_name")
        lastname_after = ctx.from_user.last_name or strings("no_last_name")
        msg += strings("lastname_change_msg").format(
            bef=lastname_before, aft=lastname_after
        )
        await add_userdata(
            ctx.from_user.id,
            ctx.from_user.username,
            ctx.from_user.first_name,
            ctx.from_user.last_name,
        )
    if msg != "":
        await ctx.reply(msg, quote=True)


@app.on_message(
    filters.group
    & filters.command("imposter", Config.PREFIX_HANDLER)
    & ~filters.bot
    & ~filters.via_bot
    & admin_filter, group=100101
)
@use_chat_lang()
async def set_mataa(self: Client, ctx: Message, strings):
    if len(ctx.command) == 1:
        return await ctx.reply(strings("set_sangmata_help").format(cmd=ctx.command[0]))
    if ctx.command[1] == "on":
        cekset = await is_sangmata_on(ctx.chat.id)
        if cekset:
            await ctx.reply(strings("sangmata_already_on"))
        else:
            await sangmata_on(ctx.chat.id)
            await ctx.reply(strings("sangmata_enabled"))
    elif ctx.command[1] == "off":
        cekset = await is_sangmata_on(ctx.chat.id)
        if not cekset:
            await ctx.reply(strings("sangmata_already_off"))
        else:
            await sangmata_off(ctx.chat.id)
            await ctx.reply(strings("sangmata_disabled"))
    else:
        await ctx.reply(strings("wrong_param"))

__PLUGIN__ = "𝗜𝗠𝗣𝗢𝗦𝗧𝗘𝗥"
__HELP__ = """
*• /imposter on:* Use this command to track name and username changes in the group. If a user changes their name and username, the bot will send a message showing any related changes.
"""
