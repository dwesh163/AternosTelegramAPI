from getpass import getpass
from python_aternos import Client, atserver
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
import re

load_dotenv()
TOKEN =  os.getenv('BOT_ATERNOS_TOKEN')

def start(update, context):
    update.message.reply_text("Hello I'm a bot...")

def help(update, context):
    update.message.reply_text("list of command")

def info(update, context):

    atclient = Client()
    aternos = atclient.account
    atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))
    srvs = aternos.list_servers()

    for srv in srvs:
        srv.fetch()
        response  = f'*** {srv.subdomain} ***\n'
        response += re.sub(r'§\d', '', srv.motd)
        response += "\n"
        response += f'*** Status: {srv.status}\n'
        response += f'*** address: {srv.domain}\n'
        response += f'*** Port: {srv.port}\n'
        response += f'*** Minecraft: {srv.software} {srv.version}\n'
        response += f'*** Version: {srv.edition}\n'
        response += f'*** Id: {srv.servid}\n'
        response += f'*** Full address: {srv.address}\n'
    
        update.message.reply_text(response)

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Base Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("info", info))


    # Run bot
    updater.start_polling()

    # Stop bot with CTRL+C
    updater.idle()

if __name__ == '__main__':
    main()
