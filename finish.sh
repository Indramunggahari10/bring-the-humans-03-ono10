#!/usr/bin/env bash
# bring-the-humans-03 v3 — finish: frames + audio -> clip -> badge + end card -> ad.mp4
# Run from the v3 workdir. Uses the fresh press-pack files in press/.
set -euo pipefail
cd "$(dirname "$0")"

CODE=j9vvzrcw
FONT=fonts/JetBrainsMono-Bold.ttf
BADGE=press/badge-9x16.png
CARD=press/card-9x16-transparent.webm
LEN=2.5        # card over the last 2.5 s
REST=1.433     # card rests 1.433 s in
CX=210 CY=1232 CW=5 CH=78 MID=1271 SIZE=62
W=1080 H=1920

# 1. frames -> video-only body (deterministic: single thread, pinned timestamps)
ffmpeg -y -v error -framerate 30 -i frames/f%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -threads 1 \
  -metadata creation_time="2026-11-22T04:00:00Z" clip_body.mp4

# 2. mux the synth audio bed
ffmpeg -y -v error -i clip_body.mp4 -i audio.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest \
  -metadata creation_time="2026-11-22T04:00:00Z" clip.mp4

# 3. badge from frame 0 until the end card + referral end card (press recipe)
# The badge PNG is a single frame: loop it so it stays up until T.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp4)
T=$(awk "BEGIN{print $D-$LEN}")
ffmpeg -y -v error -i clip.mp4 -loop 1 -t "$T" -i "$BADGE" -c:v libvpx-vp9 -i "$CARD" -filter_complex "\
[0:v]format=yuva420p,split[clip][soft];\
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];\
[clip][soft]overlay[bg];\
[1:v]format=rgba[badge];\
[bg][badge]overlay=eof_action=pass:enable='lt(t,$T)'[bg2];\
[2:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];\
[bg2][card]overlay=eof_action=pass,\
drawbox=x=$CX-2:y=$CY-2:w=$CW+4:h=$CH+4:color=white:t=fill:enable='gte(t,$T+$REST)',\
drawtext=fontfile=$FONT:text=$CODE:fontsize=$SIZE:fontcolor=0x191419:x=$CX:y=$MID-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -map '0:a' -c:v libx264 -pix_fmt yuv420p -crf 18 -threads 1 \
  -c:a aac -b:a 160k -movflags +faststart \
  -metadata creation_time="2026-11-22T04:00:00Z" ad.mp4

ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -show_entries format=duration -of default=noprint_wrappers=1 ad.mp4
sha256sum ad.mp4
echo "finish OK: T=$T D=$D"
