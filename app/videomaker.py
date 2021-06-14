import ffmpeg
import subprocess
from pathlib import Path

from espeakng import ESpeakNG
try:
    from gtts import gTTS
except ImportError:
    gTTS = None


from .settings import TEMP_DIR


class VideoMaker:

    # Supported Text to Speech libraries to convert a text to audio file.
    TTS_ENGINES = ('espeak', 'ffmpeg', 'google')

    VIDEO_ENGINES = ('ffmpeg')
    
    def __init__(self: object, file_name: str, text: str, tts_engine='espeak', image_path=None):
        if tts_engine not in self.TTS_ENGINES:
            raise ValueError(f'Engine {tts_engine} is not supported. Available TTS engines: {TTS_ENGINES}')

        self._file_name = file_name
        file_name_splits = self._file_name.rsplit('.', 1)
        self._file_name_no_extention = file_name_splits[0]
        self._file_extension = len(file_name_splits) > 1 and '.' + file_name_splits[1].lower() or '.mp4'
        self._defaul_audio_extension = '.wav'
        self._text = text
        self._temp_file_path = TEMP_DIR
        self._image_path = image_path and Path(image_path) or Path(__file__).parent / 'images' / 'no_image.png'
        self._tts_engine = tts_engine.lower()

    def _is_gtts_installed(self):
        return gTTS != None

    def _get_audio_file_gtts(self, file_type='mp3', lang='en', tld='ca'):
        # Returns a pathlib.PATH instance of audio file created
        if not self._is_gtts_installed:
            raise RuntimeError('Please make sure to install gTTS library: `pip install gTTS`')
        
        tts = gTTS(self._text, lang=lang, tld=tld)
        file_path = self._temp_file_path / (self._file_name_no_extention + '.mp3')
        tts.save(str(file_path))
        return file_path

    def _create_video(self, audio_path, image_path):
        output_options = {
            'crf': 25,
            'vcodec': 'libx264',
            'acodec': 'mp3',
            'vf': 'format=yuv444p,scale=1920:1080',
            'g': 100000,
        }
        file_path = self._temp_file_path / self._file_name
        if image_path.is_dir():
            image_input = (ffmpeg.input(str(image_path) + '/*.png', pattern_type='glob', framerate=25))
        else:
            image_input = ffmpeg.input(str(image_path), loop=1, framerate=25)
        audio_input = ffmpeg.input(str(audio_path))
        out = ffmpeg.output(image_input, audio_input, str(file_path), **output_options)
        out.run()
        return file_path

    def _create_video_ffmpeg_cmd(self, audio_path, image_path, output_path=''):
        if not output_path:
            output_path = self._temp_file_path / self._file_name
        acodec = 'aac'
        vcodec = 'h264'
        format = 'yuv420p'
        scale = '1920:1080'
        gstream = '100000'
        framerate = '25'
        cmd_args = [
            'ffmpeg', 
            '-loop', '1',
            '-y',
            '-i', str(image_path), 
            '-i', str(audio_path),
            '-shortest',
            '-acodec', acodec,
            '-vcodec', vcodec,
            '-crf', framerate,
            '-vf', f'format={format},scale={scale}',
            '-g', gstream,
            str(output_path)
        ]
        print(' '.join(cmd_args))
        p = subprocess.Popen(cmd_args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        res = iter(p.stdout.readline, b'')
        for line in res:
            print(line)
        p.stdout.close()
        if p.stderr:
            p.stderr.close()
        if p.stdin:
            p.stdin.close()
        p.wait()
        return output_path


    def _get_audio_file_espeak(self):
        # Returns a pathlib.PATH instance of audio file created
        esng = ESpeakNG()
        esng.voice = 'en-us'
        esng.pitch = 80
        esng.speed = 140
        file_path = self._temp_file_path / (self._file_name_no_extention + self._defaul_audio_extension)
        wave_bytes = esng.synth_wav(self._text)
        with open(str(file_path), 'wb') as wf:
            wf.write(wave_bytes)
        return file_path

    def make_video(self):
        if self._tts_engine == 'google':
            audio_file_path = self._get_audio_file_gtts()
        elif self._tts_engine == 'espeak':
            audio_file_path = self._get_audio_file_espeak()
        elif self._tts_engine == 'ffmpeg':
            audio_file_path = self._get_audio_file_ffmpeg()

        video_path = self._create_video_ffmpeg_cmd(audio_file_path, self._image_path)
        audio_file_path.unlink()
        return str(video_path)


if __name__ == '__main__':
    txt = """
    In 2012, Oliver Scott Curry was an anthropology lecturer at the University of Oxford.
    One day, he organized a debate among his students about whether morality was innate or acquired.
    One side argued passionately that morality was the same everywhere; the other, that morals were different everywhere.
    """
    vm = VideoMaker('read.mp4', txt, tts_engine='google')
    print(vm.make_video())
