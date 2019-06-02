from flask import Flask, render_template, request
from pygame import mixer

audioFiles = [
    "audio/whitenoise1.mp3",
    "audio/whitenoise2.mp3",
    "audio/stream.mp3",
    "audio/waves.mp3",
]

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def playAudioFile(filename):
    mixer.music.load(filename)
    mixer.music.play(-1)

@app.route('/')
def index():
    return render_template('index.html')

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
    print("Set volume: {}".format(vol))
    mixer.music.set_volume(vol)
    return ""

@app.route('/changeSound')
def changeSound():
    soundId = int(request.args['soundId'])
    audioFile = audioFiles[soundId]
    print("Change sound: {}".format(audioFile))
    playAudioFile(audioFile)
    return ""

if __name__ == "__main__":
    mixer.pre_init(44100, -16, 2, 4096)
    mixer.init() # Pygame inits must be called on main thread. Flask app seems to run in a separate thread.

    with app.app_context(): # Start playing the first file
        playAudioFile(audioFiles[0])
        mixer.music.set_volume(0.5)

    app.run(host='0.0.0.0', port='8080')
