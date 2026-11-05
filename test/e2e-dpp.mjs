// 제품 정보(DPP) 화면 점검. 실행: node test/e2e-dpp.mjs (http://localhost:8765 서버 필요)
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const BASE = process.env.PAGE_URL || 'http://localhost:8765/';
const OUT = path.join(HERE, 'shots'); fs.mkdirSync(OUT, { recursive: true });
const IDS = ['hb03-fragrance-hillstate-50', 'hb03-fragrance-idden-30', 'hb03-lotion-hillstate', 'hb03-earthbar'];
const results = [];
const ok = (n, p, d = '') => { results.push({ n, p }); console.log(`${p ? 'PASS' : 'FAIL'}  ${n}${d ? '  — ' + d : ''}`); };

const browser = await chromium.launch({ channel: process.env.PW_CHANNEL || 'chrome' });
for (const vp of [{ w: 390, h: 844, tag: 'm' }, { w: 320, h: 640, tag: 's' }, { w: 1280, h: 860, tag: 'd' }]) {
  const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 2, colorScheme: vp.tag === 's' ? 'dark' : 'light' });
  const page = await ctx.newPage();
  const errs = []; page.on('pageerror', e => errs.push(e.message));

  // 선택 화면
  await page.goto(BASE + 'dpp.html');
  ok(`[${vp.tag}] 제품 ID 없으면 선택 화면 4개`, (await page.locator('.list li').count()) === 4);

  for (const id of IDS) {
    await page.goto(BASE + 'dpp.html#' + id);
    await page.waitForTimeout(150);
    await page.evaluate(async () => { for (const i of document.images) { i.loading = 'eager'; } window.scrollTo(0, document.body.scrollHeight); });
    await page.waitForTimeout(500);
    const r = await page.evaluate(() => ({
      h1: document.querySelector('h1')?.textContent,
      ov: document.documentElement.scrollWidth - innerWidth,
      broken: [...document.images].filter(i => !(i.complete && i.naturalWidth)).map(i => i.getAttribute('src')),
      font: document.fonts.check('16px "Pretendard"'),
      bg: getComputedStyle(document.body).backgroundColor,
      others: document.querySelectorAll('.others a').length,
    }));
    ok(`[${vp.tag}] ${id} 제목 표시`, !!r.h1, r.h1);
    ok(`[${vp.tag}] ${id} 가로 넘침 없음`, r.ov <= 0, String(r.ov));
    ok(`[${vp.tag}] ${id} 이미지 정상`, r.broken.length === 0, r.broken.join(','));
    ok(`[${vp.tag}] ${id} 글꼴, 흰 바탕`, r.font && r.bg === 'rgb(255, 255, 255)', r.bg);
    ok(`[${vp.tag}] ${id} 다른 제품 3개 링크`, r.others === 3);
    const lows = await page.evaluate(() => {
      const parse = c => (c.match(/[\d.]+/g) || [0, 0, 0, 1]).map(Number);
      const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
      const bgOf = el => { while (el) { const c = parse(getComputedStyle(el).backgroundColor); if (c.length < 4 || c[3] > .5) return c; el = el.parentElement; } return [255, 255, 255]; };
      const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement; const cs = getComputedStyle(el);
        if (cs.display === 'none' || el.closest('[hidden]')) continue;
        const L1 = lum(parse(cs.color)), L2 = lum(bgOf(el)); const ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
        const big = parseFloat(cs.fontSize) >= 24; if (ratio < (big ? 3 : 4.5)) out.push(n.textContent.trim().slice(0, 12) + ' ' + ratio.toFixed(2)); }
      return out; });
    ok(`[${vp.tag}] ${id} 글자 대비 AA`, lows.length === 0, lows.slice(0, 4).join(' | '));
    if (vp.tag === 'm') { await page.evaluate(() => scrollTo(0, 0)); await page.screenshot({ path: path.join(OUT, `dpp-${id}.png`), fullPage: true }); }
  }
  // 다른 제품 링크로 이동
  await page.goto(BASE + 'dpp.html#hb03-earthbar');
  await page.click('.others a >> nth=0');
  await page.waitForTimeout(200);
  ok(`[${vp.tag}] 다른 제품 링크 이동`, (await page.locator('h1').textContent()).length > 0 && page.url().includes('#hb03-'), page.url());
  // 브랜드 페이지 버튼 → 제품 정보
  await page.goto(BASE + '?pid=hb03-fragrance-hillstate-50');
  const href = await page.getAttribute('#dppLink', 'href');
  ok(`[${vp.tag}] QR 제품 ID가 버튼으로 전달`, href === 'dpp.html#hb03-fragrance-hillstate-50', href);
  await page.click('#dppLink'); await page.waitForTimeout(400);
  ok(`[${vp.tag}] 버튼 누르면 해당 제품 화면`, (await page.locator('h1').textContent()) === '이든 에이치 프레그런스', page.url());
  await page.click('.back'); await page.waitForTimeout(400);
  ok(`[${vp.tag}] 뒤로 가기 링크로 브랜드 페이지`, await page.locator('#track').count() === 1);
  // 복사 버튼
  await page.goto(BASE + 'dpp.html#hb03-lotion-hillstate');
  await page.click('#copyMail'); await page.waitForTimeout(200);
  ok(`[${vp.tag}] 메일 복사 안내 표시`, await page.isVisible('#toast'));
  ok(`[${vp.tag}] 스크립트 오류 없음`, errs.length === 0, errs.join(' | '));
  await ctx.close();
}
await browser.close();
const f = results.filter(r => !r.p).length;
console.log(`\n${results.length - f}/${results.length} 통과`);
process.exit(f ? 1 : 0);
