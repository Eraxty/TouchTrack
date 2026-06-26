from collections import deque

HISTORY = 5
START_FRAMES = 2
END_FRAMES = 3

MIN_SCORE = 0.35
MIN_DURATION = 0.5
MERGE_GAP = 0.5


def vote(history):
    totals = {}
    counts = {}

    for frame in history:
        for tag, score in frame["scores"].items():
            totals[tag] = totals.get(tag, 0.0) + score
            counts[tag] = counts.get(tag, 0) + 1

    if not totals:
        return "SILENCE", 0.0

    averages = {
        tag: totals[tag] / counts[tag]
        for tag in totals
    }

    tag = max(averages, key=averages.get)
    score = averages[tag]

    if score < MIN_SCORE:
        return "SILENCE", 0.0
    return tag, score

def smooth_events(frames, end_time, frame_time):
    history = deque(maxlen=HISTORY)
    events = []
    current = None
    current_score = 0.0
    start_time = 0.0
    candidate = None
    candidate_frames = 0
    end_frames = 0

    for frame in frames:
        history.append(frame)
        tag, score = vote(history)
        t = frame["time"]
        frame["stable"] = current or "SILENCE"

        if current is None:

            if tag == "SILENCE":
                candidate = None
                candidate_frames = 0
                continue

            if tag != candidate:
                candidate = tag
                candidate_frames = 1
                continue

            candidate_frames += 1

            if candidate_frames >= START_FRAMES:
                current = candidate
                current_score = score
                start_time = t - (START_FRAMES - 1) * frame_time
                candidate = None
                candidate_frames = 0
            continue

        if tag == current:
            current_score = max(current_score, score)
            end_frames = 0
            continue

        end_frames += 1

        if end_frames < END_FRAMES:
            continue

        events.append({
            "start": start_time,
            "end": t - (END_FRAMES - 1) * frame_time,
            "tag": current,
            "score": current_score,
        })

        current = None
        current_score = 0.0
        candidate = None
        candidate_frames = 0
        end_frames = 0

    if current is not None:
        events.append({
            "start": start_time,
            "end": end_time,
            "tag": current,
            "score": current_score,
        })
    merged = []

    for event in events:
        if event["end"] - event["start"] < MIN_DURATION:
            continue
        if (merged and merged[-1]["tag"] == event["tag"] and event["start"] - merged[-1]["end"] <= MERGE_GAP):
            merged[-1]["end"] = event["end"]
            merged[-1]["score"] = max(merged[-1]["score"],event["score"],)
        else:
            merged.append(event)
    return merged