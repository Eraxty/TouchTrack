import torch
from transformers import ClapProcessor, ClapModel

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = ClapProcessor.from_pretrained("laion/clap-htsat-fused")
model = ClapModel.from_pretrained("laion/clap-htsat-fused").to(device)

labels = [
    "speech",
    "music",
    "explosion",
    "gunshot",
    "glass breaking",
    "metal impact",
    "car engine",
    "car crash",
    "footsteps",
    "heartbeat",
    "rain",
    "thunder",
    "wind",
    "train",
    "airplane",
    "helicopter"
]


def detect(clip, sr):
    inputs = processor(
        text=labels,
        audio=clip,
        sampling_rate=sr,
        return_tensors="pt",
        padding=True,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    scores = outputs.logits_per_audio.softmax(dim=1)[0]
    values, indices = torch.topk(scores, k=3)
    predictions = []

    for i in range(3):
        predictions.append(
            (
                labels[indices[i].item()],
                values[i].item()
            )
        )

    return predictions