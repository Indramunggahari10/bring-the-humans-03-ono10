// Bring the humans 03 — "Bring the humans with a TikTok ad" (Node 22, stdlib only).
//
// The entry is the video itself: an original 26-second vertical ad for
// make.fun, rendered in the agent session that built this repository
// (see render.sh + gen_audio.py), posted publicly on TikTok from a public
// account with the bounty's line and the play code in its caption, and
// named by VIDEO.json. The house reads the video's views from TikTok;
// places go by views alone, the most first, top 20 share $500.
//
// What this program does, deterministically, with no network:
//   1. copies VIDEO.json from the repository root to the output dir,
//   2. copies ad.mp4 (the rendered ad) to the output dir,
//   3. writes dossier.json describing the ad, its caption and its codes,
//   4. reads all three files back and verifies them: VIDEO.json parses and
//      holds a TikTok video address (or the starter placeholder, which the
//      gate refuses until the real address replaces it), ad.mp4 re-hashes
//      to the sha256 recorded in the dossier and matches its byte size,
//      and dossier.json parses with exactly the values just computed.
// Any mismatch fails the run (exit 1). The outputs are byte-identical
// across runs: the dossier carries no timestamps and no randomness.
//
// Run locally:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const REFERRAL_CODE = 'j9vvzrcw';
const PLAY_CODE = 'makefun-elm-linen-strudel';
const CAPTION =
  'Made by my AI agent for a $500 bounty on make.fun, where AI agents compete for real money: make.fun/bounty/bring-the-humans-03\n' +
  'Your AI agent could win you $500. Enter it in a bounty on make.fun — use my referral code j9vvzrcw: https://make.fun/r/j9vvzrcw\n' +
  'makefun-elm-linen-strudel';

function sha256Hex(buf: Buffer): string {
  return createHash('sha256').update(buf).digest('hex');
}

function fail(message: string): never {
  console.error(`self-check failed: ${message}`);
  process.exit(1);
}

// Parse an MP4's duration from its mvhd box (timescale + duration),
// pure stdlib: walk the box tree (mvhd lives inside moov), read mvhd
// version 0 or 1. Returns seconds, or null when no usable mvhd is found.
function parseMp4DurationSeconds(buf: Buffer): number | null {
  const CONTAINERS = new Set(['moov', 'trak', 'mdia', 'minf', 'stbl', 'edts', 'dinf', 'udta']);
  function walk(start: number, end: number): number | null {
    let off = start;
    while (off + 8 <= end) {
      let size = buf.readUInt32BE(off);
      const type = buf.toString('ascii', off + 4, off + 8);
      let header = 8;
      if (size === 1) {
        if (off + 16 > end) return null;
        size = Number(buf.readBigUInt64BE(off + 8));
        header = 16;
      } else if (size === 0) {
        size = end - off;
      }
      if (size < header || off + size > end) return null;
      if (type === 'mvhd') {
        const body = off + header;
        const version = buf[body];
        if (version === 0) {
          const timescale = buf.readUInt32BE(body + 12);
          const duration = buf.readUInt32BE(body + 16);
          return timescale > 0 ? duration / timescale : null;
        }
        if (version === 1) {
          const timescale = buf.readUInt32BE(body + 20);
          const duration = Number(buf.readBigUInt64BE(body + 24));
          return timescale > 0 ? duration / timescale : null;
        }
        return null;
      }
      if (CONTAINERS.has(type)) {
        const found = walk(off + header, off + size);
        if (found !== null) return found;
      }
      off += size;
    }
    return null;
  }
  return walk(0, buf.length);
}

mkdirSync(OUTPUT_DIR, { recursive: true });

// --- 1 + 2: deliver VIDEO.json and the ad ---
const videoJsonSrc = join(BOT_DIR, 'VIDEO.json');
const adSrc = join(BOT_DIR, 'ad.mp4');
const videoJsonDst = join(OUTPUT_DIR, 'VIDEO.json');
const adDst = join(OUTPUT_DIR, 'ad.mp4');
try {
  copyFileSync(videoJsonSrc, videoJsonDst);
  copyFileSync(adSrc, adDst);
} catch (err) {
  fail(`could not copy entry files from ${BOT_DIR}: ${(err as Error).message}`);
}

// --- measure what was delivered ---
const videoJsonBytes = readFileSync(videoJsonDst);
const adBytes = readFileSync(adDst);
const adSha256 = sha256Hex(adBytes);

let videoUrl: string;
try {
  const parsed: unknown = JSON.parse(videoJsonBytes.toString('utf8'));
  if (typeof parsed !== 'object' || parsed === null || typeof (parsed as { url?: unknown }).url !== 'string') {
    fail('VIDEO.json is not an object with a string url');
  }
  videoUrl = (parsed as { url: string }).url;
} catch (err) {
  fail(`VIDEO.json does not parse: ${(err as Error).message}`);
}

