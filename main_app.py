import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests
from setup import UPLOAD_FOLDER, DOWNLOAD_FOLDER, remove_and_create_download_folder
from command_parser import command_parser_main
from vid_parser import vid_parser_main
from console_parser import console_parser_main
from networklog_parser import network_parser_main
from seleniumlog_parser import selenium_parser_main
from appiumlog_parser import appium_parser_main

app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size up to 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
username = None
password = None
ALLOWED_EXTENSIONS = {'json', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        global username
        global password
        username = request.form['username']
        password = request.form['password']
        with requests.get('https://api.browserstack.com/automate/plan.json',
                          auth=(username, password),
                          timeout=(5, 5)) as check:
            if check.headers['Status'] == '200 OK':
                return redirect(url_for('aut_ss'))
            else:
                error = "Unauthorized to proceed."
    return render_template("login.html", error=error)


@app.route('/autss')
def aut_ss():
    return render_template('upload_autss.html')


@app.route('/slowsessionaut', methods=['POST'])
def aut_ss_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results = command_parser_main(filename)
            remove_and_create_download_folder()
            return render_template("autssresult.html", output_list=results)
    return render_template('upload_autss.html')


@app.route('/autvid')
def aut_vid():
    return render_template('upload_autvid.html')


@app.route('/vidstatusaut', methods=['POST'])
def aut_vid_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results = vid_parser_main(filename)
            remove_and_create_download_folder()
            return render_template("autvidresult.html", output_list=results)
    return render_template('upload_autvid.html')


@app.route('/autconsole')
def aut_console():
    return render_template('upload_autconsole.html')


@app.route('/consolestatusaut', methods=['POST'])
def aut_console_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            search_text = request.form['search_text']
            results = console_parser_main(filename, search_text)
            remove_and_create_download_folder()
            return render_template("autconsoleresult.html", output_list=results)
    return render_template('upload_autvid.html')


@app.route('/autnetwork')
def aut_network():
    return render_template('upload_autnetwork.html')


@app.route('/networkstatusaut', methods=['POST'])
def aut_network_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            search_text = request.form['search_text']
            results = network_parser_main(filename, search_text)
            remove_and_create_download_folder()
            return render_template("autnetworkresult.html", output_list=results)
    return render_template('upload_autnetwork.html')


@app.route('/autselenium')
def aut_selenium():
    return render_template('upload_autselenium.html')


@app.route('/seleniumstatusaut', methods=['POST'])
def aut_selenium_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            search_text = request.form['search_text']
            results = selenium_parser_main(filename, search_text)
            remove_and_create_download_folder()
            return render_template("autseleniumresult.html", output_list=results)
    return render_template('upload_autselenium.html')


@app.route('/autappium')
def aut_appium():
    return render_template('upload_autappium.html')


@app.route('/appiumstatusaut', methods=['POST'])
def aut_appium_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            search_text = request.form['search_text']
            results = appium_parser_main(filename, search_text)
            remove_and_create_download_folder()
            return render_template("autappiumresult.html", output_list=results)
    return render_template('upload_autappium.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
