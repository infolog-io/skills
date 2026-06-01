// run-checks.mjs — headless mechanical validator for the spraypixel adapter.
//
//   node run-checks.mjs <html-file> <mechanical-checks.js>
//
// Renders the drafted HTML in a real Chromium at three viewports and runs
// component-composer's mechanical-checks.js `runInBrowser()` for every
// mechanical criterion. Emits ONE JSON object on stdout:
//
//   { ok: true, criteria: { <id>: 'pass'|'fail'|'n/a', ... },
//     failures: [ { id, viewport, evidence } ], viewports: {...} }
//   { ok: false, error: "<message>" }
//
// A criterion is 'fail' if it fails at ANY viewport, 'pass' if it ran and never
// failed, 'n/a' if no matching marks existed (vacuous). mechanical-checks.js is
// an ES module; we strip the `export ` keyword and inject the body as a classic
// in-page script so `runInBrowser` and its lexically-closed helpers (CHECKS,
// rgbToHex, …) are all defined in one page scope.

import { readFileSync } from "node:fs";
import { chromium } from "playwright";

const [, , htmlPath, checksPath] = process.argv;

const VIEWPORTS = [
  { label: "mobile", width: 375, height: 800 },
  { label: "tablet", width: 768, height: 1024 },
  { label: "desktop", width: 1280, height: 900 },
];
const CRITERIA = [
  "text_collision",
  "text_truncation",
  "contrast_failure",
  "font_size_too_small",
  "overflow",
  "responsive_break",
  "chartjunk_decorative_css",
  "hidden_mark",
  "token_compliance",
];

async function main() {
  const html = readFileSync(htmlPath, "utf8");
  const checksSrc = readFileSync(checksPath, "utf8").replace(/^export\s+/gm, "");

  const out = { ok: true, viewports: {}, criteria: {}, failures: [] };
  const browser = await chromium.launch({ headless: true });
  try {
    for (const vp of VIEWPORTS) {
      const page = await browser.newPage({
        viewport: { width: vp.width, height: vp.height },
      });
      try {
        await page.setContent(html, { waitUntil: "load", timeout: 15000 });
        await page.addScriptTag({ content: checksSrc });
        const results = [];
        for (const id of CRITERIA) {
          results.push(
            await page.evaluate(
              ([cid, label]) => runInBrowser(cid, label),
              [id, vp.label],
            ),
          );
        }
        out.viewports[vp.label] = results;
      } catch (e) {
        out.viewports[vp.label] = { error: String((e && e.message) || e) };
      } finally {
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }

  // Roll up across viewports: fail if it failed anywhere it ran mechanically.
  for (const id of CRITERIA) {
    let ran = false;
    let failed = false;
    let evidence = null;
    let vpFailed = null;
    for (const vp of VIEWPORTS) {
      const list = out.viewports[vp.label];
      if (!Array.isArray(list)) continue;
      const r = list.find((x) => x && x.id === id);
      if (!r || r._no_mechanical) continue;
      ran = true;
      if (r.result === "fail") {
        failed = true;
        evidence = r.evidence;
        vpFailed = vp.label;
      }
    }
    out.criteria[id] = !ran ? "n/a" : failed ? "fail" : "pass";
    if (failed) out.failures.push({ id, viewport: vpFailed, evidence });
  }

  process.stdout.write(JSON.stringify(out));
}

main().catch((e) => {
  process.stdout.write(
    JSON.stringify({ ok: false, error: String((e && e.message) || e) }),
  );
  process.exit(0);
});
