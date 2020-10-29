import urllib
import requests

from .bot_config import BOT_TOKEN, CHANNEL_CHAT_ID
MESSAGE_TEMPLATE = "_Benji was on the move!_\n*{action}* is now at *{count}*!"
URL_TEMPLATE = "https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}"


def update_telegram_channel(action):
    name = action.name
    count = action.get_count()
    message_text = urllib.parse.quote(MESSAGE_TEMPLATE.format(action=name, count=count))
    url = URL_TEMPLATE.format(bot_token=BOT_TOKEN, chat_id=CHANNEL_CHAT_ID, text=message_text)
    requests.get(url)
