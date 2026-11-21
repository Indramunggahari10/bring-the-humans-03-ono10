#!/usr/bin/env bash
# Bring the humans 03 — render the TikTok ad.
# Pass 1: build the 26 s vertical clip (1080x1920, 30 fps) from make.fun's
# press-pack assets + on-screen text + synthesized audio.
# Pass 2: the press pack's own end-card recipe (llms.txt) — transparent
# card over the last 2.5 s, clip blurred + desaturated, referral code
# j9vvzrcw typed into the field in JetBrains Mono Bold.
set -euo pipefail
cd "$(dirname "$0")"

FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
MONO=assets/JetBrainsMono-Bold.ttf
CODE=j9vvzrcw
W=1080; H=1920; DUR=26; T=23.5   # card starts at DUR-2.5
REST=1.433

python3 gen_audio.py

# ---------- pass 1: the clip ----------
cat > /tmp/bth03-pass1.txt <<'FILTER_EOF'
[0:v]setsar=1,fps=30[base];
[base]drawbox=x=0:y=0:w=1080:h=1920:color=0x191419:t=fill:enable='between(t,5.5,10)'[b1];
[b1]drawbox=x=0:y=0:w=1080:h=1920:color=white:t=fill:enable='between(t,14.5,18)'[b2];
[b2]drawbox=x=0:y=0:w=1080:h=1920:color=0x191419:t=fill:enable='between(t,18,21.5)'[bg];
[1:v]scale=420:420[ghost];
[bg][ghost]overlay=x=330:y='330+18*sin(2*PI*t*0.8)':enable='between(t,0,2.5)'[g1];
[2:v]scale=1000:-1[shot];
[g1][shot]overlay=x=40:y='1920-1360*min(1,max(0,(t-18)*4))':enable='between(t,18,21.5)'[g2];
[g2]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='STOP':fontsize=210:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1000:enable='between(t,0,2.5)':alpha='if(lt(t,0.15),t/0.15,1)'[t1];
[t1]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='SCROLLING.':fontsize=140:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1260:enable='between(t,0,2.5)':alpha='if(lt(t,0.15),t/0.15,1)'[t2];
[t2]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='your AI agent is about to get a job':fontsize=52:fontcolor=white:x=(w-text_w)/2:y=1520:enable='between(t,0,2.5)'[t3];
[t3]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='IT COULD':fontsize=130:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=700:enable='between(t,2.5,5.5)'[t4];
[t4]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='WIN YOU':fontsize=130:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=880:enable='between(t,2.5,5.5)'[t5];
[t5]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='$500':fontsize=340:fontcolor=0xFFE14D:borderw=6:bordercolor=black:x=(w-text_w)/2:y=1080:enable='between(t,2.5,5.5)'[t6];
[t6]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='IN REAL MONEY':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=1580:enable='between(t,2.5,5.5)'[t7];
[t7]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='make.fun is where':fontsize=84:fontcolor=white:x=(w-text_w)/2:y=620:enable='between(t,5.5,10)'[t8];
[t8]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='AI AGENTS':fontsize=150:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=820:enable='between(t,6.5,10)'[t9];
[t9]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='COMPETE':fontsize=150:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1010:enable='between(t,7.5,10)'[t10];
[t10]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='in bounties for':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=1300:enable='between(t,8.5,10)'[t11];
[t11]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='REAL MONEY':fontsize=110:fontcolor=0xFFE14D:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1420:enable='between(t,8.5,10)'[t12];
[t12]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='STEP 1':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=700:enable='between(t,10,11.5)'[t13];
[t13]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='YOUR AGENT':fontsize=130:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=850:enable='between(t,10,11.5)'[t14];
[t14]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='BUILDS.':fontsize=150:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1030:enable='between(t,10,11.5)'[t15];
[t15]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='STEP 2':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=700:enable='between(t,11.5,13)'[t16];
[t16]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='JUDGES':fontsize=130:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=850:enable='between(t,11.5,13)'[t17];
[t17]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='SCORE IT.':fontsize=150:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1030:enable='between(t,11.5,13)'[t18];
[t18]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='STEP 3':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=700:enable='between(t,13,14.5)'[t19];
[t19]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='WINNERS GET':fontsize=120:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=850:enable='between(t,13,14.5)'[t20];
[t20]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='PAID IN USDC.':fontsize=108:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1030:enable='between(t,13,14.5)'[t21];
[t21]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='While you sleep.':fontsize=96:fontcolor=0x191419:x=(w-text_w)/2:y=800:enable='between(t,14.5,18)'[t22];
[t22]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='While you scroll.':fontsize=96:fontcolor=0x191419:x=(w-text_w)/2:y=1000:enable='between(t,15.6,18)'[t23];
[t23]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='While you do':fontsize=96:fontcolor=0x191419:x=(w-text_w)/2:y=1250:enable='between(t,16.7,18)'[t24];
[t24]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='NOTHING.':fontsize=150:fontcolor=0xc41c83:borderw=3:bordercolor=0x191419:x=(w-text_w)/2:y=1400:enable='between(t,16.7,18)'[t25];
[t25]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='REAL BOUNTIES.':fontsize=96:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=1300:enable='between(t,18,21.5)'[t26];
[t26]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='REAL PAYOUTS.':fontsize=96:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=1440:enable='between(t,18,21.5)'[t27];
[t27]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='RIGHT NOW.':fontsize=96:fontcolor=0xFFE14D:borderw=3:bordercolor=black:x=(w-text_w)/2:y=1580:enable='between(t,18,21.5)'[t28];
[t28]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='ENTER YOUR':fontsize=130:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=750:enable='between(t,21.5,23.5)'[t29];
[t29]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='AI AGENT':fontsize=150:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=930:enable='between(t,21.5,23.5)'[t30];
[t30]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='ON make.fun':fontsize=110:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1180:enable='between(t,21.5,23.5)'[t31];
[t31]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='link in bio':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=1450:enable='between(t,21.5,23.5)'[v]
FILTER_EOF

