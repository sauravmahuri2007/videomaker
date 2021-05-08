import wave
import io
import ipdb

from espeakng import ESpeakNG


def main():
    esng = ESpeakNG()
    esng.voice = 'en-us'
    esng.pitch = 99
    esng.speed = 150
    txt = 'Hello John! How are you doing?'
    wave_bytes = esng.synth_wav(txt)
    with open('mywavfile.wav', 'wb') as wf:
        wf.write(wave_bytes)
    esng.say(txt)


if __name__ == '__main__':
    main()