"""Video Maker.

Usage:
    vmaker.py --txt <txt> [--output <output>] [--img <img>] [--ttse <ttse>] [--espeak <espeak_args>...] [--ffmpeg <ffmpeg_args>...]
    vmaker.py --txtfile <txtfile> [--output <output>] [--img <img>] [--ttse <ttse>] [--espeak <espeak_args>...] [--ffmpeg <ffmpeg_args>...]
    vmaker.py (-h | --help)
    vmaker.py --version

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --ttse                      Text to speech engine [default: espeak]
    --txt                       Text which will be converted into speech file [default: Hello World]
    --txtfile                   Text file path to read text and convert into video.
    --output                    Path to save created video. If no absolute path then will save into current location.
    --img                       Path to image. Can be a blob format like ~/images/*.png
    --ffmpeg                    ffmpeg extra arguments to override default used [default: ffmpeg -acodec mp3 -vcodec libx265 -vf format=yuv444p,scale=1920:1080 -crf 25]
    --espeak                    espeak extra arguments to override default used [default: espeak]
    --gtts                      Google text to speech arguments [default: slow=True | Normal=False]
"""
from docopt import docopt

from app import videomaker

def main(**kwargs):
    txt = kwargs.get('<txt>') or 'Hello World'
    output = kwargs.get('<output>')
    img = kwargs.get('<img>')
    ttse = kwargs.get('<ttse>') or 'google'
    vm = videomaker.VideoMaker(file_name=output, text=txt, image_path=img, tts_engine=ttse)
    video_path = vm.make_video()
    return video_path


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Video Maker 1.0')
    print(main(**arguments))

