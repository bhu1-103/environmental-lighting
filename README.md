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
- [x] generate tags for all colors using [qwen3.5:0.8b](https://ollama.com/library/qwen3.5)

| Model | Speed | Quality | Notes |
|---|---|---|---|
| qwen3.5:0.8b | medium | Best overall | Good creativity |
| qwen3:4b | slowest | Straight up bad | "aktually 🤓" and harder to follow rules |
| qwen3:1.7b | fast | Cinematic | Very good but always "soft glow" "ethereal" "muted tones"|
| qwen3:0.6b | fast | Repititive | Same as 1.7b but obsessed with "ethereal"|
| qwen2.5:0.5b | fastest | Alright | Very basic model, just sticks to catchphrases like "ethereal"|

- [x] generate new embeddings along with the tags
- [ ] parallelize the generation of embeddings as embedding models are tiny

| Threads | out |
|---|---|
| 1 | Embedding colors and tags ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   3% 0:08:55 |
| 4 | Embedding colors and tags ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   3% 0:14:09 |

Turns out parallelizing made it slower, I ram 4 instances of ollama, only to get a higher ETA
