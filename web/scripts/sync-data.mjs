/**
 * sync-data.mjs
 * -------------
 * Copies KOTTU's training artifacts from ../output into the site.
 *
 * READ-ONLY with respect to the project: it only reads from output/ and
 * writes under web/. It never imports src/, never writes to output/,
 * models/ or data/. Runs automatically before `npm run build` and can be
 * run on demand with `npm run sync`.
 */

import { copyFileSync, mkdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";

const repoRoot = new URL("../../", import.meta.url);
const fromOutput = (p) => fileURLToPath(new URL("output/" + p, repoRoot));
const toWeb = (p) => fileURLToPath(new URL("web/" + p, repoRoot));

mkdirSync(toWeb("src/data"), { recursive: true });
mkdirSync(toWeb("public/plots"), { recursive: true });

const artifacts = [
  ["metrics/metrics.json", "src/data/metrics.json"],
  ["reports/classification_report.txt", "src/data/classification_report.txt"],
  ["plots/accuracy_curve.png", "public/plots/accuracy_curve.png"],
  ["plots/loss_curve.png", "public/plots/loss_curve.png"],
  ["plots/confusion_matrix.png", "public/plots/confusion_matrix.png"],
];

let copied = 0;
for (const [src, dest] of artifacts) {
  if (existsSync(fromOutput(src))) {
    copyFileSync(fromOutput(src), toWeb(dest));
    copied += 1;
    console.log("  synced  " + src);
  } else {
    console.warn("  missing " + src + "  (kept existing copy in web/src/data)");
  }
}

console.log(`\n${copied}/${artifacts.length} artifacts synced (read-only from output/).`);
