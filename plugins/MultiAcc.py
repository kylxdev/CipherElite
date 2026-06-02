from telethon import TelegramClient
from telethon.sessions import StringSession
from CipherElite.utils import admin_cmd, edit_or_reply
import asyncio
import os

# ==================== MULTI ACCOUNT CONTROL PRO ====================

# Глобальный словарь для дополнительных аккаунтов
extra_clients = {}
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Автозагрузка аккаунтов при старте (из переменных)
async def load_saved_accounts():
    global extra_clients
    for i in range(1, 6):  # Поддержка до 5 аккаунтов
        session_var = f"MULTI_SESSION_{i}"
        name_var = f"MULTI_NAME_{i}"
        
        session = os.getenv(session_var)
        name = os.getenv(name_var) or f"Account{i}"
        
        if session and session.startswith("1"):
            try:
                client = TelegramClient(StringSession(session), API_ID, API_HASH)
                await client.connect()
                if await client.is_user_authorized():
                    me = await client.get_me()
                    extra_clients[name] = client
                    print(f"✅ Загружен аккаунт: {name} ({me.first_name})")
            except:
                print(f"❌ Не удалось загрузить {name}")

# Запускаем загрузку при импорте плагина
asyncio.create_task(load_saved_accounts())


@admin_cmd(pattern="^.addaccount(?:\s|$)([\s\S]*)")
async def add_account(event):
    """Добавить новый аккаунт"""
    if len(extra_clients) >= 5:
        await edit_or_reply(event, "❌ Максимум 5 дополнительных аккаунтов!")
        return

    reply = await event.get_reply_message()
    if not reply or not reply.text or not reply.text.strip().startswith("1"):
        await edit_or_reply(event, "❌ Ответь на сообщение содержащее **String Session** (начинается с 1)")
        return

    session_string = reply.text.strip()
    name = event.pattern_match.group(1).strip() or f"Account{len(extra_clients)+1}"

    try:
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.connect()
        me = await client.get_me()

        extra_clients[name] = client

        await edit_or_reply(event, f"""
✅ **Аккаунт успешно добавлен!**

**Название:** `{name}`
**Имя:** {me.first_name} {me.last_name or ''}
**Username:** @{me.username if me.username else 'Нет'}
**Всего аккаунтов:** {len(extra_clients) + 1}
        """)
    except Exception as e:
        await edit_or_reply(event, f"❌ Ошибка:\n`{str(e)[:500]}`")


@admin_cmd(pattern="^.accounts$")
async def list_accounts(event):
    """Список всех аккаунтов"""
    if not extra_clients:
        await edit_or_reply(event, "📭 Дополнительных аккаунтов нет.\nИспользуй `.addaccount`")
        return

    text = "**📋 Подключённые аккаунты:**\n\n"
    for name, client in extra_clients.items():
        try:
            me = await client.get_me()
            status = "🟢 Онлайн" if await client.is_user_authorized() else "🔴 Оффлайн"
            text += f"{status} | **{name}** → {me.first_name} (@{me.username or 'нет'})\n"
        except:
            text += f"⚠️ **{name}** → Ошибка подключения\n"
    
    text += f"\n**Всего:** {len(extra_clients)} аккаунтов"
    await edit_or_reply(event, text)


@admin_cmd(pattern="^.sendas(?:\s|$)([\s\S]*)")
async def send_as(event):
    """Отправить сообщение от имени другого аккаунта"""
    args = event.pattern_match.group(1).strip().split(maxsplit=1)
    if len(args) < 2:
        await edit_or_reply(event, "❌ Использование:\n`.sendas имя_аккаунта текст`")
        return

    acc_name = args[0]
    message_text = args[1]

    if acc_name not in extra_clients:
        await edit_or_reply(event, f"❌ Аккаунт `{acc_name}` не найден!\nИспользуй `.accounts`")
        return

    client = extra_clients[acc_name]
    reply = await event.get_reply_message()

    try:
        if reply:
            await client.send_message(event.chat_id, message_text, reply_to=reply.id)
        else:
            await client.send_message(event.chat_id, message_text)
        
        await edit_or_reply(event, f"✅ Отправлено от **{acc_name}**")
    except Exception as e:
        await edit_or_reply(event, f"❌ Ошибка отправки:\n`{str(e)[:400]}`")


@admin_cmd(pattern="^.removeaccount(?:\s|$)([\s\S]*)")
async def remove_account(event):
    """Удалить аккаунт"""
    name = event.pattern_match.group(1).strip()
    if name in extra_clients:
        try:
            await extra_clients[name].disconnect()
        except:
            pass
        del extra_clients[name]
        await edit_or_reply(event, f"✅ Аккаунт `{name}` удалён.")
    else:
        await edit_or_reply(event, "❌ Аккаунт не найден.")


@admin_cmd(pattern="^.multihelp$")
async def multi_help(event):
    await edit_or_reply(event, """
**🔰 MultiAccountControl Pro**

`.addaccount <имя>` — добавить аккаунт (ответь на StringSession)
`.accounts` — список всех аккаунтов
`.sendas <имя> <текст>` — отправить сообщение от аккаунта
`.removeaccount <имя>` — удалить аккаунт
`.multihelp` — эта помощь

**Пример:**
`.sendas work Привет, я на работе`

**Совет:** Чтобы аккаунты сохранялись после рестарта — используй переменные `MULTI_SESSION_1`, `MULTI_NAME_1` и т.д. в Variable Manager.
    """)
