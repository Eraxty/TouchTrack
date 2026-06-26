import torch
from transformers import ClapModel, ClapProcessor

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = ClapProcessor.from_pretrained("laion/clap-htsat-fused")
model = ClapModel.from_pretrained("laion/clap-htsat-fused").to(device)
model.eval()

labels = [
    "speech",
    "music",
    "engine",
    "car engine",
    "engine revving",
    "engine idling",
    "vehicle engine",
    "sports car",
    "race car",
    "car driving",
    "car passing",
    "tire screech",
    "car drifting",
    "metal impact",
    "glass breaking",
    "car crash",
    "explosion",
    "wind",
    "thunder",
    "crowd",
    "footsteps",
    "click",
    "gunshot",
]

@torch.inference_mode()
def detect(audio, sr):
    inputs = processor(
        text=labels,
        audio=audio,
        sampling_rate=sr,
        return_tensors="pt",
        padding=True,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    logits = model(**inputs).logits_per_audio[0]
    scores = logits.softmax(dim=0)

    preds = list(zip(labels, scores.tolist()))
    preds.sort(key=lambda x: x[1], reverse=True)

    return preds