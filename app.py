from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import azure.cognitiveservices.speech as speechsdk
import os
import uuid


app = Flask(__name__)
app.config.from_json("config.json")


# speech_config = speechsdk.SpeechConfig(subscription=app.config.get("SPEECH_KEY"), region=app.config.get("SPEECH_REGION"))
# audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
# speech_config.speech_synthesis_voice_name = 'zh-CN-XiaochenNeural'
# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)



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
    print('GET audio file, id = {0}'.format(id))
    return send_from_directory(os.path.join(app.root_path, "resource"), "{0}.wav".format(id), as_attachment=True)


def create_txt_to_speech_task():
    id = str(uuid.uuid1())
    print("start trans, id = {0}".format(id))
    # result = speech_synthesizer.speak_text_async(text).get()
    # if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     if result.reason == speechsdk.ResultReason.Canceled:
    #         detail = result.cancellation_details
    #     print("Speech synthesized for text '{0}' failed, reason: {1}, detail: {2}".format(text, result.reason, detail))
    #     return {"errno": 500, "errmsg": result}
    # stream = speechsdk.AudioDataStream(result)
    # stream.detach_input()
    # stream.save_to_wav_file_async(os.path.join(app.root_path, 'resources', '{0}.wav'.format(id))).get()
    return {"errno": 0, "id" : id}


if __name__ == '__main__':
    app.run()
