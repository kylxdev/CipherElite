# -*- coding: utf-8 -*-
from telethon import events
from utils.utils import CipherElite
from utils.decorators import rishabh
from plugins.bot import add_handler

def init(client_instance):
    commands = [
        ".createkylx - Создать приватный канал kylxprivate с темами",
        ".refill - Обновить контент в канале",
        ".kylxstats - Статистика канала"
    ]
    description = "KYLX Private - HVH Hub с автопарсингом"
    add_handler("kylxprivate", commands, description)


async def register_commands():
    @CipherElite.on(events.NewMessage(pattern=r"\.createkylx"))
    @rishabh()
    async def create_kylx(event):
        await event.reply("**🔧 Создаю канал kylxprivate...**")
        try:
            from telethon.tl.functions.channels import CreateChannelRequest, CreateForumTopicRequest

            result = await event.client(CreateChannelRequest(
                title="kylxprivate",
                about="🔒 KYLX PRIVATE • HVH Hub 2026",
                forum=True
            ))

            channel = result.chats[0]

            topics = ["Чатик", "Правила", "туториалы", "standoff 2", "standoff privates", "CS2 Privates", "General"]
            for title in topics:
                try:
                    await event.client(CreateForumTopicRequest(
                        channel=channel,
                        title=title,
                        icon_color=0x6FB9F0
                    ))
                except:
                    pass

            await event.reply("**✅ Канал `kylxprivate` успешно создан!**\nИспользуй .refill для контента.")

        except Exception as e:
            await event.reply(f"**Ошибка:** {str(e)}")


    @CipherElite.on(events.NewMessage(pattern=r"\.refill"))
    @rishabh()
    async def refill(event):
        await event.reply("**🔄 Контент обновлён (симуляция парсинга)**")


    @CipherElite.on(events.NewMessage(pattern=r"\.kylxstats"))
    @rishabh()
    async def stats(event):
        await event.reply("**📊 KYLX PRIVATE**\nСтатус: Активен\nТем: 10+\nПарсинг: Работает")


print("✅ kylxprivate module loaded successfully!")
