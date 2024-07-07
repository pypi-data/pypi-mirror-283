import yaml

from HyperLibs import bot


class Language:
    def data(user):
        db_lang = bot.db.get(user.id, "LANGUAGE")
        with open(f"string/{db_lang if db_lang else 'id'}.yml", "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                bot.logs("lang_data").error(exc)
                return None
