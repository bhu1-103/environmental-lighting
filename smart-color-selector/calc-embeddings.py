import json
import ollama
from datetime import datetime

print("loading colors...")

with open("colornames.json") as f:
    colors = json.load(f)

embedded_colors = []
total = len(colors)
start_time = datetime.now()

for i,color in enumerate(colors):
    response = ollama.embeddings(
        model='all-minilm',
        prompt=color["name"]
    )

    embedded_colors.append({
        "name": color["name"],
        "hex": color["hex"],
        "embedding": response["embedding"]
    })
    
    if i % 300 == 0 and i != 0:

        percentage = i/total*100
        now = datetime.now()
        difference = now - start_time
        seconds_elapsed = difference.total_seconds()
        ETA_minutes = (seconds_elapsed * total) / (i * 60) 
        ETA_seconds = ((seconds_elapsed * total) / (i)) % 60 
        print(f"{i}/{total} embeddings done")
        print(f"{percentage:.2f}% complete")
        print(f"ETA: {ETA_minutes:.0f} minutes {ETA_seconds:.0f} seconds")
        j = 0

print("Saving to file db.json")

with open("db.json","w") as f:
    json.dump(embedded_colors, f)

    print("Done")
