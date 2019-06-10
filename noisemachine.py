from flask import Flask, render_template, request
from pygame import mixer
import os


audioFiles = []

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


def playAudioFile(filename):
    print("Play audio: {}".format(filename))
    volume = mixer.music.get_volume()
    mixer.music.load(filename)
    mixer.music.play(-1)
    mixer.music.set_volume(volume) #docs say volume is reset on new sound, so we keep it the same


def setVolume(value):
    volume = min(max(value, 0.0), 1.0)
    print("Set volume: {}".format(volume))
    mixer.music.set_volume(volume)


def formatAudioName(audioFile):
    basename = os.path.basename(audioFile)
    basenameNoExt = os.path.splitext(basename)[0]
    return basenameNoExt.capitalize()


@app.route('/')
def index():
    audioNames = [formatAudioName(name) for name in audioFiles]
    return render_template('index.html', len = len(audioNames), audioNames = audioNames)


@app.route('/play')
def play():
    print("Play")
    mixer.music.play(-1)
    return ""


@app.route('/stop')
def stop():
    print("Stop")
    mixer.music.stop()
    return ""


@app.route('/volume')
def volume():
    vol = float(request.args['value'])
    setVolume(vol)
    return ""


@app.route('/volumeDown')
def volumeDown():
    setVolume(mixer.music.get_volume() - 0.1)
    return ""


@app.route('/volumeUp')
def volumeUp():
    setVolume(mixer.music.get_volume() + 0.1)
    return ""


@app.route('/changeSound')
def changeSound():
    soundId = int(request.args['soundId'])
    print("soundId = {}".format(soundId))
    audioFile = audioFiles[soundId]
    playAudioFile(audioFile)
    return ""

if __name__ == "__main__":
    # List audio files
    audioDir = "./audio"
    audioFiles = [os.path.join(audioDir, f) for f in os.listdir(audioDir) if os.path.splitext(f)[1] == ".mp3"]

    # Initialize pygame music mixer
    mixer.pre_init(44100, -16, 2, 4096)
    mixer.init() # Pygame inits must be called on main thread. Flask app seems to run in a separate thread.

    with app.app_context(): # Start playing the first file
        playAudioFile(audioFiles[0])
        mixer.music.set_volume(0.5)

    # Run the webserver
    app.run(host='0.0.0.0', port='8080')
