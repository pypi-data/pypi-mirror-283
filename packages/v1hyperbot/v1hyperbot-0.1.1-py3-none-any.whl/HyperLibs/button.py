import re

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Button:
    def url(text):
        link_pattern = r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:[/?]\S+)?|tg://\S+$"
        return re.findall(link_pattern, text)

    def text(text):
        button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
        text_matches = re.split(r"\| [^|]+ - [^|]+ \|", text)[0].strip() if "|" in text else text.strip()
        return button_matches, text_matches

    def create(text, is_id=False):
        keyboard = []
        button_matches, text_matches = Button.text(text)

        for button_text, button_data in button_matches:
            data_parts = button_data.split(";")
            cb_data = data_parts[0]

            if not Button.url(cb_data):
                cb_data = f"_gtnote {is_id}_{cb_data}" if is_id else cb_data

            button = (
                InlineKeyboardButton(button_text, user_id=cb_data)
                if "user" in data_parts
                else (
                    InlineKeyboardButton(button_text, url=cb_data)
                    if Button.url(cb_data)
                    else InlineKeyboardButton(button_text, callback_data=cb_data)
                )
            )

            if "same" in data_parts and keyboard:
                keyboard[-1].append(button)
            else:
                keyboard.append([button])

        return InlineKeyboardMarkup(keyboard), text_matches

    def ikb(btn):
        button, text = Button.create(btn)
        return button
