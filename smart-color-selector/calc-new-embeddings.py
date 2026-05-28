import json
import ollama
from rich.progress import track
import numpy as np

EMBED_MODEL = "all-minilm"

with open("color_tags.json") as f:
    colors = json.load(f)

metadata = []
embeddings = []

for color in track(colors, description="Embedding colors and tags"):

    embedding_text = f"""
{color["name"]}

{" ".join(color["tags"])}
"""

    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=embedding_text
    )

    metadata.append({
        "name": color["name"],
        "hex": color["hex"],
        "tags": color["tags"]
    })

    embeddings.append(response["embedding"])

embeddings = np.array(embeddings, dtype=np.float32)

embeddings = embeddings / np.linalg.norm(
    embeddings,
    axis=1,
    keepdims=True
)

print("Saving files")

with open("metadata.json", "w") as f:
    json.dump(metadata, f)

np.save("embeddings.npy", embeddings)

print("Done")
