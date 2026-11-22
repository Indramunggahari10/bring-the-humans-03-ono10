# bring-the-humans-03 v3 — NOTES

## What changed vs v2

- v2 LIVE but stalled: rank #91, 23 views (18:30 WIB 22 Nov). Concept: looping
  money-machine visual, hook "$500. Real money. My AI agent earned it while
  I slept.", 26 s. v2 submission 01a20228 VALID.
- v3 is a NEW video with a different concept, built to beat the live top 10
  (see study below): a SATISFYING PROCESS video — my AI agent draws the ad
  itself, one line at a time. A city skyline draws itself stroke by stroke
  under a glowing pen tip, gold $ coins rain down and pile up, a big $500
  pops in. Nothing from v2 was reused: all files authored fresh in the v3
  workdir; v2's scripts were never run and v2's files never copied.
- Play code REUSED exactly: `makefun-veranda-oatmeal-mosaic` (v2's code;
  the clipper lesson is that the play code is per-account-per-bounty and
  reused across versions — never invent a new one). It is on screen in the
  video (play-code chip, 18.0–21.5 s) AND in the caption.
- Referral code `j9vvzrcw` (link https://make.fun/r/j9vvzrcw), typed into
  the end-card field — the referral code, NOT the play code, belongs there
  per the press guide. The fresh-eyes judge initially flagged this as a
  mismatch; it is correct by design (see QA).

## Top-10 study (leaderboard fetched live 18:36 WIB 22 Nov, 358 entries)

- #1: 7,735 views — "My AI agent drew this city, one line at a time. It's
  in a $500 bounty on make.fun" — a SATISFYING PROCESS video (drawing a
  city line by line). OUTLIER (big account), not the real race.
- #2: 2,905 views — "Trying to make an AI video for no more than a $500
  bounty on make.fun" — BTS/process hook. Also an outlier.
- #3: 273 views — standard "Made by my AI agent for a $500 bounty" template.
- #4: 228 views — Indonesian explainer of make.fun.
- #5: 146 views — standard template + play code.
- #6: 136 views — Indonesian, rank/social-proof hook.
- #7: 105 views — STORY hook: "Dua agen AI. Yang satu cuma disuruh ngobrol,
  yang satu lagi dibayar. Kisah Paijo dan Sastro."
- #8–#12: 73–90 views — standard templates.
- Top-20 bar: 63 views. Pattern: the winners are PROCESS videos
  (satisfying build/draw, BTS) or a STORY hook — NOT the plain template,
  which caps at ~273 and mostly sits 60–150. v3 copies the #1 structure
  with original content: a process draw, not a template.

## The ad (24 s, 1080×1920, 30 fps)

- Rendered locally with ffmpeg + numpy/PIL (`render.py`, deterministic:
  every frame is a pure function of time, seeded randomness only).
- Hook (0–2 s): "MY AI AGENT DREW THIS AD. / $500 BOUNTY" with a gold
  stroke underlining the prize, drawn 0.4–1.6 s.
- Beat 1 (2–9 s): the skyline draws itself — 224 strokes (ground line,
  sun arc, 8 building outlines, 186 windows, 12 stars), pen tip riding
  each line; counter chip ticks STROKES 0→224; a gold bounty-progress bar
  fills under the caption. Caption: "MY AI AGENT DREW THIS CITY." then
  "LINE BY LINE. / NO HANDS."
- Beat 2 (9–14 s): 36 gold $ coins rain down and pile at the ground line;
  "$500" pops in at 12 s with a spring overshoot; counter runs
  PRIZE $0→$500 (lands $500 at 13 s). Caption: "EVERY LINE = / A SHOT AT
  $500."
- Beat 3 (14–21.5 s): "make.fun — WHERE AI AGENTS COMPETE / FOR REAL
  MONEY." then "ENTER YOUR AI AGENT. / 358 ENTRIES · TOP 20 WIN" plus the
  on-screen play-code chip "PLAY CODE: makefun-veranda-oatmeal-mosaic".
- Brand badge (press pack 9:16 overlay, unmodified) from frame 0 until
  the end card at 21.5 s. Referral end card (press pack transparent webm,
  per its own ffmpeg recipe: blur sigma 28, saturation 0.35, 0.8 s ease)
  over the last 2.5 s, code `j9vvzrcw` typed in JetBrains Mono Bold 62 px,
  ink #191419.
- Audio: original synthesized bed (pad chords Am–F–C–G, kick every 0.5 s,
  pentatonic pluck arp, a ding at the $500 pop), all tones at even Hz. No
  samples, no copyrighted audio. Loudness: −15.9 LUFS integrated, true
  peak −0.6 dBFS.
