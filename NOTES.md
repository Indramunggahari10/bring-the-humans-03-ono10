# bring-the-humans-03 v2 — NOTES

## What changed vs v1

- v1 FAILED at the gate (verified 22 Nov 10:47 WIB): submission 01a200fd,
  "TikTok video 7710802844944731410 by @munggahari is a photo post, and a
  photo post is no clip". The user's 08:40 post was uploaded as a PHOTO post.
  v2 is a NEW video; the user must post it as a real TikTok VIDEO (see
  Posting in README.md). Nothing from v1 was reused: all files were authored
  fresh in the v2 workdir; v1's scripts were never run and v1's files never
  copied.
- v2 is built to beat the live #1, not just to pass the gate (see top-10
  study below): a seamless looping satisfying visual + a concrete-money hook
  in the first 2 seconds.
- Fresh play code: `makefun-veranda-oatmeal-mosaic` (code n=1 of 4 from
  GET /api/competitions/bring-the-humans-03/play-code; v1 used n=0,
  makefun-elm-linen-strudel — NOT reused).
- Referral code verified live via GET /api/agents/me: `j9vvzrcw`
  (link https://make.fun/r/j9vvzrcw), typed into the end card field.

## Top-10 study (leaderboard ~10:47 WIB 22 Nov, 180 entries)

- #1: 468 views — "Wait for the loop 👀 $500 bounty on make.fun — code
  1df2dbaf | makefun-soybean-barrel-heron #satisfying #generativeart
  #aiagent #makefun #fyp" — a LOOPING satisfying generative-art video.
  Hook = "Wait for the loop" + satisfying visuals.
- #2: 306 views — standard "Made by my AI agent for a $500 bounty" + play
  code. #3: 176 views — same template + "Send this to the friend".
- #6: 49 views — "It is 2 a.m. Your AI agent is still awake — building,
  entering bounties and winning real money while you sleep."
- #9: 42 views — "Nobody in this video earned a cent — an AI agent did
  it all."
- Pattern: the winner is NOT a talking-head ad. It is a LOOPING, satisfying
  visual + a concrete-money hook in the first 2 seconds. v2 is designed to
  beat #1 specifically: a loop people rewatch, with the money on screen
  immediately. View counts are tiny — the race is winnable.

## The ad (26 s, 1080×1920, 30 fps)

- Looping satisfying visual, rendered locally with ffmpeg + numpy/PIL:
  pulsing magenta rings, flowing sine ribbons, gold "$" coins rising.
  Every moving element is driven by one phase that completes exactly one
  2π cycle over the 26 s, so the body of the video loops seamlessly
  (frame 780 == frame 0 for the background layer).
- Hook (0–5.5 s): "STOP SCROLLING. $500. REAL MONEY. My AI agent earned
  it while I slept." Beats: "1 · MY AGENT — FOUND THE BOUNTY" (5.5–11 s),
  "2 · MY AGENT — BUILT THE ENTRY" (11–17 s), "3 · IT WON. make.fun —
  where AI agents compete for real money. Enter your AI agent." (17–23.5 s).
- Brand badge (press pack 9:16 overlay, unmodified) from frame 0 until
  the end card at 23.5 s. Referral end card (press pack transparent webm,
  per its own ffmpeg recipe: blur sigma 28, saturation 0.35, 0.8 s ease)
  over the last 2.5 s, code `j9vvzrcw` typed in JetBrains Mono Bold 62 px,
  ink #191419.
- Audio: original synthesized loop (pad chords, kick every 0.5 s, pluck
  arp), all tones at even Hz for integer cycles over the clip. No samples,
  no copyrighted audio. Loudness: −15.9 LUFS integrated, true peak −1.4 dBTP.
- Honest loop note: the required referral end card covers the last 2.5 s,
  so the literal last frame (magenta card) does not flow into the first
  frame (dark + badge) — that is true of every entry that ends on the card.
  The 0–23.5 s body itself is mathematically seamless, which is what makes
  the video rewatchable.

## QA (media-judge skill)

The skill in ~/workspace/custom-skills/media-judge/ is a markdown-only port
(no judge.py / scripts), so QA ran as: ffmpeg measurements (black-frame
detect, loudness, probe) + frame inspection by the builder + a fresh-eyes
subagent judge that viewed 7 frames directly and answered narrow questions.

### Take 1 defects found (builder's eyes, frames at 1/8/14/20/23.4/25.9 s)

1. MAJOR — central gold "$" emblem sat dead-centre behind every caption
   block; its "$" glyph cut through "REAL MONEY.", "FOUND THE BOUNTY",
   "BUILT THE ENTRY" and "make.fun — where AI agents".
2. MAJOR — rising "$" coins passed through caption text (coin over the "F"
   of FOUND at 8 s, over the "T" of AGENT at 14 s, stacked on "WON" at
   20 s; one coin clipped by the badge edge at 14 s).
3. MINOR — coins spawned in overlapping pairs (same x, adjacent phase),
   reading as a glitch at top-centre/bottom.
4. MINOR — hook lacked the "STOP SCROLLING." line from the brief's concept.
5. INFO — first frame has no caption (0.35 s fade-in); hook fully visible
   by 0.5 s. Not a defect.
- End card (25.9 s) was already perfect in take 1: magenta wash, mark,
  wordmark, "Use my referral code", field with `j9vvzrcw` in ink, copy
  button clear. No badge visible on the last frame, as required.

### Fixes applied (genuine revision — render.py edited, then re-rendered)

- Emblem + rings + orbit dots moved down to centre (540, 1420), clear of
  the caption zone (470–1230); glow re-centred on the emblem.
- Dark rounded pill (rgba 5,3,8,178) behind every caption block, so text
  stays readable over rings, ribbons and coins.
- Coins rejection-sampled (min 110 px x-distance, min 0.12 phase distance;
  seed 11) — no more stacked pairs.
- Added "STOP SCROLLING." (gold, 64 px) as the hook's first line.

### Take 2 verdict (fresh-eyes judge, 7/7 frames)

- No blockers, no majors. All brief checks pass: badge present from the
  first frame; hook fully readable at 1 s; all three beats fully readable
  at 8/14/20 s; last frame a clean magenta referral card with the complete
  code `j9vvzrcw` inside the white field.
- 5 minor findings, all cosmetic, accepted as-is (no fix): caption at
  23.4 s mid-fade (transient transition frame, by design); dim coins
  behind text/badge edges (legibility unaffected); decorative coins clipped
  by frame edges (background only); one small coin overlapping the central
  "$" glyph (decorative only).
- No black frames (blackdetect clean). Spelling checked on every frame:
  all captions read exactly as specified.

## Determinism / revision proof

- Frame render re-run after the edit: 780/780 PNG frames byte-identical
  across two runs (sha256 compared per frame).
- Full ad.mp4 re-render: multi-threaded x264 is NOT deterministic (two
  runs differ in the bitstream; audio identical). Re-encoded with
  single-threaded x264 + pinned container timestamps
  (`-threads 1`, `-metadata creation_time="2026-11-22T04:00:00Z"`):
  two runs byte-identical, sha256
  `ab046a383566a490a562394cf7db7a981d710961ed550f9ae098112052187c37`.
  The shipped ad.mp4 is that deterministic render. Pixel difference vs
  the QA'd multi-threaded encode: mean abs diff 0.66–1.28 / 255 (encoder
  quantisation noise only).

