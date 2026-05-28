import json
from pathlib import Path

import ollama
from rich.progress import track

MODEL = "qwen3.5:0.8b"

OUTPUT_FILE = "color_tags.json"

SYSTEM_PROMPT = """
Generate EXACTLY 5 atmospheric tags for a color name.

Rules:
- Output ONLY comma-separated tags
- No numbering
- No lists
- No newlines
- No underscores
- No periods
- No explanations
- Tags should be short phrases or words
- Prefer cinematic, environmental, emotional, or aesthetic imagery
- Do not restate the input literally
- Avoid obvious color descriptors

Correct format:
foggy alley, rusted metal, twilight, distant rain, urban haze
"""

BANNED = {
    "beautiful",
    "nice",
    "cool",
    "color",
    "shade",
}

MAX_RETRIES = 4


# -----------------------------------
# CLEANING
# -----------------------------------

def clean_tags(raw, color_name):

    tags = [
        tag.strip().lower().replace(".", "")
        for tag in raw.split(",")
    ]

    tags = [
        tag for tag in tags
        if (
            len(tag) > 2
            and "_" not in tag
            and tag not in BANNED
            and tag != color_name.lower()
        )
    ]

    # remove duplicates while preserving order
    tags = list(dict.fromkeys(tags))

    return tags


# -----------------------------------
# LOAD COLORS
# -----------------------------------

with open("colornames.json") as f:
    colors = json.load(f)

# demo mode
# colors = colors[:10]


# -----------------------------------
# LOAD EXISTING PROGRESS
# -----------------------------------

output = []
completed = set()

if Path(OUTPUT_FILE).exists():

    with open(OUTPUT_FILE) as f:
        output = json.load(f)

    completed = {
        item["name"]
        for item in output
    }

    print(f"Resuming from {len(completed)} completed colors")


# -----------------------------------
# MAIN LOOP
# -----------------------------------

remaining = [
    color for color in colors
    if color["name"] not in completed
]

for color in track(remaining, description="Generating tags"):

    success = False

    for attempt in range(MAX_RETRIES):

        prompt = f"""
Color name: {color["name"]}
"""

        try:

            response = ollama.chat(
                model=MODEL,
                think=False,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.85,
                    "top_p": 0.9,
                    "repeat_penalty": 1.15,
                    "num_predict": 32,
                    "stop": ["\n"]
                }
            )

            raw = response["message"]["content"].strip()

            tags = clean_tags(raw, color["name"])

            if len(tags) < 5:

                print(f"\nRetry {attempt+1}: {color['name']}")
                print("RAW:", raw)
                print("CLEANED:", tags)

                continue

            tags = tags[:5]

            print(f"\n{color['name']}")
            print(tags)

            output.append({
                "name": color["name"],
                "hex": color["hex"],
                "tags": tags
            })

            success = True
            break

        except Exception as e:

            print(f"\nError on {color['name']}: {e}")

    if not success:

        print(f"\nFAILED: {color['name']}")

    # progressive save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

print("\nDone")
