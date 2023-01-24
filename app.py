from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import requests
import os
import uuid


app = Flask(__name__)
app.config.from_json("config.json")


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name = name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


@app.route('/txt2speech', methods=['GET', 'POST'])
def txt_to_speech():
    print('Request for txt2speech, method = ' + request.method)
    if request.method == 'GET':
        return get_txt_to_speech(request.args.get('id'))
    elif request.method == 'POST':
        return create_txt_to_speech_task()


def get_txt_to_speech(id):
    print('GET mp3 file, id = {0}'.format(id))
    return send_from_directory(os.path.join(app.root_path, "resource"), "{0}.mp3".format(id), as_attachment=True)


def create_txt_to_speech_task():
    id = str(uuid.uuid1())
    print("start downloading, id = {0}".format(id))
    r = requests.post(
        url="https://{0}.tts.speech.microsoft.com/cognitiveservices/v1".format(app.config.get("SPEECH_REGION")),
        headers={
            "Ocp-Apim-Subscription-Key": app.config.get("SPEECH_KEY"),
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": 'python',
        },
        data=format_txt_to_speech_request())
    print("end downloading, id = {0}, status = {1}".format(id, r.status_code))
    if r.status_code != 200:
        return {"errno": r.status_code, "errmsg": r.content}
    print("start saving, id = {0}".format(id))
    with open(os.path.join(app.root_path, "resource", "{0}.mp3".format(id)), 'w') as f:
        f.write(r.content)
    return {"errno": 0, "id" : id}


def format_txt_to_speech_request():
    rate = request.json.get('rate')
    pitch = request.json.get('pitch')
    text = request.json.get('text').encode('utf-8')
    return '''<speak version="1.0"
        <voice xml:lang="zh-CN" xml:gender="Female" name="zh-CN-XiaochenNeural">
            <prosody rate="{0}" pitch="{1}">
                {2}
            </prosody>
        </voice>
    </speak>'''.format(rate, pitch, text)


if __name__ == '__main__':
    app.run()
