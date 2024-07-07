import asyncio
import logging

from pyrogram import Client

from HyperLibs import (HYPER, Button, Chat, Database, Download, EmojiPrem, Function, Language, Page, RapidApi, Translate, User,
                       Userbot)


class BaseUbot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = RapidApi
        self.chat = Chat()
        self.client = Userbot
        self.db = Database
        self.dl = Download
        self.emoji = EmojiPrem
        self.func = Function
        self.get = HYPER
        self.get_my_id = {}
        self.get_my_peer = {}
        self.help = {}
        self.lang = Language
        self.line = Button
        self.list_ubot = []
        self.page = Page
        self.prefix = {}
        self.trans = Translate()
        self.user = User

    def logs(name):
        return logging.getLogger(name)

    def get_mention(self, me, logs=False, no_tag=False):
        name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
        link = f"tg://user?id={me.id}"
        return f"{me.id}|{name}" if logs else name if no_tag else f"<a href={link}>{name}</a>"

    def set_prefix(self, user, prefix):
        self.prefix[user.id] = prefix

    def get_prefix(self, user):
        return self.prefix.get(user.id, [".", ",", ":", ";", "!"])

    def copy_to(self, chat_id, value):
        return value.copy(chat_id)

    def reply_to(self, message, value, query=None):
        try:
            reply_methods = {
                "bot": message.reply_inline_bot_result,
                "video": message.reply_video,
                "photo": message.reply_photo,
                "document": message.reply_document,
                "animation": message.reply_animation,
            }
            if query:
                asyncio.create_task(query.delete())

            reply_method = next((method for key, method in reply_methods.items() if key in value), message.reply)

            if "bot" in value:
                x = asyncio.create_task(message._client.get_inline_bot_results(**value))
                return reply_method(x.query_id, x.results[0].id)
            else:
                return reply_method(**value)

        except Exception as e:
            self.logs("reply_to").error(f"An error occurred: {e}")
            return None
