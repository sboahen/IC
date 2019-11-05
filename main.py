from gtts import gTTS
from pygame import mixer

mixer.init()
mixer.music.load("Welcome.mp3")
mixer.music.play()


while True:
    k = input()
    if k == '1':
        import read_mode
        break
    elif k == '2':
        import active_mode
        break
    else:
        mixer.music.play()
