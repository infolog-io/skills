// export-pdf.js — protocol for emitting final.pdf via preview_eval +
// browser print-to-PDF.
//
// Invocation contract:
//   1. Composer ensures final.html has print-friendly CSS @media print
//      block — body padding 0, no fixed elements, default page size.
//   2. preview_eval runs: window.print() — but this opens a dialog in
//      regular Chromium, not Claude Preview's headless mode.
//   3. Claude Preview exposes Page.printToPDF via the Chrome DevTools
//      Protocol when running in headless mode. The composer's SKILL.md
//      operating mode declares: if printToPDF is available, use it; else
//      mark PDF export as "manual: open final.html in a browser and print
//      to PDF" and continue.
//   4. Save returned PDF bytes to <session-dir>/final.pdf.
//
// At v1.0, PDF export is best-effort. If Claude Preview doesn't expose
// printToPDF, the composer emits a one-line note in the audit summary:
// "PDF export skipped — printToPDF unavailable in this Claude Preview build."

export const PDF_EXPORT_CONTRACT = {
  format: 'pdf',
  filename: 'final.pdf',
  best_effort: true,
  print_css_requirement: `@media print {
    body { padding: 0; }
    #__composer_hud { display: none; }
  }`
};
