import os
import sys

BROWSERSTACK_AUT_LOG_URL = "https://automate.browserstack.com/logs/"
BROWSERSTACK_AUT_SESSION_LOG_URL = "https://api.browserstack.com/automate/sessions/"

try:
    AUTH = (os.environ["BROWSERSTACK_USERNAME"], os.environ["BROWSERSTACK_KEY"])
except KeyError:
    print("Ensure BROWSERSTACK_USERNAME and BROWSERSTACK_KEY has been set in environment variable.")
    sys.exit(1)

try:
    os.mkdir('uploads')
    os.mkdir('downloads')
except FileExistsError:
    pass


try:
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
    DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
except Exception:
    pass


def rm_txt_from_downloads():
    txt_files = os.listdir(DOWNLOAD_FOLDER)
    for txt_file in txt_files:
        if txt_file.endswith(".txt"):
            os.remove(os.path.join(DOWNLOAD_FOLDER, txt_file))


def rm_json_from_downloads():
    json_files = os.listdir(DOWNLOAD_FOLDER)
    for json_file in json_files:
        if json_file.endswith(".json"):
            os.remove(os.path.join(DOWNLOAD_FOLDER, json_file))
