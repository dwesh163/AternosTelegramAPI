from getpass import getpass
from python_aternos import Client, atserver
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os

atclient = Client()
aternos = atclient.account
atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))
srvs = aternos.list_servers()

load_dotenv()
TOKEN =  os.getenv('BOT_ATERNOS_TOKEN')

def start(update, context):
    update.message.reply_text("Hello I'm a bot...")

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Base Command
    dp.add_handler(CommandHandler("start", start))

    # Run bot
    updater.start_polling()

    # Stop bot with CTRL+C
    updater.idle()

if __name__ == '__main__':
    main()
