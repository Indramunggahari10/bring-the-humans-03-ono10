#!/bin/bash
# Finish the v2 ad: assemble rendered frames + synth audio, then lay the
# press pack's brand badge (first frame until the end card) and referral
# end card (last 2.5 s, with the referral code typed in) over it, using the
# press pack's own ffmpeg recipe (press/llms.txt).
#
# Inputs (all produced/fetched in the build session, NOT in this repo):
#   frames/%04d.png  — from render.py (780 frames, 1080x1920, 30 fps)
#   audio.wav         — from gen_audio.py (26 s synth loop)
#   press/makefun-badge-9x16.png
#       — https://make.fun/press/brand-badge/9x16/makefun-badge-9x16.png
#   press/makefun-card-9x16-transparent.webm
#       — https://make.fun/press/referral-card/9x16/makefun-card-9x16-transparent.webm
#   fonts/JetBrainsMono-Bold.ttf — for the referral code field
# Output: ad.mp4 (1080x1920, 26 s, H.264 + AAC)
#
# Single-threaded x264 + pinned creation_time make the output
# byte-identical across runs (verified: two runs, same sha256).
set -e
cd "$(dirname "$0")/.."

CODE=j9vvzrcw
FONT=fonts/JetBrainsMono-Bold.ttf
W=1080 H=1920
CARD=press/makefun-card-9x16-transparent.webm
BADGE=press/makefun-badge-9x16.png
LEN=2.5 REST=1.433 CX=210 CY=1232 CW=5 CH=78 MID=1271 SIZE=62

ffmpeg -y -v error -framerate 30 -i frames/%04d.png -i audio.wav \
  -c:v libx264 -threads 1 -crf 18 -pix_fmt yuv420p -c:a aac -shortest \
  -metadata creation_time="2026-11-22T04:00:00Z" clip.mp4

D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp4)
T=$(awk "BEGIN{print $D-$LEN}")

ffmpeg -y -v error -i clip.mp4 -c:v libvpx-vp9 -i "$CARD" -i "$BADGE" \
  -filter_complex "\
[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=0,format=yuva420p,split[clip][soft];\
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];\
[clip][soft]overlay[bg];\
[2:v]format=yuva420p[bdg];[bg][bdg]overlay=enable='lt(t,$T)'[bg2];\
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];\
[bg2][card]overlay=eof_action=pass,\
drawbox=x=$CX-2:y=$CY-2:w=$CW+4:h=$CH+4:color=white:t=fill:enable='gte(t,$T+$REST)',\
drawtext=fontfile=$FONT:text=$CODE:fontsize=$SIZE:fontcolor=0x191419:x=$CX:y=$MID-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -map '0:a' -c:v libx264 -threads 1 -pix_fmt yuv420p -crf 18 \
  -c:a aac -movflags +faststart \
  -metadata creation_time="2026-11-22T04:00:00Z" ad.mp4

ffprobe -v error -show_entries format=duration,size -of default=nw=1 ad.mp4
sha256sum ad.mp4
