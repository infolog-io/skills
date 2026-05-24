// export-png.js — protocol for emitting final.png from the composer.
//
// Invocation contract:
//   The composer, after stripping the HUD from final.html, calls:
//     1. preview_resize(width=1280, height=2400)   (tall, to fit page)
//     2. preview_screenshot()                       (returns image bytes)
//     3. Save returned bytes to <session-dir>/final.png
//
// This file documents the contract. The composer SKILL.md operating mode
// owns the actual invocation; no runtime JS is needed here.

export const PNG_EXPORT_CONTRACT = {
  width: 1280,
  height: 2400,
  format: 'png',
  filename: 'final.png'
};
