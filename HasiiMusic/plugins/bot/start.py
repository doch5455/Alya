import asyncio
import random
import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from config import BANNED_USERS, STICKERS
from strings import get_string
from HasiiMusic import app
from HasiiMusic.misc import _boot_
from HasiiMusic.plugins.sudo.sudoers import sudoers_list
from HasiiMusic.utils import bot_sys_stats
from HasiiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from HasiiMusic.utils.decorators.language import LanguageStart
from HasiiMusic.utils.formatters import get_readable_time
from HasiiMusic.utils.inline import private_panel, start_panel
from HasiiMusic.utils.inline.help import help_keyboard


# ───────────────────────── helpers ─────────────────────────
async def delete_sticker_after_delay(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass

def _rows_from(markup_or_rows):
    if isinstance(markup_or_rows, InlineKeyboardMarkup):
        return markup_or_rows.inline_keyboard
    return markup_or_rows

def safe_markup(markup_or_rows):
    """None/boş satırları ve None butonları temizler."""
    rows = _rows_from(markup_or_rows) or []
    cleaned = []
    for r in rows:
        if not r:
            continue
        rr = [b for b in r if isinstance(b, InlineKeyboardButton)]
        if rr:
            cleaned.append(rr)
    return InlineKeyboardMarkup(cleaned) if cleaned else None
# ───────────────────────────────────────────────────────────


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # /start parametreli
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_keyboard(_)
            await message.reply_text(
                text=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=safe_markup(keyboard),
                disable_web_page_preview=True
            )

        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                         f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                         f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )

        elif name.startswith("inf"):
            m = await message.reply_text("🔎")
            vid_id = str(name).replace("info_", "", 1)
            query_url = f"https://www.youtube.com/watch?v={vid_id}"

            title = duration = views = channellink = channel = link = published = "—"
            try:
                results = VideosSearch(query_url, limit=1)
                payload = await results.next()
                items = payload.get("result") or []
                if items:
                    r0 = items[0]
                    title = r0.get("title") or "—"
                    duration = r0.get("duration") or "—"
                    views = (r0.get("viewCount") or {}).get("short") or "—"
                    ch = r0.get("channel") or {}
                    channellink = ch.get("link") or "—"
                    channel = ch.get("name") or "—"
                    link = r0.get("link") or query_url
                    published = r0.get("publishedTime") or "—"
            except Exception:
                link = query_url  # sessiz düş

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )

            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text=_["S_B_6"], url=link),
                    InlineKeyboardButton(text=_["S_B_4"], url=config.SUPPORT_CHAT),
                ]]
            )
            try:
                await m.delete()
            except Exception:
                pass

            await app.send_message(
                chat_id=message.chat.id,
                text=searched_text,
                reply_markup=safe_markup(key),
                disable_web_page_preview=True
            )

            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} checked <b>track info</b>.\n\n"
                         f"<b>ID:</b> <code>{message.from_user.id}</code>\n"
                         f"<b>Username:</b> @{message.from_user.username}",
                )

    # Parametresiz /start
    else:
        out = private_panel(_)

        # STICKERS boşsa gönderme
        try:
            if STICKERS and isinstance(STICKERS, (list, tuple)):
                sticker_message = await message.reply_sticker(sticker=random.choice(STICKERS))
                asyncio.create_task(delete_sticker_after_delay(sticker_message, 2))
        except Exception:
            pass

        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()

        await message.reply_text(
            text=_["start_2"].format(
                message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats
            ),
            reply_markup=safe_markup(out),
            disable_web_page_preview=True
        )

        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} started the bot.\n\n"
                     f"<b>ID:</b> <code>{message.from_user.id}</code>\n"
                     f"<b>Username:</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    try:
        await message.reply_text(
            text=_["start_1"].format(app.mention, get_readable_time(uptime)),
            reply_markup=safe_markup(out),
            disable_web_page_preview=True
        )
    except Exception:
        pass
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_text(
                    text=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=safe_markup(out),
                    disable_web_page_preview=True
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print("welcome handler error:", ex)