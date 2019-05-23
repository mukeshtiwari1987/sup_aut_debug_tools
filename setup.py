import os
import sys

BROWSERSTACK_AUT_LOG_URL = "https://automate.browserstack.com/logs/"

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
