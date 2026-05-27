import json
import numpy as np
import ollama
import asyncio
import colorsys
from pywizlight import wizlight, PilotBuilder

light_ip = "192.168.0.10"

with open("metadata.json") as f:
    metadata = json.load(f)

embeddings = np.load("embeddings.npy")
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

def hex_to_rgb(hexcode):
    hexcode = hexcode.lstrip("#")
    return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

def transition(a, b, t):
    return a + (b - a) * t

def rgb_to_hsv(rgb):
    r, g, b = [x / 255 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)

def hsv_to_rgb(h, s=1.0, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def get_palette():
    sentence = input("Enter a sentence: ")

    query_embedding = ollama.embeddings(
        model="all-minilm",
        prompt=sentence
    )["embedding"]

    query_vector = np.array(query_embedding, dtype=np.float32)
    query_vector = query_vector / np.linalg.norm(query_vector)

    scores = embeddings @ query_vector
    top_indices = np.argsort(scores)[::-1][:5]

    print("\nTop matches:\n")

    palette = []
    for idx in top_indices:
        item = metadata[idx]
        print(f"{item['name']}: {item['hex']}  ({scores[idx]:.3f})")
        palette.append(item["hex"])

    return [hex_to_rgb(color) for color in palette]

async def light_update():
    light = wizlight(light_ip)

    palette = get_palette()
    current_color = palette[0]

    while True:
        for i in range(len(palette)):

            start_rgb = current_color
            end_rgb = palette[i]

            start_h, start_s, start_v = rgb_to_hsv(start_rgb)
            end_h, end_s, end_v = rgb_to_hsv(end_rgb)

            diff = end_h - start_h
            if abs(diff) > 0.5:
                if diff > 0:
                    start_h += 1
                else:
                    end_h += 1

            steps = 60

            for step in range(steps):
                t = step / steps

                cur_h = transition(start_h, end_h, t) % 1.0
                cur_s = transition(start_s, end_s, t)
                cur_v = transition(start_v, end_v, t)

                color = hsv_to_rgb(cur_h, cur_s, cur_v)

                await light.turn_on(PilotBuilder(rgb=color))
                await asyncio.sleep(0.05)

            current_color = end_rgb

async def main():
    await light_update()

asyncio.run(main())
