GROUPS = {
    "ENGINE_REVVING": [
        "engine",
        "car engine",
        "engine revving",
        "engine idling",
        "vehicle engine",
        "sports car",
        "race car",
        "car driving",
    ],

    "WHOOSH": [
        "car passing",
        "tire screech",
        "car drifting",
    ],

    "METALLIC_HIT": [
        "metal impact",
        "glass breaking",
        "car crash",
    ],

    "BIG_BOOM": [
        "explosion",
    ],

    "THUNDER": [
        "thunder",
    ],

    "WIND_GUST": [
        "wind",
    ],

    "SMALL_CLICK": [
        "click",
    ],

    "FOOTSTEP_HEAVY": [
        "footsteps",
    ],

    "PISTOL_SHOT": [
        "gunshot",
    ],
}


def map_scores(predictions):
    scores = {}

    for label, conf in predictions:
        text = label.lower()

        for event, names in GROUPS.items():
            if any(name in text for name in names):
                scores[event] = scores.get(event, 0.0) + conf
                break

    if not scores:
        return {}

    best = max(scores.values())

    # reject weak predictions
    if best < 0.45:
        return {}

    if len(scores) > 1:
        values = sorted(scores.values(), reverse=True)
        if values[0] - values[1] < 0.10:
            return {}

    return scores