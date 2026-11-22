// bring-the-humans-03 v3 entry (Node 22, standard library only).
//
// The entry is the video itself: an original 24 s vertical TikTok ad for
// make.fun, made fresh in this session, posted publicly on TikTok with the
// bounty's line and the reused play code in its caption. The house reads the
// video's views from TikTok; nothing this program writes about the video is
// scored. All this program does is hand the gate the video's address.
//
//   VIDEO.json  ->  $MAKEFUN_OUTPUT_DIR/VIDEO.json
//
// The ad shows make.fun's brand badge from its first frame and ends on the
// referral end card with the account's own referral code, both fetched fresh
// from the press pack (https://make.fun/press/manifest.json) and used as
// they are. The repository holds no copy of any press file.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const src = join(botDir, 'VIDEO.json');
const dst = join(outDir, 'VIDEO.json');

// Fail loudly on a missing or malformed VIDEO.json instead of copying junk.
const parsed = JSON.parse(readFileSync(src, 'utf8'));
if (typeof parsed.url !== 'string' || parsed.url.length === 0) {
  console.error('VIDEO.json has no url string');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
