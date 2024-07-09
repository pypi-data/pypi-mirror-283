from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot.util import quick_markup


def send_telegram_bot_message(
    bot: TeleBot,
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> dict:
    """Send a message to a specified telegram bot chat.

    Args:
        bot (TeleBot): _description_
        chat_id (int): _description_
        text (str): _description_
        reply_markup (InlineKeyboardMarkup | None, optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    return bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
    )


def get_inline_keyboard_markup(
    keyboard_labels: list[str],
    callback_values: list[str],
    row_width: int = 1,
) -> InlineKeyboardMarkup:
    """Get a markup for a telegram message inline keyboard.

    Args:
        keyboard_labels (list[str]): _description_
        callback_values (list[str]): _description_
        row_width (int): _description_. Defaults to 1.

    Returns:
        InlineKeyboardMarkup: _description_
    """
    data_options = [{"callback_data": callback_value} for callback_value in callback_values]
    markup_values = dict(zip(keyboard_labels, data_options))
    return quick_markup(values=markup_values, row_width=row_width)
