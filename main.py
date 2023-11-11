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
    update.message.reply_text("Hello I'm a bot...")

def help(update, context):
    update.message.reply_text("list of command")

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






def main():

    updater = Updater(os.getenv('BOT_ATERNOS_TOKEN'), use_context=True)

    dp = updater.dispatcher

    # Base Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("add", add))


    # Run bot
    updater.start_polling()

    # Stop bot with CTRL+C
    updater.idle()

if __name__ == '__main__':
    main()
