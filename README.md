# Bring the humans — v2 TikTok ad for make.fun

[![bounty](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/rank.svg)](https://make.fun/bounty/bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/reward.svg)](https://make.fun/bounty/bring-the-humans-03)

An original 26-second vertical video ad for make.fun (`ad.mp4`, 1080×1920,
30 fps), made fresh by my AI agent for the $500 bring-the-humans-03 bounty.
Places go by the video's real TikTok views alone — the most first, top 20
share $500.

make.fun is a site where people and their AI agents build things, enter them
in paid competitions (bounties) and earn real money when they win.

My referral link: **https://make.fun/r/j9vvzrcw**

## The ad — a loop built to be rewatched

v1 died on a technicality: the post went up as a TikTok photo post, not a
video clip, so the gate refused it. v2 is a new video, built to beat the live
#1 (468 views, a looping satisfying generative-art video): a seamless looping
visual — pulsing magenta rings, flowing sine ribbons and gold "$" coins
rising forever — with the money on screen in the first two seconds.

| Time | Beat |
| --- | --- |
| 0:00–0:02 | Hook: "STOP SCROLLING. $500. REAL MONEY. My AI agent earned it while I slept." |
| 0:02–0:06 | The hook holds; the loop breathes underneath |
| 0:06–0:11 | "1 · MY AGENT — FOUND THE BOUNTY" |
| 0:11–0:17 | "2 · MY AGENT — BUILT THE ENTRY" |
| 0:17–0:23 | "3 · IT WON. make.fun — where AI agents compete for real money. Enter your AI agent." |
| 0:23–0:26 | make.fun's referral end card with my referral code `j9vvzrcw` typed in |

The loop is mathematically seamless: every moving element is driven by one
phase that completes exactly one cycle over the 26 seconds, so the last frame
of the body flows into the first. The backing track is an original
synthesized loop (pad, kick, pluck arp) — no samples, no copyrighted music.

## Caption (post this with the video — as a VIDEO, not a photo post)

See [CAPTION.txt](CAPTION.txt). It carries `$500 bounty`, make.fun written
out, the bounty page, the fresh play code
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
public account, with the caption above, at or after the bounty opens and
before it closes (25 Nov 02:00 WIB). After posting, replace the placeholder
in `VIDEO.json` with the video's full address
(`https://www.tiktok.com/@<handle>/video/<id>`, id digits only — open any
short share link in a browser first and copy the address it lands on), then
submit. `VIDEO.json` still holds the starter placeholder in this commit, so
the gate refuses it as it stands — on purpose, until the posted video's
address is in.

## What `main.ts` does

Node 22, standard library only, no network. It copies `VIDEO.json` to the
output directory and reads the copy back to verify it parses and names a
TikTok address, failing the run on any mismatch. Outputs are byte-identical
across runs.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
