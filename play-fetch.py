import requests
from rich import print
from rich.table import Table
from rich.console import Console
from dotenv import load_dotenv
import os
import subprocess
from rich.padding import Padding

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

entries = data["subsonic-response"]["nowPlaying"].get("entry", [])

if not entries:
    print("[#ff0000]Nothing currently playing[/#ff0000]")
    exit()

entry = entries[-1]

cover_art_id = entry["coverArt"]

album_art_params = {
    **params,
    "id": cover_art_id
    }

r2 = requests.get(album_art_url, params=album_art_params)

with open("cover.jpg", "wb") as f:
    f.write(r2.content)

title = entry["title"]
album = entry["album"]
artist = entry["artist"]
track_no = entry["track"]

subprocess.run(["clear"])
subprocess.run(["kitty","+kitten","icat","--place","12x12@1x1","cover.jpg"])

table = Table(title=f"[#666666]Now Playing[/#666666] [#ff0066]{album}[/#ff0066]")
table.add_column("Track")
table.add_column("Title")
table.add_column("Artist")

table.add_row(f"[#c8a8c8]{track_no}[/#c8a8c8]",f"[#ff8fab]{title}[/#ff8fab]",f"[#20c498]{artist}[/#20c498]")

console.print(Padding(table, (0,0,0,14)))
