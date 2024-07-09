import telebot

from django.conf import settings


def send_alert(text):
    bot = telebot.TeleBot(settings.BOT_TOKEN)
    bot.send_message(settings.CHANNEL_ID, text=f"<code> {text[:1000]} </code>", parse_mode='html')


def alert_to_telegram(traceback, message):
    if not isinstance(message, list):
        message = message
    text = f'❌{settings.PROEJECT_NAME if hasattr(settings, "PROJECT_NAME") else "Project"} Exception❌\n\n' \
           f'<strong>✍️ Message: 🔴{message}🔴</strong>' \
           f'\n\n🔖 TraceBack: {traceback}'
    if hasattr(settings, "BOT_TOKEN") and hasattr(settings, "CHANNEL_ID"):
        send_alert(text)
