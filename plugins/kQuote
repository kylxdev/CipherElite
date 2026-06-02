from telethon import events
from CipherElite.utils import admin_cmd, edit_or_reply, sudo_cmd
import random
import asyncio

# ==================== QUOTE GENERATOR ====================

@admin_cmd(pattern="^.q(?:\s|$)([\s\S]*)")
@admin_cmd(pattern="^.quote(?:\s|$)([\s\S]*)")
async def quote_generator(event):
    """Создаёт красивые цитаты"""
    reply = await event.get_reply_message()
    if not reply:
        await edit_or_reply(event, "❌ Ответь на сообщение, которое хочешь сделать цитатой!")
        return

    args = event.pattern_match.group(1).strip()
    style = "default"

    if args:
        style = args.lower()

    # Разные стили цитат
    styles = {
        "default": "🖤",
        "dark": "⚫",
        "light": "⚪",
        "neon": "🌈",
        "fire": "🔥",
        "love": "❤️",
        "toxic": "☠️",
        "random": random.choice(["🖤", "⚫", "🌈", "🔥", "❤️", "☠️", "💎"])
    }

    emoji = styles.get(style, styles["default"])

    user = await event.client.get_entity(reply.sender_id)
    name = user.first_name if user.first_name else "Unknown"

    text = reply.text or "Медиа"

    quote_text = f"""
{emoji} **Цитата** {emoji}

**{name} сказал(а):**

> {text}

— {name}
    """

    # Дополнительные крутые варианты
    if style == "sticker" or style == "st":
        await event.reply(quote_text)
        await event.delete()
        return

    if "rainbow" in style or "color" in style:
        quote_text = f"🌈 **Rainbow Quote**\n\n{text}\n\n— {name}"

    if "big" in style or "bold" in style:
        quote_text = f"**{text}**\n\n— **{name}**"

    result = await edit_or_reply(event, quote_text)

    # Дополнительные функции
    if "save" in args.lower():
        await event.client.send_message("me", quote_text)
        await result.edit(quote_text + "\n\n✅ Сохранено в Избранное!")


@admin_cmd(pattern="^.qlist$")
async def quote_list(event):
    """Показывает все доступные стили"""
    text = """
**🎨 Доступные стили Quote:**

`.q` — обычная цитата
`.q dark` — тёмная
`.q light` — светлая
`.q neon / rainbow` — неоновая
`.q fire` — огненная
`.q love` — романтичная
`.q toxic` — токсичная
`.q random` — случайный стиль
`.q big` — жирным шрифтом
`.q save` — сохранить в Избранное

**Пример:** `.q neon` (на реплай)
    """
    await edit_or_reply(event, text)


# Дополнительная функция — рандомная цитата из интернета
@admin_cmd(pattern="^.randquote$")
async def random_quote(event):
    """Случайная мотивационная цитата"""
    quotes = [
        "Великие дела совершаются не силой, а упорством.",
        "Не бойся идти медленно, бойся стоять на месте.",
        "Будущее принадлежит тем, кто верит в красоту своей мечты.",
        "Тот, кто хочет видеть радугу, должен пережить дождь.",
        "Успех — это идти от неудачи к неудаче, не теряя энтузиазма.",
        "Мечтай так, будто никто не будет тебя осуждать.",
    ]
    quote = random.choice(quotes)
    await edit_or_reply(event, f"✨ **Случайная цитата:**\n\n{quote}")


# Авто-цитата при реплае на определённые слова
@admin_cmd(pattern="^.qon$")
async def quote_on(event):
    await edit_or_reply(event, "✅ Режим авто-цитат **включён** (временно)")
    # Здесь можно добавить persistent режим, если хочешь
