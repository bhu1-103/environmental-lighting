Script I made to experiment with current technology and my WiZ light bulb

# environmental-lighting

- [x] environmental lighting based on album art of the music playing right now
- [x] fetch script to show currently playing music in terminal
- [x] credentials and mode setting and brightness in .env file
- [x] mode 1: killswitch when next album starts
- [x] mode 2: dynamically update light color to new album as more music plays
- [x] master script appropriately named "set-stage" saved in $PATH that sets the colors to my room based on current album's album art

![Fetch Script](./assets/fetch_script.png)

# smart-color-selector

- [ ] set color based on input sentence
- [x] find colors. thanks to [color names](https://github.com/meodai/color-names) by meodai
- [x] embedding all 31k colors (as of may 27 2026) using [all minilm](https://ollama.com/library/all-minilm) and script with ETA
