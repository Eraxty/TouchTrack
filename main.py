import os

from audio import extract_audio, load_audio
from clap_detector import detect
from mapper import map_scores
from temporal_filter import smooth_events

VIDEO = "movie.mp4"
AUDIO = "temp.wav"
OUTPUT = "output.srt"

SR = 48000
WINDOW = 0.25


def format_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(events):
    with open(OUTPUT, "w", encoding="utf-8") as f:
        for i, e in enumerate(events, 1):
            f.write(f"{i}\n")
            f.write(
                f"{format_time(e['start'])} --> "
                f"{format_time(e['end'])} "
                f"{e['tag']} "
                f"{e['score']:.2f}\n"
            )
            f.write(f"Detected: {e['tag']}\n\n")

def main():
    if not os.path.exists(VIDEO):
        print("Video not found.")
        return

    extract_audio(VIDEO, AUDIO, SR)
    audio, sr = load_audio(AUDIO, SR)
    size = int(sr * WINDOW)
    frames = []

    for i in range(0, len(audio) - size + 1, size):
        clip = audio[i:i + size]
        time = i / sr
        scores = map_scores(detect(clip, sr))
        frames.append({
            "time": time,
            "scores": scores,
        })

        if scores:
            print(f"{time:6.2f}s -> {max(scores, key=scores.get)}")
        else:
            print(f"{time:6.2f}s -> SILENCE")

    events = smooth_events(frames, len(audio) / sr)
    write_srt(events)

    if os.path.exists(AUDIO):
        os.remove(AUDIO)

if __name__ == "__main__":
    main()