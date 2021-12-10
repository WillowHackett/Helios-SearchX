import logging
import os
import time
import telegram.ext as tg
import requests
from dotenv import load_dotenv

from telegraph import Telegraph

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

load_dotenv('config.env')

def getConfig(name: str):
    return os.environ[name]

LOGGER = logging.getLogger(__name__)

try:
    if bool(getConfig('_____REMOVE_THIS_LINE_____')):
        logging.error('The README.md file there to be read! Exiting now!')
        exit()
except KeyError:
    pass

BOT_TOKEN = None

AUTHORIZED_CHATS = set()
if os.path.exists('authorized_chats.txt'):
    with open('authorized_chats.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            AUTHORIZED_CHATS.add(int(line.split()[0]))
try:
    achats = getConfig('AUTHORIZED_CHATS')
    achats = achats.split(" ")
    for chats in achats:
        AUTHORIZED_CHATS.add(int(chats))
except:
    pass

try:
    VIEW_LINK = getConfig('VIEW_LINK')
    VIEW_LINK = VIEW_LINK.lower() == 'true'
except KeyError:
    VIEW_LINK = False

try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    OWNER_ID = int(getConfig('OWNER_ID'))
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)
try:
    TOKEN_PICKLE_URL = getConfig('TOKEN_PICKLE_URL')
    if len(TOKEN_PICKLE_URL) == 0:
        TOKEN_PICKLE_URL = None
    else:
        res = requests.get(TOKEN_PICKLE_URL)
        if res.status_code == 200:
            with open('token.pickle', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
            logging.error(f"Failed to download token.pickle {res.status_code}")
            raise KeyError
except KeyError:
    pass
DRIVES_NAMES = []
DRIVES_IDS = []
INDEX_URLS = []

if os.path.exists('drive_folder'):
    with open('drive_folder', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            try:
                temp = line.strip().split()
                DRIVES_IDS.append(temp[1])
                DRIVES_NAMES.append(temp[0].replace("_", " "))
            except:
                pass
            try:
                INDEX_URLS.append(temp[2])
            except IndexError as e:
                INDEX_URLS.append(None)

updater = tg.Updater(token=BOT_TOKEN,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
