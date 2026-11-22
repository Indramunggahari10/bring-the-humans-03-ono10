// bring-the-humans-03 entry (Node 22, standard library only).
//
// The entry is the video itself: ad.mp4, posted publicly on TikTok, and
// VIDEO.json naming it. This program copies VIDEO.json from the repository
// root to the output directory, where the gate reads it, then reads the copy
// back and checks it parses and names a TikTok video address (or the starter
// placeholder, which the gate refuses as it stands — on purpose, until the
// posted video's address is in).
//
// No network, no wall clock, no files outside the repository. Two runs write
// the same bytes.
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
const src = join(BOT_DIR, 'VIDEO.json');
const dst = join(OUTPUT_DIR, 'VIDEO.json');
try {
  copyFileSync(src, dst);
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

// Self-check: read the copy back and verify its shape.
let parsed: unknown;
try {
  parsed = JSON.parse(readFileSync(dst, 'utf8'));
} catch (err) {
  console.error(`VIDEO.json in ${OUTPUT_DIR} is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}
const url = (parsed as { url?: unknown }).url;
if (typeof url !== 'string' || !/^https:\/\/(www\.|m\.)?tiktok\.com\//.test(url)) {
  console.error(`VIDEO.json url is not a TikTok address: ${String(url)}`);
  process.exit(1);
}
