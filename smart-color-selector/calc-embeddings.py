import json
import ollama
from datetime import datetime
from rich.progress import track
import numpy as np

with open("colornames.json") as f:
    colors = json.load(f)

metadata = []
embeddings = []

for i, color in enumerate(track(colors, description="Embedding colors...", transient=False)):
    response = ollama.embeddings(
        model='all-minilm',
        prompt=color["name"]
    )

    metadata.append({
        "name": color["name"],
        "hex": color["hex"],
    })

    embeddings.append(response["embedding"])

print("Saving files")

with open("metadata.json", "w") as f:
    json.dump(metadata,f)

np.save("embeddings.npy", np.array(embeddings, dtype=np.float32))

print("Done")
