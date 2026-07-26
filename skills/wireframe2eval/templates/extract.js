/* Extraction expression for `agent-browser eval`. Run once per source page.
   Captures meaning-bearing content only: headings, CTA labels, real paragraphs.
   Nav chrome and boilerplate are structure, not content — keep them out. */
JSON.stringify({
  url: location.href,
  title: document.title,
  h1: [...document.querySelectorAll("h1")].map(e => e.innerText.trim()),
  headings: [...document.querySelectorAll("h2,h3")]
    .map(e => ({ t: e.tagName, x: e.innerText.trim() }))
    .filter(o => o.x),
  ctas: [...new Set(
    [...document.querySelectorAll("a[class*=button], button")]
      .map(e => e.innerText.trim()).filter(Boolean)
  )],
  paras: [...document.querySelectorAll("p")]
    .map(e => e.innerText.trim())
    .filter(t => t.length > 40)
})
