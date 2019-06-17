import os
import sys
import shutil

BROWSERSTACK_AUT_LOG_URL = "https://automate.browserstack.com/logs/"
BROWSERSTACK_AUT_SESSION_LOG_URL = "https://api.browserstack.com/automate/sessions/"

try:
    AUTH = (os.environ["BROWSERSTACK_USERNAME"], os.environ["BROWSERSTACK_KEY"])
except KeyError:
    print("Ensure BROWSERSTACK_USERNAME and BROWSERSTACK_KEY has been set in environment variable.\n")
    print("Command to set environment variable.\n")
    print("export BROWSERSTACK_USERNAME='your_browserstack_username'.\n")
    print("export BROWSERSTACK_KEY='your_browserstack_key'.\n")
    print("source ~/.bash_profile")
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


def remove_and_create_download_folder():
    shutil.rmtree(DOWNLOAD_FOLDER)
    os.mkdir('downloads')
