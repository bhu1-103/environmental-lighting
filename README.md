Scripts I made to experiment with current technology and my WiZ light bulb

# environmental-lighting

![Fetch Script](./assets/fetch_script.png)

- [x] environmental lighting based on album art of the music playing right now
- [x] fetch script to show currently playing music in terminal
- [x] credentials and mode setting and brightness in .env file
- [x] mode 1: killswitch when next album starts
- [x] mode 2: dynamically update light color to new album as more music plays
- [x] master script appropriately named "set-stage" saved in $PATH that sets the colors to my room based on current album's album art

# smart-color-selector

![Over-Engineered Light Bulb](./assets/set-mood.png)

- [x] set color based on prompt (achieved on may 27 2026)
- [x] find colors. thanks to [color names](https://github.com/meodai/color-names) by meodai
- [x] embedding all 31k colors (as of may 27 2026) using [all minilm](https://ollama.com/library/all-minilm) and script with ETA
- [x] generate tags for all colors using [qwen3.5:0.8b](https://ollama.com/library/qwen3.5). It took 6 hours to generate the tags.... (Well worth it)
- [x] tested various embedding models and finalized -> snowflake-arctic-embed:22m
- [ ] parallelize the generation of embeddings as embedding models are tiny
- [ ] use tiny llm to even generate the prompts as well and keep cycling color schemes every 1 hour or so
- [ ] auto detect mood based on what's on screen and probably use an llm that does vision as well

| Model | Speed | Quality | Notes |
|---|---|---|---|
| qwen3.5:0.8b | medium | Best overall | Good creativity |
| qwen3:4b | slowest | Straight up bad | "aktually 🤓☝️" and harder to follow rules |
| qwen3:1.7b | fast | Cinematic | Very good but always "soft glow" "ethereal" "muted tones"|
| qwen3:0.6b | fast | Repetitive | Same as 1.7b but obsessed with "ethereal"|
| qwen2.5:0.5b | fastest | Alright | Very basic model, just sticks to catchphrases like "ethereal"|

| Model | Speed (generating 31k embeddings) | Quality | Notes | results |
|---|---|---|---|---|
| granite:33m | 00:16:03 | linkedin 🧠📉 | <details><summary>i would use rapidfuzz or pywal instead, like a caveman</summary>Truth be told, it seems like this is better for RAG than creative tasks. Still very 🧠🪦 | [check here](./smart-color-selector/embedding_model_cookoff/emb_ibm-granite-33m.md) |
| all-minilm:22m | 00:09:52 | excellent | it's better than 33m variant, but feels robotic | [check here](./smart-color-selector/embedding_model_cookoff/emb_all-minilm-22m.md) |
| all-minilm:33m | 00:11:13 | good | no soul + a bit corpo | [check here](./smart-color-selector/embedding_model_cookoff/emb_all-minilm-33m.md) |
| snowflake-arctic-embed:22m | 00:08:07 | excellent | perfect model for this use case | [check here](./smart-color-selector/embedding_model_cookoff/emb_snowflake-arctic-embed-22m.md) |
| snowflake-arctic-embed:33m | 00:09:36 | good | loses character compared to smaller model | [check here](./smart-color-selector/embedding_model_cookoff/emb_snowflake-arctic-embed-33m.md) |
| <details><summary>larger models</summary>nomic-embed-moe, bge-m3, mxbai-embed-large</details> | 1-2 hours | bad | not really good for this use case | <details><summary>NA</summary>not gonna waste any more time</details> |

One thing I learnt after using all these models is that <b>~~bigger is better~~</b> or <b>~~newer is better~~</b> is now always true.

## issues/to-do-list

<details><summary>Turns out parallelizing made it slower, I ran 4 instances of ollama, only to get a higher ETA.</summary>

One model used approximately 126 mb vram, I spun up 3 more instances of ollama and models were working with minimal GPU usage, but for some reason, the ETA when 4 models were running concurrently was 5+ minutes higher. It probably had something to do with how my script does the scheduling to 4 independent models. Will fix it later

| Threads | out |
|---|---|
| 1 | Embedding colors and tags ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   3% 0:08:55 |
| 4 | Embedding colors and tags ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   3% 0:14:09 |
</details>
