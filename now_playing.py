import requests
from rich import print
from rich.table import Table
from rich.console import Console
from dotenv import load_dotenv
import os
import subprocess
from rich.padding import Padding
from PIL import Image
import asyncio
from pywizlight import wizlight, PilotBuilder
import colorsys

console = Console()

get_url = "http://localhost:4533/rest/getNowPlaying.view"
album_art_url = "http://localhost:4533/rest/getCoverArt.view"

load_dotenv()
USERNAME = os.getenv("NAVIDROME_USERNAME")
PASSWORD = os.getenv("NAVIDROME_PASSWORD")

params = {
        "u": USERNAME,
        "p": PASSWORD,
        "v": "1.16.1",
        "c": "album art based lightup",
        "f": "json"
        }

r1 = requests.get(get_url, params=params)
data = r1.json()

entries = data["subsonic-response"]["nowPlaying"]["entry"]

if not entries:
    print("[#ff0000]Nothing currently playing[/#ff0000]")
    exit()
entry = entries[-1]

title = entry["title"]
album = entry["album"]
artist = entry["artist"]
track_no = entry["track"]
cover_art_id = entry["coverArt"]

album_art_params = {
        **params,
        "id": cover_art_id
        }

r2 = requests.get(album_art_url, params=album_art_params)

with open("cover.jpg", "wb") as f:
    f.write(r2.content)

subprocess.run(["clear"])
subprocess.run(["kitty","+kitten","icat","--place","12x12@1x1","cover.jpg"])

table = Table(title=f"[#666666]Now Playing[/#666666] [#ff0066]{album}[/#ff0066]")
table.add_column("Track")
table.add_column("Title")
table.add_column("Artist")

table.add_row(f"[#c8a8c8]{track_no}[/#c8a8c8]",f"[#ff8fab]{title}[/#ff8fab]",f"[#20c498]{artist}[/#20c498]")
console.print(Padding(table, (0,0,0,14)))

img = Image.open("cover.jpg").convert("RGB")
img = img.resize((64,64))
colors = img.getcolors(1000000)
filtered = []

for count, color in colors:
    r,g,b = [x/255 for x in color]
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    hue_normal = int(h*32)
    filtered.append((count,hue_normal))

sorted_colors = sorted(filtered,key=lambda x: x[0],reverse=True)
top_hues = []

for item in sorted_colors:
    hue = item[1] / 32
    if hue not in top_hues:
        top_hues.append(hue)
    if len(top_hues) == 5:
        break

def hsv2rgb(hue,s=1.0,v=1.0):
    r,g,b = colorsys.hsv_to_rgb(hue,s,v)
    return (int(r*255),int(g*255),int(b*255))

best_color = hsv2rgb(top_hues[1])

async def main():
    light = wizlight("192.168.0.10")
    for hue in top_hues:
        color = hsv2rgb(hue)
        #print(color)
        await light.turn_on(PilotBuilder(rgb = color))
        await asyncio.sleep(1)
print(best_color)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
