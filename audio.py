import ffmpeg
import librosa

def extract_audio(video_file, audio_file, sr=48000):
    (ffmpeg.input(video_file).output(audio_file, ac=1, ar=sr).overwrite_output().run(quiet=True))

def load_audio(audio_file, sr=48000):
    samples, old_sr = librosa.load(audio_file, sr=None, mono=True)
    if old_sr != sr:
        samples = librosa.resample(samples, orig_sr=old_sr, target_sr=sr)
    return samples, sr
