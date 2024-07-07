taxt_running = """
###################################
# 📚 Library On: @V1HyperBot 📚   #
# 📝 Author    :   @NorSodikin 📝 #
# 💡 Channel   : @FakeCodeX 💡    #
###################################
"""
print(taxt_running)


from glob import glob
from os.path import basename, dirname, isfile

from pyrogram.handlers import CallbackQueryHandler, MessageHandler

from HyperLibs.base import BaseUbot
from HyperLibs.config import Config


def LoadLibs():
    mod_paths = glob(f"{dirname(__file__)}/*.py")
    return sorted([basename(f)[:-3] for f in mod_paths if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")])


for module_name in LoadLibs():
    import_statement = f"from HyperLibs.{module_name} import *"
    exec(import_statement)


class Bot(BaseUbot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        self.logs("ROBOT").info(f"({self.get_mention(self.me, True)}) - 𝐒𝐓𝐀𝐑𝐓𝐄𝐃")


bot = Bot(name="bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
