import os
import librosa

from audio import extract_audio, load_audio
from clap_detector import detect
from mapper import map_event

video = "movie.mp4"
audio = "temp.wav"


def main():
    if not os.path.exists(video):
        print("video not found")
        return

    extract_audio(video, audio)
    samples, sr = load_audio(audio)

    samples = librosa.resample(samples,orig_sr=sr,target_sr=48000)
    sr = 48000

    clip_length = sr * 3
    start = 0

    while start < len(samples):
        print(f"\ntime {start / sr:.1f}s")
        clip = samples[start:start + clip_length]
        predictions = detect(clip, sr)

        best_label, confidence = predictions[0]

        if confidence >= 0.75:
            tag = map_event(best_label)
        else:
            tag = "SILENCE"

        for label, score in predictions:
            print(f"  {label:<25} {score:.2f}")

        print(f"  -> {tag}")
        start += clip_length

    os.remove(audio)

if __name__ == "__main__":
    main()