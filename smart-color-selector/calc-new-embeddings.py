import json
import ollama
from rich.progress import track
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
EMBED_MODEL = os.getenv("EMBED_MODEL")

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

with open(f"{EMBED_MODEL}.json", "w") as f:
    json.dump(metadata, f)

np.save(f"{EMBED_MODEL}.npy", embeddings)

print("Done")