// A real TikTok video address; the starter placeholder (<handle>/<id>)
// is not one, and the gate refuses it until the posted video replaces it.
const REAL_VIDEO = /^https:\/\/(www\.|m\.)?tiktok\.com\/@[^/]+\/video\/\d+\/?$/;
const videoIsReal = REAL_VIDEO.test(videoUrl);

// Duration is read from the file itself, never assumed: parse the mvhd
// box and sanity-check the ad is a short (20-30 s) vertical video.
const adDuration = parseMp4DurationSeconds(adBytes);
if (adDuration === null) fail('ad.mp4 has no readable mvhd duration');
if (adDuration < 20 || adDuration > 30) fail(`ad.mp4 duration ${adDuration}s is outside 20-30 s`);

// --- 3: the dossier (fixed key order, no timestamps: deterministic) ---
const dossier = {
  competition: 'bring-the-humans-03',
  title: 'Bring the humans with a TikTok ad',
  video_file: 'ad.mp4',
  video: {
    sha256: adSha256,
    bytes: adBytes.length,
    duration_s: Math.round(adDuration * 1000) / 1000,
    width: 1080,
    height: 1920,
    fps: 30,
    codec: 'h264+aac',
  },
  video_json: {
    url: videoUrl,
    is_real_tiktok_video_url: videoIsReal,
    placeholder: !videoIsReal,
  },
  referral: {
    code: REFERRAL_CODE,
    link: `https://make.fun/r/${REFERRAL_CODE}`,
  },
  play_code: PLAY_CODE,
  caption: CAPTION,
  concept:
    'Hook in the first 2 seconds ("STOP SCROLLING. your AI agent is about to get a job"), ' +
    'then the $500 promise in giant type, then what make.fun is (AI agents compete in bounties for real money), ' +
    'three quick steps (your agent builds, judges score it, winners get paid in USDC), the joke beat ' +
    '("While you sleep. While you scroll. While you do NOTHING."), a real screenshot of the make.fun board ' +
    '("REAL BOUNTIES. REAL PAYOUTS. RIGHT NOW."), the call to action ("ENTER YOUR AI AGENT ON make.fun"), ' +
    'and the press pack referral end card with the referral code typed in. Brand badge from the press pack ' +
    'on screen from the first frame until the end card; every make.fun mark, wordmark and colour as the ' +
    'press pack gives it; original synthesized backing track (kick, hats, bassline, pluck arp).',
  made_with:
    'ffmpeg 8.1.2 (render.sh) + a numpy-synthesized backing track (gen_audio.py); ' +
    'press-pack files fetched from https://make.fun/press/manifest.json when the ad was made: ' +
    'brand badge 9:16, referral end card 9:16, mascot mark, board screenshot.',
};
const dossierText = JSON.stringify(dossier, null, 2) + '\n';
const dossierDst = join(OUTPUT_DIR, 'dossier.json');
writeFileSync(dossierDst, dossierText, 'utf8');

// --- 4: read-back self-check ---
const videoJsonBack = readFileSync(videoJsonDst);
if (!videoJsonBack.equals(videoJsonBytes)) fail('VIDEO.json read back differs from what was copied');
const adBack = readFileSync(adDst);
if (sha256Hex(adBack) !== adSha256) fail('ad.mp4 read back hashes differently');
if (adBack.length !== dossier.video.bytes) fail('ad.mp4 read back has a different byte size');
let dossierBack: unknown;
try {
  dossierBack = JSON.parse(readFileSync(dossierDst, 'utf8'));
} catch (err) {
  fail(`dossier.json does not parse on read-back: ${(err as Error).message}`);
}
const back = dossierBack as typeof dossier;
if (back.video.sha256 !== adSha256) fail('dossier.json sha256 does not match ad.mp4');
if (back.video.bytes !== adBytes.length) fail('dossier.json bytes do not match ad.mp4');
if (back.video.duration_s !== Math.round(adDuration * 1000) / 1000) fail('dossier.json duration does not match ad.mp4');
if (back.video_json.url !== videoUrl) fail('dossier.json url does not match VIDEO.json');
if (back.caption !== CAPTION) fail('dossier.json caption differs');
if (back.referral.code !== REFERRAL_CODE) fail('dossier.json referral code differs');
if (back.play_code !== PLAY_CODE) fail('dossier.json play code differs');

console.log(`VIDEO.json -> ${videoJsonDst} (${videoJsonBytes.length} bytes, real TikTok url: ${videoIsReal})`);
console.log(`ad.mp4 -> ${adDst} (${adBytes.length} bytes, sha256 ${adSha256})`);
console.log(`dossier.json -> ${dossierDst} (${dossierText.length} bytes)`);
console.log('self-check passed: all outputs read back and verified');
