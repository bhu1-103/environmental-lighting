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
import time
from pywizlight import wizlight, PilotBuilder
import colorsys

console = Console()

get_url = "http://localhost:4533/rest/getNowPlaying.view"
album_art_url = "http://localhost:4533/rest/getCoverArt.view"
supersonic_check = subprocess.run(["pgrep", "-af", "supersonic-desktop"], capture_output=True)

load_dotenv()
USERNAME = os.getenv("NAVIDROME_USERNAME")
PASSWORD = os.getenv("NAVIDROME_PASSWORD")
MODE = os.getenv("MODE")
BRIGHTNESS = int(os.getenv("BRIGHTNESS"))

params = {
        "u": USERNAME,
        "p": PASSWORD,
        "v": "1.16.1",
        "c": "album art based lightup",
        "f": "json"
        }

subprocess.run(["supersonic-desktop", "--play"])
if supersonic_check.returncode != 0:
    console.print("[#ff0000]Supersonic is closed. Exiting script.[/#ff0000]")
    exit()

r1 = requests.get(get_url, params=params)
data = r1.json()

def get_entries(data):
    entries = data["subsonic-response"]["nowPlaying"].get("entry", [])
    if not entries:
        print("[#ff0000]Nothing currently playing[/#ff0000]")
        print("[#ff3333]is supersonic running?[/#ff3333]")
        print("[#ff6666]attempting to play music on supersonic[/#ff6666]")
        subprocess.run(["supersonic-desktop", "--play"])
    return entries

entries = get_entries(data)
entry = entries[-1]
cover_art_id = entry["coverArt"]
album_art_params = {
    **params,
    "id": cover_art_id
    }
r2 = requests.get(album_art_url, params=album_art_params)

with open("cover.jpg", "wb") as f:
    f.write(r2.content)

async def poll_music():
    r1 = requests.get(get_url, params=params)
    data = r1.json()
    entries = get_entries(data)
    entry = entries[-1]
    last_title = None
    last_album = entry["album"]
    light = wizlight("192.168.0.10")
    await light.turn_on(PilotBuilder(brightness = BRIGHTNESS))
    while True:
        r1 = requests.get(get_url, params=params)
        data = r1.json()

        entries = get_entries(data)
        entry = entries[-1]

        title = entry["title"]
        if title == last_title:
            await asyncio.sleep(5)
            continue
        last_title = title
        album = entry["album"]
        artist = entry["artist"]
        track_no = entry["track"]

        if album != last_album:
            cover_art_id = entry["coverArt"]
            album_art_params = {
                **params,
                "id": cover_art_id
            }
            r2 = requests.get(album_art_url, params=album_art_params)
            with open("cover.jpg", "wb") as f:
                f.write(r2.content)

            # these are for when i need single album mode
            if MODE == "1":
                print("Go touch some grass")
                subprocess.run(["notify-send","Go touch grass","time to take a sip"])
                for i in range (6):
                    await light.turn_on(PilotBuilder(brightness = 51*(5-i)))
                    await asyncio.sleep(1)
                exit()

            # the 3 lines to make it either for single album immersion or dynamically change with each album
            elif MODE == "2":
                new_hues = extract_hues()
                top_hues[:] = new_hues

        last_album = album
    
        subprocess.run(["clear"])
        subprocess.run(["kitty","+kitten","icat","--place","12x12@1x1","cover.jpg"])

        table = Table(title=f"[#666666]Now Playing[/#666666] [#ff0066]{album}[/#ff0066]")
        table.add_column("Track")
        table.add_column("Title")
        table.add_column("Artist")

        table.add_row(f"[#c8a8c8]{track_no}[/#c8a8c8]",f"[#ff8fab]{title}[/#ff8fab]",f"[#20c498]{artist}[/#20c498]")
        console.print(Padding(table, (0,0,0,14)))
        await asyncio.sleep(5)

def extract_hues():
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
    hues = []

    for item in sorted_colors:
        hue = (item[1] + 0.5) / 32
        if hue not in hues:
            hues.append(hue)
        if len(hues) == 5:
            break
    hues.sort()
    return hues

top_hues = extract_hues()

def hsv2rgb(hue,s=1.0,v=1.0):
    r,g,b = colorsys.hsv_to_rgb(hue,s,v)
    return (int(r*255),int(g*255),int(b*255))

'''for i in range (0,5):
    print(hsv2rgb(top_hues[i]))
    print("these are the 5 colors")'''

transition_time = 60
def transition(a,b,t):
    return a + (b - a) * t

async def light_update():
    light = wizlight("192.168.0.10")
    current_hue = top_hues[0]

    while True:
        for i in range(len(top_hues)):
            start_hue = current_hue
            end_hue = top_hues[i]
            diff = end_hue - start_hue
            if abs(diff) > 0.5:
                if diff > 0:
                    start_hue += 1
                else:
                    end_hue += 1
            steps = 60

            for step in range(steps):
                t = step/steps
                cur_hue = transition(start_hue, end_hue, t)
                cur_hue %= 1.0
                color = hsv2rgb(cur_hue)
                #print(color)
                await light.turn_on(PilotBuilder(rgb = color))
                await asyncio.sleep(transition_time/steps)
            current_hue = cur_hue

async def main():
    await asyncio.gather(
        poll_music(),
        light_update()
        )

asyncio.run(main())