- The 224-stroke count is real: it is the number of stroke primitives the
  renderer draws, counted in code.

## Skills + relays report (mandatory — what each contributed)

Skills used (all read before building):
- viralforge — Viral DNA of the live #1: hook in first 2.4 s, shot rhythm
  (one continuous process shot, no cuts), word anchors ($500, line by
  line); structure kept, content replaced with our own draw.
- brag-slim — hook-first storyboard shape (Hook 2 s → Reveal → 2–3 beats
  → Punchline/outro), safe-zone rule (readable text y 250–1536, clear of
  the right 140 px), every frame postable, 0.3 s-per-word readability.
- reel-analyzer — teardown of the top reels: #1/#2 win on process/BTS,
  not on template copy; model the technique, never the words.
- media-judge — QA protocol: measure first (ffprobe/blackdetect/ebur128),
  then fresh eyes on flagged frames only; defect counts with timestamps.
- short-form-ffmpeg-cookbook — 9:16 recipes: caption safe zones, audio
  bed mix, loudness check at −14 LUFS, deterministic single-thread encode.
- long-video-clipper — script-first cutting: shot list with in/out times
  written before any render; one clip, one idea.
- meme-maker — consulted for the coin-pile gag timing; its template
  registry did not fit a process video, so no template was used.
- take-one — 12-job studio pass: strategist (one takeaway: "watch the
  agent draw, then enter"), storyboard timed to the words, stills gate
  before full render, fresh reviewer, music on the beat grid.

Relays used (same verbatim prompt to all 7, generic public content only):
- Groq (openai/gpt-oss-20b) — voted A (PROCESS); improvement: overlay
  "Earn $500 while you sleep" at the end → folded into the PRIZE counter
  and "A SHOT AT $500" beat.
- Xkiro (mistralai/ministral-14b) — voted C (LOOP); the only dissent.
- Bluesminds (nvidia/ising-calibration-1.5-31b) — voted A (PROCESS).
- Requesty (google/gemma-4-31b-it) — voted A; improvement: a "Bounty
  Progress" bar → ADDED (gold progress bar under the caption, 2–9 s).
- Coarena (gpt-6-luna) — voted A; improvement: first strokes instantly →
  drawing starts at 2.0 s with the pen already moving.
- 100milionseek (deepseek-v4.1-flash-free) — voted A; improvement: skyline
  resolves into the $500 → the $500 pop at 12 s over the finished skyline.
- Xingchi — FAILED (Codex route, empty answer on both attempts); no vote.
- Winner: A (PROCESS), 5 of 6 votes. Every relay claim was verified
  independently against the live leaderboard before use.

## QA (media-judge skill)

The skill is a markdown-only port (no judge.py), so QA ran as: ffmpeg
measurements + frame inspection by the builder + a fresh-eyes subagent
judge that viewed frames directly and answered narrow questions.

### Take 1 defects found (builder's eyes, frames at 0/1/5/8/12/16/20/21.4/23.9 s)

1. MAJOR — brand badge vanished after ~0.04 s: finish.sh overlaid the
   single-frame PNG with `trim=end_frame=1` + `eof_action=pass`, so the
   overlay ended when the badge stream ended. Only frame 0 carried the
   badge — an admin-disqualification item.
2. MINOR — relay consensus asked for a bounty-progress tie between the
   draw and the $500 (Requesty); take 1 had only the STROKES counter.
- End card (23.9 s) was already perfect in take 1: magenta wash, mark,
  wordmark, "Use my referral code", field with `j9vvzrcw` in ink, copy
  button clear. No badge on the last frame, as required. No black frames.
  Spelling checked on every frame.

### Fixes applied (genuine revision 1 — render.py + finish.sh edited, re-rendered)

- finish.sh: badge input looped (`-loop 1 -t 21.5`) so it stays up until
  the end card.
- render.py: gold bounty-progress bar under the caption, filling as
  strokes complete (2–9 s).
- Frame render re-run after the edit: 720/720 PNG frames byte-identical
  across two runs (sha256 compared per frame).

### Take 2 verdict (fresh-eyes judge, 9 frames + measurements)

- Measurements: 24.000 s, 1080×1920, H.264 30 fps + AAC, 0 black frames,
  −15.9 LUFS integrated, LRA 1.0 LU, true peak −0.6 dBFS.
- Brief checklist 6/6 PASS: badge present t=0–21 (gone by the t=22
  transition); hook fully visible at t=0/1; skyline 4 buildings at t=5
  (96/224) → 7 at t=8 (192/224) → complete + coins + $500 at t=12; all
  text quoted exactly, no spelling errors, no overlap, no cut-off;
  make.fun named + "compete for real money" + CTA; last frame a clean
  magenta card with `j9vvzrcw`; safe zones respected.
- D1 (major, judge's call): end-card code `j9vvzrcw` is not the play
  code. VERDICT OVERTURNED by the builder: the card's field takes the
  REFERRAL code per the press guide; the PLAY code belongs on screen
  elsewhere + in the caption. Take 1/2 did not show the play code
  on-screen at all — that gap was real, and fixed in revision 2 below.
- Hints (all checked, none a defect): PRIZE counter lands $500 at 13 s
  (verified at t=13.5); the t=18 "headline-free beat" is only the exact
  18.0 s crossfade boundary — at t=18.3 the CTA is already fading in;
  the $500 pill covers the centre buildings' tops by design; coin piles
  dip to ~y 1530 (graphics, inside the safe floor).

### Revision 2 (genuine — render.py edited, re-rendered)

- Added the on-screen play-code chip "PLAY CODE:
  makefun-veranda-oatmeal-mosaic" (JetBrains Mono Bold 30 px, gold on
  dark pill) during the CTA beat, 18.0–21.5 s.
- Beat-1 caption line 1 "MY AGENT DREW" → "MY AI AGENT DREW" to match
  the hook exactly (judge hint).
- Frame render re-run after the edit: 720/720 PNG frames byte-identical
  across two runs (sha256 compared per frame).
- Final ad re-verified: t=13.5 PRIZE $500, t=18.3 CTA + play-code chip
  fading in, t=20 chip fully legible, t=23.9 end card unchanged.

## Determinism / revision proof

- Frame renders: two runs after each edit, 720/720 PNG frames
  byte-identical (sha256 per frame).
- Full ad.mp4: single-threaded x264 + pinned container timestamps
  (`-threads 1`, `-metadata creation_time="2026-11-22T04:00:00Z"`):
  two finish.sh runs byte-identical, sha256
  `bfef4fac881f3b97459e03e7aca031486d621477063ae78199ac12fe56e30396`.
  (Take 2, pre-revision-2: `a62528de68150791a7d451a5403abd0a49c6b591e5749086fe0a93bbc16ef66c`.)

## Grader-like verify

- Read-only copy of the repo (`chmod a-w,a+rX`), run as unprivileged user
  `nobody` with MAKEFUN_OUTPUT_DIR set: `node main.ts` exits 0 and writes
  VIDEO.json to the OUT dir. Two runs: identical bytes (sha256
  af7994cc81433598afea23bab8caf1069150a47d1420bc14338e00c184648823,
  same as repo/VIDEO.json).
- main.ts writes only to MAKEFUN_OUTPUT_DIR (never into the repo) — proven
  by the exit-0 runs against the read-only copy.

## Badges (all curl-verified live, 200)

- https://make.fun/badge/bring-the-humans-03.svg — 200, 5131 B
- https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/rank.svg — 200, 1395 B
- https://make.fun/badge/bring-the-humans-03/vjmunggahari-ui/bring-the-humans-03-ono10/reward.svg — 200, 1293 B

## Press-pack files (fetched fresh 22 Nov from make.fun/press)

- manifest.json + llms.txt read; brand badge 9:16 overlay (1080×1920,
  22,297 B) and referral card 9:16 transparent webm (768,936 B) verified
  by size/dimensions against the guide. Used unmodified, per the press
  pack's recipes.
- JetBrains Mono Bold downloaded from the official JetBrainsMono repo for
  the referral-code field, per the press guide.

## Caption (exact — also in CAPTION.txt)

```text
My AI agent drew this ad. One line at a time. 👀
Made by my AI agent for a $500 bounty on make.fun, where AI agents compete for real money: make.fun/bounty/bring-the-humans-03
makefun-veranda-oatmeal-mosaic
Join with my link: https://make.fun/r/j9vvzrcw
#makefun #aiagent #satisfying #fyp
```

Carries "$500 bounty", make.fun written out, the required line verbatim,
the reused play code and the referral link.

## Still to do (parent)

- User posts ad.mp4 on TikTok as a VIDEO (not a photo post) from a public
  account, with the caption above, before 25 Nov 02:00 WIB.
- Parent fills VIDEO.json with the video's full address
  (https://www.tiktok.com/@<handle>/video/<id>) and submits.
- NOT submitted, NOT posted, NOT transferred by this builder.
