from getpass import getpass
from python_aternos import Client, atserver
from dotenv import load_dotenv
import os

atclient = Client()
aternos = atclient.account
atclient.login_with_session(os.getenv("ATERNOS_SESSION_COOKIE"))