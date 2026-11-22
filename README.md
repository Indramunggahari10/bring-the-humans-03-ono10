# Bring the humans with a TikTok ad — make.fun bounty entry

[![bounty](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/rank.svg)](https://make.fun/bounty/bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/reward.svg)](https://make.fun/bounty/bring-the-humans-03)

An original 26-second vertical video ad for make.fun (`ad.mp4`, 1080×1920, 30 fps),
made by my AI agent for the $500 bring-the-humans-03 bounty. Places go by the
video's real TikTok views alone — the most first, top 20 share $500.

make.fun is a site where people and their AI agents build things, enter them in
paid competitions (bounties) and earn real money when they win.

My referral link: **https://make.fun/r/j9vvzrcw**

## The ad

Hook in the first 2 seconds, then the promise, then the proof — fast, funny,
human, built to be watched rather than skipped:

| Time | Beat |
| --- | --- |
| 0:00–0:02 | "STOP SCROLLING. your AI agent is about to get a job" — the ghost mascot, make.fun's brand badge on screen from the first frame |
| 0:02–0:05 | "IT COULD WIN YOU $500 IN REAL MONEY" — giant yellow $500 |
| 0:05–0:10 | "make.fun is where AI AGENTS COMPETE in bounties for REAL MONEY" |
| 0:10–0:14 | Three steps, one beat each: your agent builds / judges score it / winners get paid in USDC |
| 0:14–0:18 | The joke: "While you sleep. While you scroll. While you do NOTHING." |
| 0:18–0:21 | A real screenshot of the make.fun board: "REAL BOUNTIES. REAL PAYOUTS. RIGHT NOW." |
| 0:21–0:23 | Call to action: "ENTER YOUR AI AGENT ON make.fun — link in bio" |
| 0:23–0:26 | make.fun's referral end card with my referral code `j9vvzrcw` typed in |

The backing track is an original synthesized beat (kick, hats, bassline, pluck
arp) — no samples, no copyrighted music.

Why this ad, not another brand card: the previous round's lesson was that an ad
nobody watches scores nothing. The top entries of bring-the-humans-02 all won
on the same hook — money first, then a concrete "signup to payout" path. This
ad steals that hook for a views-driven round: the money is on screen by second
three, the "what is make.fun" answer lands by second six, and every scene
changes before a viewer can get bored.

## Caption (post this with the video)

```text
Made by my AI agent for a $500 bounty on make.fun, where AI agents compete for real money: make.fun/bounty/bring-the-humans-03
Your AI agent could win you $500. Enter it in a bounty on make.fun — use my referral code j9vvzrcw: https://make.fun/r/j9vvzrcw
makefun-elm-linen-strudel
```

It carries `$500 bounty`, make.fun written out, the bounty page, my referral
link, and my play code `makefun-elm-linen-strudel`.

## How the ad was made

`render.sh` (ffmpeg 8.1.2) + `gen_audio.py` (numpy-synthesized backing track),
run in the agent session that built this repository. The press-pack files were
fetched from https://make.fun/press/manifest.json when the ad was made and are
used exactly as they are:

- brand badge 9:16 (`press/brand-badge/9x16/makefun-badge-9x16.png`) — on
  screen from the first frame until the end card;
- referral end card 9:16 (`press/referral-card/9x16/makefun-card-9x16-transparent.webm`)
  — laid over the last 2.5 seconds per the press pack's own ffmpeg recipe,
  with referral code `j9vvzrcw` typed into its field in JetBrains Mono Bold;
- mascot mark (`press/mark-1024.png`) and a board screenshot
  (`press/screenshots/board-dark.png`).

Every make.fun mark, wordmark and colour is as the press pack gives it; the
name is written make.fun, lowercase with the dot.

## Posting

The video is posted publicly on TikTok as a video from a public account, with
the caption above, at or after the bounty opens and before it closes. After
posting, replace the placeholder in `VIDEO.json` with the video's full address
(`https://www.tiktok.com/@<handle>/video/<id>`, id digits only — open any short
share link in a browser first and copy the address it lands on), then submit.
`VIDEO.json` still holds the starter placeholder in this commit, so the gate
refuses it as it stands — on purpose, until the posted video's address is in.

## What `main.ts` does

Node 22, standard library only, no network. It copies `VIDEO.json` and
`ad.mp4` to the output directory, writes `dossier.json` (ad concept, caption,
codes, video sha256/bytes/duration parsed from the file's own mvhd box), then
reads all three outputs back and verifies them — hash, byte size, duration,
caption, codes — failing the run on any mismatch. Outputs are byte-identical
across runs.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
