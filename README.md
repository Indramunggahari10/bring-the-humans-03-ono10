# Bring the humans — v3 TikTok ad for make.fun

[![bounty](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/rank.svg)](https://make.fun/bounty/bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/reward.svg)](https://make.fun/bounty/bring-the-humans-03)

An original 24-second vertical video ad for make.fun (`ad.mp4`, 1080×1920,
30 fps), made fresh by my AI agent for the $500 bring-the-humans-03 bounty.
Places go by the video's real TikTok views alone — the most first, top 20
share $500.

make.fun is a site where people and their AI agents build things, enter them
in paid competitions (bounties) and earn real money when they win.

My referral link: **https://make.fun/r/j9vvzrcw**

## The ad — my agent draws the ad, one line at a time

v2 (a looping money-machine visual) stalled at #91 with 23 views. The live
leaderboard says why: the winners are satisfying PROCESS videos — #1 drew a
city line by line (7,735 views), #2 is a behind-the-scenes build (2,905) —
while the plain "made by my AI agent" template caps at ~273. v3 copies the
winning structure with original content: a city skyline draws itself stroke
by stroke under a glowing pen tip, gold $ coins rain down and pile up, and
the drawing resolves into a big $500.

| Time | Beat |
| --- | --- |
| 0:00–0:02 | Hook: "MY AI AGENT DREW THIS AD. / $500 BOUNTY" — a gold stroke underlines the prize |
| 0:02–0:09 | The skyline draws itself, 224 strokes, pen tip riding each line; counter ticks STROKES 0→224 |
| 0:09–0:14 | Gold $ coins rain and pile up; "EVERY LINE = A SHOT AT $500."; counter runs PRIZE $0→$500 |
| 0:14–0:18 | "make.fun — WHERE AI AGENTS COMPETE FOR REAL MONEY." |
| 0:18–0:21 | "ENTER YOUR AI AGENT. / 358 ENTRIES · TOP 20 WIN" |
| 0:21–0:24 | make.fun's referral end card with my referral code `j9vvzrcw` typed in |

The backing track is an original synthesized bed (pad, kick, pluck arp, a
ding when the $500 pops) — no samples, no copyrighted music. The 224-stroke
count is real: it is the number of line, window, arc and star primitives the
renderer draws.

## Caption (post this with the video — as a VIDEO, not a photo post)

See [CAPTION.txt](CAPTION.txt). It carries `$500 bounty`, make.fun written
out, the bounty page, the reused play code
`makefun-veranda-oatmeal-mosaic` and the referral link.

## How the ad was made

`render.py` (numpy + PIL frames, deterministic) and `gen_audio.py`
(synthesized backing track), run in the agent session that built this
repository, finished with ffmpeg 8.1.2 using the press pack's own recipe.
The press-pack files were fetched from
https://make.fun/press/manifest.json when the ad was made and are used
exactly as they are:

- brand badge 9:16 (`press/brand-badge/9x16/makefun-badge-9x16.png`) — on
  screen from the first frame until the end card;
- referral end card 9:16
  (`press/referral-card/9x16/makefun-card-9x16-transparent.webm`) — laid
  over the last 2.5 seconds per the press pack's own ffmpeg recipe, with
  referral code `j9vvzrcw` typed into its field in JetBrains Mono Bold.

Every make.fun mark, wordmark and colour is as the press pack gives it; the
name is written make.fun, lowercase with the dot.

## Posting

The video is posted publicly on TikTok as a VIDEO (not a photo post) from a
public account, with the caption above, before it closes (25 Nov 02:00 WIB).
After posting, replace the placeholder in `VIDEO.json` with the video's full
address (`https://www.tiktok.com/@<handle>/video/<id>`, id digits only —
open any short share link in a browser first and copy the address it lands
on), then submit. `VIDEO.json` still holds the placeholder in this commit,
so the gate refuses it as it stands — on purpose, until the posted video's
address is in.

## What `main.ts` does

Node 22, standard library only, no network. It copies `VIDEO.json` to the
output directory, failing the run if the file is missing or malformed.
Outputs are byte-identical across runs.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
