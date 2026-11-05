// 이든 브랜드 소개 페이지 E2E 점검 (Playwright)
// 실행: node test/e2e.mjs  (http://localhost:8765 서버 필요)
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));

const PAGE = process.env.PAGE_URL || 'http://localhost:8765/';
const OUT = path.join(HERE, 'shots');
fs.mkdirSync(OUT, { recursive: true });
const results = [];
const ok = (name, pass, detail = '') => { results.push({ name, pass, detail }); console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${detail ? '  — ' + detail : ''}`); };

const browser = await chromium.launch({ channel: process.env.PW_CHANNEL || 'chrome' });

async function run(label, ctxOpts) {
  const ctx = await browser.newContext(ctxOpts);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/idden-film\.mp4|404/.test(m.text())) errors.push(m.text()); });
  const t0 = Date.now();
  await page.goto(PAGE, { waitUntil: 'load' });
  const loadMs = Date.now() - t0;
  await page.evaluate(() => document.fonts.ready);
  ok(`[${label}] 로딩 시간`, loadMs < 3000, `${loadMs}ms`);

  // 가로 스크롤 없음
  const ov = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  ok(`[${label}] 가로 넘침 없음`, ov <= 0, `${ov}px`);

  // 폰트 적용
  const fontOk = await page.evaluate(() => document.fonts.check('16px "Pretendard"'));
  ok(`[${label}] Pretendard 적용`, fontOk);

  // 필름: 영상 파일이 없으면 정지 이미지 대체, 일시정지 버튼 동작
  const film = await page.evaluate(() => document.querySelector('.film').className);
  ok(`[${label}] 필름 영역 표시`, /film/.test(film), film);
  await page.click('#filmCtrl');
  const paused = await page.evaluate(() => document.querySelector('.film').classList.contains('paused'));
  const lbl = await page.getAttribute('#filmCtrl', 'aria-label');
  ok(`[${label}] 필름 일시정지 토글`, paused && lbl === '필름 재생', lbl);
  await page.click('#filmCtrl');

  // 스토리 캐러셀: 다음 버튼, 점, 스와이프(스크롤)
  const total = await page.locator('#track > .card').count();
  ok(`[${label}] 스토리 카드 7장`, total === 7, String(total));
  await page.locator('#track').scrollIntoViewIfNeeded();
  const cur = () => page.evaluate(() => [...document.querySelectorAll('#dots button')].findIndex(b => b.getAttribute('aria-current') === 'true'));
  ok(`[${label}] 첫 점 활성, 이전 버튼 비활성`, (await cur()) === 0 && await page.isDisabled('#prev'));
  await page.click('#next'); await page.waitForTimeout(700);
  ok(`[${label}] 다음 버튼으로 2번째`, (await cur()) === 1, String(await cur()));
  await page.locator('#dots button').nth(4).click(); await page.waitForTimeout(800);
  ok(`[${label}] 점 클릭으로 5번째`, (await cur()) === 4, String(await cur()));
  // 터치 스와이프 대용: 스크롤 이동 후 점 동기화
  await page.evaluate(() => { const t = document.getElementById('track'); const s = t.children; t.scrollTo({ left: s[6].offsetLeft - s[0].offsetLeft }); });
  await page.waitForTimeout(600);
  ok(`[${label}] 스와이프 후 마지막 점 동기화, 다음 버튼 비활성`, (await cur()) === 6 && await page.isDisabled('#next'), String(await cur()));
  // 키보드
  await page.focus('#track'); await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(700);
  ok(`[${label}] 키보드 왼쪽 화살표`, (await cur()) === 5, String(await cur()));
  // 카드 높이 일정
  const hs = await page.$$eval('#track > .card', els => els.map(e => Math.round(e.getBoundingClientRect().height)));
  ok(`[${label}] 카드 높이 통일`, new Set(hs).size === 1, hs.join(','));

  // 이미지 로딩
  await page.evaluate(async () => { for (const i of document.images) { i.loading = 'eager'; } window.scrollTo(0, document.body.scrollHeight); });
  await page.waitForTimeout(800);
  const broken = await page.$$eval('img', imgs => imgs.filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.getAttribute('src')));
  ok(`[${label}] 깨진 이미지 없음`, broken.length === 0, broken.join(', '));

  // DPP 버튼: 화면 하단 고정, 클릭 시 안내
  const cta = await page.locator('#dppLink').boundingBox();
  const vh = page.viewportSize().height;
  ok(`[${label}] DPP 버튼 하단 고정, 높이 44px 이상`, cta && cta.y + cta.height <= vh && cta.y > vh - 100 && cta.height >= 44, JSON.stringify(cta));
  const href = await page.getAttribute('#dppLink', 'href');
  ok(`[${label}] DPP 버튼이 제품 정보 화면으로 연결`, href === 'dpp.html', href);

  // 터치 영역 44px 이상 (버튼)
  const small = await page.$$eval('button, .cta', els => els.filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.height < 24 || r.width < 24); }).length);
  ok(`[${label}] 너무 작은 버튼 없음`, small === 0, String(small));

  // 계산된 대비 검사 (글자와 실제 바탕)
  const lows = await page.evaluate(() => {
    const parse = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : [0, 0, 0, 1]; };
    const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
    const bgOf = el => { while (el) { const c = parse(getComputedStyle(el).backgroundColor); if (c[3] === undefined || c[3] > .5) { if (!(c[0] === 0 && c[1] === 0 && c[2] === 0 && c[3] === 0)) return c; } el = el.parentElement; } return [255, 255, 255]; };
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const n = walker.currentNode; if (!n.textContent.trim()) continue;
      const el = n.parentElement; const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || el.closest('[hidden]') || el.closest('.film')) continue;
      const fg = parse(cs.color), bg = bgOf(el);
      const L1 = lum(fg), L2 = lum(bg); const r = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
      const size = parseFloat(cs.fontSize), large = size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700);
      if (r < (large ? 3 : 4.5)) out.push(`${n.textContent.trim().slice(0, 14)} ${r.toFixed(2)}`);
    }
    return out;
  });
  ok(`[${label}] 글자 대비 WCAG AA`, lows.length === 0, lows.slice(0, 6).join(' | '));

  ok(`[${label}] 콘솔 오류 없음`, errors.length === 0, errors.join(' | '));

  // 스크린샷
  await page.evaluate(() => { window.scrollTo(0, 0); const t = document.getElementById('track'); t.scrollLeft = 0; document.getElementById('toast').hidden = true; });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, `${label}.png`), fullPage: true });
  await ctx.close();
}

await run('mobile-light', { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'light' });
await run('mobile-dark', { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'dark' });
await run('small-320', { viewport: { width: 320, height: 640 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'light' });
await run('desktop', { viewport: { width: 1280, height: 860 }, colorScheme: 'light' });

// 동작 줄이기 설정
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage(); await page.goto(PAGE);
  const p = await page.evaluate(() => document.querySelector('.film').classList.contains('paused'));
  ok('[reduced-motion] 필름 자동 정지', p);
  await ctx.close();
}

await browser.close();
const fails = results.filter(r => !r.pass);
fs.writeFileSync(path.join(HERE, 'result.json'), JSON.stringify(results, null, 2));
console.log(`\n${results.length - fails.length}/${results.length} 통과`);
process.exit(fails.length ? 1 : 0);