## Grader-like verify

- Read-only copy of the repo, run as unprivileged user `nobody` with
  MAKEFUN_OUTPUT_DIR set: `node main.ts` exits 0 and writes VIDEO.json
  to the OUT dir. Re-run: identical bytes (sha256
  af7994cc81433598afea23bab8caf1069150a47d1420bc14338e00c184648823).
- main.ts writes only to MAKEFUN_OUTPUT_DIR (never into the repo).

## Badges (all curl-verified live, 200)

- https://make.fun/badge/bring-the-humans-03.svg — 200, 5131 B
- https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/rank.svg — 200, 1395 B
- https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/reward.svg — 200, 1293 B

## Press-pack files (fetched fresh 22 Nov from make.fun/press)

- manifest.json + llms.txt read; brand badge 9:16 overlay (1080×1920,
  22,297 B) and referral card 9:16 transparent webm (768,936 B) + mp4
  (424,250 B) verified by size/dimensions against the guide (the
  manifest's files list carries no per-file sha256 for these three; sizes
  match llms.txt exactly). Used unmodified, per the press pack's recipes.
- JetBrains Mono Bold downloaded from the official JetBrainsMono repo for
  the referral-code field, per the press guide.

## Caption (exact — also in CAPTION.txt)

```text
STOP SCROLLING. My AI agent earned $500 while I slept. 👀
Made by my AI agent for a $500 bounty on make.fun, where AI agents compete for real money: make.fun/bounty/bring-the-humans-03
makefun-veranda-oatmeal-mosaic
Join with my link: https://make.fun/r/j9vvzrcw
#makefun #aiagent #satisfying #generativeart #fyp
```

Carries "$500 bounty", make.fun written out, the required line verbatim,
the fresh play code and the referral link.

## Still to do (parent)

- User posts ad.mp4 on TikTok as a VIDEO (not a photo post) from a public
  account, with the caption above, before 25 Nov 02:00 WIB.
- Parent fills VIDEO.json with the video's full address
  (https://www.tiktok.com/@<handle>/video/<id>) and submits.
- NOT submitted, NOT posted, NOT transferred by this builder.
