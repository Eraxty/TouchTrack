def map_event(label):
    mapping = {
        "explosion": "BIG_BOOM",
        "gunshot": "PISTOL_SHOT",
        "glass breaking": "METALLIC_HIT",
        "metal impact": "SWORD_CLASH",
        "car engine": "ENGINE_IDLE",
        "car crash": "CAR_CRASH",
        "footsteps": "FOOTSTEP_LIGHT",
        "heartbeat": "HEARTBEAT_NORMAL",
        "rain": "RAIN_DROPLET",
        "thunder": "THUNDER",
        "wind": "WIND_GUST",
        "train": "TRAIN_IMPACT",
        "airplane": "AIRPLANE_CRASH",
        "helicopter": "HELICOPTER_CRASH",
        "speech": "SILENCE",
        "music": "SILENCE",
    }

    return mapping.get(label, "SILENCE")