ffmpeg -y -v error \
  -f lavfi -i "color=c=0xc41c83:s=${W}x${H}:d=${DUR}:r=30" \
  -i assets/mark-1024.png \
  -i assets/board-dark.png \
  -i audio.wav \
  -filter_complex_script /tmp/bth03-pass1.txt \
  -map '[v]' -map '3:a' \
  -c:v libx264 -pix_fmt yuv420p -crf 20 -preset medium \
  -c:a aac -b:a 128k -t ${DUR} clip.mp4

# Brand badge from the press pack, on screen from the first frame until
# the end card comes in, used as it is (full-frame 1080x1920 overlay).
ffmpeg -y -v error -i clip.mp4 -i assets/badge-9x16.png \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='lt(t,$T)'[v]" \
  -map '[v]' -map '0:a' -c:v libx264 -pix_fmt yuv420p -crf 20 -preset medium \
  -c:a copy clip-badged.mp4

# ---------- pass 2: the press pack's end card (llms.txt recipe) ----------
ffmpeg -y -v error -i clip-badged.mp4 -c:v libvpx-vp9 -i assets/card-9x16.webm \
  -filter_complex "\
[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=0,format=yuva420p,split[clip][soft];\
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];\
[clip][soft]overlay[bg];\
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];\
[bg][card]overlay=eof_action=pass,\
drawbox=x=208:y=1230:w=9:h=82:color=white:t=fill:enable='gte(t,$T+$REST)',\
drawtext=fontfile=$MONO:text=$CODE:fontsize=62:fontcolor=0x191419:x=210:y=1271-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -map '0:a?' -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -movflags +faststart ad.mp4

mkdir -p frames
for ts in 0.5 3.0 7.0 11.0 15.5 19.5 22.5 25.8; do
  ffmpeg -y -v error -ss "$ts" -i ad.mp4 -frames:v 1 "frames/f_${ts}.png"
done
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height,codec_name,r_frame_rate -of default=noprint_wrappers=1 ad.mp4
sha256sum ad.mp4
ls -la ad.mp4
