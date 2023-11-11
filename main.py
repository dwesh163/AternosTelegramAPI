from getpass import getpass
from python_aternos import Client, atserver
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
import re
import json

load_dotenv()

if not os.path.isfile("data.json"):
    atclient = Client()
    aternos = atclient.account
    atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))
    srvs = aternos.list_servers()

    data = {}

    for srv in srvs:
        data[srv.servid] = [os.getenv('ADMIN_TELEGRAM_ID')]

    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)


def start(update, context):
    update.message.reply_text("Hello! I'm a bot designed to assist with Aternos servers.\n\n"
                              "- If you need help, you can use the /help command for a list of available commands.\n\n"
                              "- If you are a guest, please ask the administrator to give you access.\n\n"
                              "- If you wish to manage your own server, please see https://github.com/dwesh163/AternosTelegramAPI\n")

def help(update, context):
    update.message.reply_text("Available commands:\n"
                              "/open : Start the Aternos server\n"
                              "/start : Start the bot\n"
                              "/help : Display the list of available commands\n"
                              "/info : Get information about your Aternos server\n"
                              "/add <server_id> <telegram_user_id> : Add a user as an admin for a server\n"
                              )

def info(update, context):

    atclient = Client()
    aternos = atclient.account
    atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))
    srvs = aternos.list_servers()

    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    for srv in srvs:
        if(str(update.message.from_user["id"]) in data[srv.servid]):

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

def getAllServeur():
    atclient = Client()
    aternos = atclient.account
    atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))
    srvs = aternos.list_servers()

    response = ""

    for srv in srvs:
        srv.fetch()
        response += f'{srv.domain} -- {srv.servid}\n'
    
    return response

def add(update, context):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    if(len(context.args) == 2):
        if(context.args[0] in data):
            data[context.args[0]].append(context.args[1])
            with open("data.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=2)
            update.message.reply_text("goof")
        else:
            update.message.reply_text(getAllServeur())
    else:
        update.message.reply_text(getAllServeur())

def startServeur(update, context):
    atclient = Client()
    aternos = atclient.account
    atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))
    srvs = aternos.list_servers()

    for srv in srvs:
        srv.fetch()
        try:
            srv.start()
            update.message.reply_text(f'{srv.subdomain} is starting up')
        except:
            update.message.reply_text(f'The {srv.subdomain} server is opening')


def main():

    updater = Updater(os.getenv('BOT_ATERNOS_TOKEN'), use_context=True)

    dp = updater.dispatcher

    # Base Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("open", startServeur))

    # Run bot
    updater.start_polling()

    # Stop bot with CTRL+C
    updater.idle()

if __name__ == '__main__':
    main()
