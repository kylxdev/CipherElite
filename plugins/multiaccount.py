from telethon import TelegramClient
from telethon.sessions import StringSession
from CipherElite.utils import admin_cmd, edit_or_reply
import asyncio
import os

# ==================== MULTI ACCOUNT CONTROL PRO ====================

extra_clients = {}
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


async def load_saved_accounts():
    global extra_clients
    for i in range(1, 6):
        session_var = f"MULTI_SESSION_{i}"
        name_var = f"MULTI_NAME_{i}"
        
        session = os.getenv(session_var)
        name = os.getenv(name_var) or f"Account{i}"
        
        if session and str(session).startswith("1"):
            try:
                client = TelegramClient(StringSession(session), API_ID, API_HASH)
                await client.connect()
                if await client.is_user_authorized():
                    me = await client.get_me()
                    extra_clients[name] = client
                    print(f"✅ MultiAccount: Загружен {name} ({me.first_name})")
            except Exception as e:
                print(f"❌ MultiAccount: Ошибка загрузки {name} - {e}")


# Автозагрузка при старте плагина
asyncio.create_task(load_saved_accounts())


@admin_cmd(pattern="^.addaccount(?:\s|$)([\s\S]*)")
async def add_account(event):
    if len(extra_clients) >= 5:
        return await edit_or_reply(event, "❌ Максимум 5 аккаунтов!")

    reply = await event.get_reply_message()
    if not reply or not reply.text or not str(reply.text).strip().startswith("1"):
        return await edit_or_reply(event, "❌ Ответь на сообщение с **String Session**")

    session_string = reply.text.strip()
    name = event.pattern_match.group(1).strip() or f"Account{len(extra_clients)+1}"

    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.connect()
        me = await client.get_me()
        extra_clients[name] = client

        await edit_or_reply(event, f"""
✅ **Аккаунт добавлен успешно!**

**Название:** `{name}`
**Имя:** {me.first_name}
**Username:** @{me.username or 'нет'}
**Всего аккаунтов:** {len(extra_clients)}
        """)
    except Exception as e:
        await edit_or_reply(event, f"❌ Ошибка:\n`{str(e)[:500]}`")


@admin_cmd(pattern="^.accounts$")
async def list_accounts(event):
    if not extra_clients:
        return await edit_or_reply(event, "📭 Нет добавленных аккаунтов.")

    text = "**📋 Multi Accounts:**\n\n"
    for name, client in extra_clients.items():
        try:
            me = await client.get_me()
            status = "🟢" if await client.is_user_authorized() else "🔴"
            text += f"{status} **{name}** → {me.first_name} (@{me.username or 'нет'})\n"
        except:
            text += f"⚠️ **{name}** → Ошибка\n"
    await edit_or_reply(event, text + f"\n**Всего:** {len(extra_clients)}")


@admin_cmd(pattern="^.sendas(?:\s|$)([\s\S]*)")
async def send_as(event):
    args = event.pattern_match.group(1).strip().split(maxsplit=1)
    if len(args) < 2:
        return await edit_or_reply(event, "`.sendas имя текст`")

    name, text = args[0], args[1]
    if name not in extra_clients:
        return await edit_or_reply(event, f"❌ Аккаунт `{name}` не найден.")

    client = extra_clients[name]
    reply = await event.get_reply_message()
    try:
        await client.send_message(event.chat_id, text, reply_to=reply.id if reply else None)
        await edit_or_reply(event, f"✅ Отправлено от **{name}**")
    except Exception as e:
        await edit_or_reply(event, f"❌ Ошибка: {str(e)}")


@admin_cmd(pattern="^.multihelp$")
async def multi_help(event):
    await edit_or_reply(event, """
**🔰 MultiAccount Pro**

`.addaccount <имя>` — добавить (ответь на StringSession)
`.accounts` — список аккаунтов
`.sendas <имя> <текст>` — отправить от аккаунта
`.removeaccount <имя>` — удалить
`.multihelp` — помощь

**Пример:** `.sendas work Я на втором аккаунте`
    """)


# Команда удаления (добавил)
@admin_cmd(pattern="^.removeaccount(?:\s|$)([\s\S]*)")
async def remove_account(event):
    name = event.pattern_match.group(1).strip()
    if name in extra_clients:
        try:
            await extra_clients[name].disconnect()
        except:
            pass
        del extra_clients[name]
        await edit_or_reply(event, f"✅ `{name}` удалён.")
    else:
        await edit_or_reply(event, "❌ Аккаунт не найден.")
