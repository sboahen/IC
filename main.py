from read_mode import main as read_mode_main
from pygame import mixer

mixer.init()
mixer.music.load("Welcome.mp3")
mixer.music.play()


while True:
    k = input()
    if k == '1':
        read_mode_main()
        break
    elif k == '2':
        import active_mode
        break
    else:
        mixer.music.play()
