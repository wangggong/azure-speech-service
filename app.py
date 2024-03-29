from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import azure.cognitiveservices.speech as speechsdk
from game import *
import os
import uuid


app = Flask(__name__)
app.config.from_json("config.json")
games = {}


# speech_config = speechsdk.SpeechConfig(subscription=app.config.get("SPEECH_KEY"), region=app.config.get("SPEECH_REGION"))
# # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
# audio_config = None
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


@app.route('/txt2speech', methods=['GET', 'POST'])
def txt_to_speech():
    print('Request for txt2speech, method = ' + request.method)
    if request.method == 'GET':
        return get_txt_to_speech(request.args.get('id'))
    elif request.method == 'POST':
        return create_txt_to_speech_task(request.form.get("text"))


@app.route('/games/oce/<int:player_count>', methods=['GET', 'POST'])
def create_oce_game(player_count):
    print('create oce game, player count {player_count}')
    game = Game(player_count)
    games[game.id] = game
    return {"errno": 200, "id": game.id}


@app.route('/games/oce/<string:_id>', methods=['GET'])
def get_oce_game(_id):
    print('get oce game, method = ' + request.method)
    game = games.get(_id)
    if not game:
        return {"errno": 404}
    return {"errno": 200, "detail": str(game)}


@app.route('/games/oce/<string:_id>/add_player/{string:alias}', methods=['GET', 'POST'])
def add_player(_id, alias):
    print(f'add player {alias} for game {_id}')
    games[game.id] = game
    if not game:
        return {"errno": 404}
    game.add_player(Player(alias))
    return {"errno": 200}


def format_ssml(text, voice_name, rate, pitch):
    return '''<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="{0}">
        <prosody rate="{1}%" pitch="{2}%">{3}</prosody></voice></speak>'''.format(voice_name, rate, pitch, text)


def get_txt_to_speech(id):
    print('GET audio file, id = {0}'.format(id))
    return send_from_directory(os.path.join(app.root_path, "resource"), "{0}.wav".format(id), as_attachment=True)


def create_txt_to_speech_task(text):
    id = str(uuid.uuid1())
    rate = request.form.get("rate") or "50%"
    pitch = request.form.get("pitch") or "0"
    voice_name = request.form.get("voice-name") or app.config.get("DEFAULT_VOICE_NAME")
    print("start trans, id = {0}, text = {1}".format(id, text))
    speech_config = speechsdk.SpeechConfig(subscription=app.config.get("SPEECH_KEY"), region=app.config.get("SPEECH_REGION"))
    audio_config = None
    speech_config.speech_synthesis_voice_name = voice_name
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_ssml_async(format_ssml(text, voice_name, rate, pitch)).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        if result.reason == speechsdk.ResultReason.Canceled:
            detail = result.cancellation_details
        print("Speech synthesized for text '{0}' failed, reason: {1}, detail: {2}".format(text, result.reason, detail))
        return {"errno": 500, "errmsg": result}
    stream = speechsdk.AudioDataStream(result)
    stream.detach_input()
    stream.save_to_wav_file(os.path.join(app.root_path, 'resource', '{0}.wav'.format(id)))
    return send_from_directory(os.path.join(app.root_path, "resource"), "{0}.wav".format(id), as_attachment=True)


if __name__ == '__main__':
    app.run()
