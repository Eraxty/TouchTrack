import ffmpeg
import librosa

def extract_audio(video, audio):
    (ffmpeg.input(video).output(audio).overwrite_output().run(quiet=True))

def load_audio(audio):
    samples, sr = librosa.load(audio, sr=None)
    return samples, sr