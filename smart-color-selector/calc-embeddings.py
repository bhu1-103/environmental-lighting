import json
import ollama
from datetime import datetime
from rich import print

print("loading colors...")

with open("colornames.json") as f:
    colors = json.load(f)

embedded_colors = []
total = len(colors)
start_time = datetime.now()

for i,color in enumerate(colors, start=1):
    response = ollama.embeddings(
        model='all-minilm',
        prompt=color["name"]
    )

    embedded_colors.append({
        "name": color["name"],
        "hex": color["hex"],
        "embedding": response["embedding"]
    })
    
    if i % 300 == 0:

        percentage = i/total*100
        now = datetime.now()
        difference = now - start_time
        seconds_elapsed = difference.total_seconds()
        time_per_embedding = (seconds_elapsed / i)
        ER_minutes  = int(time_per_embedding * total) // 60
        ER_seconds  = (time_per_embedding * total) % 60
        ETA_minutes = (time_per_embedding * (total - i)) // 60
        ETA_seconds = (time_per_embedding * (total - i)) % 60
        print("------------------------------------------")
        print(f"[#ffffff]{i}/{total}[/#ffffff] embeddings done. [#ffffff]{percentage:.2f}%[/#ffffff] complete")
        print(f"Expected runtime: [#ff0066]{ER_minutes}[/#ff0066] minutes [#ff0066]{ER_seconds:.0f}[/#ff0066] seconds")
        print(f"ETA: [#00ffff]{ETA_minutes:.0f}[/#00ffff] minutes [#00ffff]{ETA_seconds:.0f}[/#00ffff] seconds")
        print("------------------------------------------")

print("Saving to file db.json")

with open("db.json","w") as f:
    json.dump(embedded_colors, f)

    print("Done")
