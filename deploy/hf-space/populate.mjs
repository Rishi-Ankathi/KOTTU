/**
 * Copy everything the Space's Dockerfile needs into a Hugging Face Space
 * checkout. Run from the repo root:
 *
 *   node deploy/hf-space/populate.mjs  /path/to/kottu-api        (space checkout)
 *
 * Then, in that checkout:  git add -A && git commit -m "update" && git push
 *
 * This script only copies files. It never touches this repo's git.
 */

import { cpSync, copyFileSync, existsSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

const dest = process.argv[2];
if (!dest || !existsSync(dest)) {
  console.error(
    "usage: node deploy/hf-space/populate.mjs <path-to-space-checkout>"
  );
  process.exit(1);
}

const root = fileURLToPath(new URL("../../", import.meta.url)); // repo root
const tpl = resolve(root, "deploy/hf-space");

const noPyCache = (src) => !src.includes("__pycache__") && !src.endsWith(".pyc");

function vendorDir(rel) {
  const to = resolve(dest, rel);
  rmSync(to, { recursive: true, force: true });
  cpSync(resolve(root, rel), to, { recursive: true, filter: noPyCache });
  console.log("  vendored", rel + "/");
}

vendorDir("api");
vendorDir("src");
vendorDir("models");

copyFileSync(resolve(root, "api/requirements.txt"), resolve(dest, "requirements.txt"));
copyFileSync(resolve(tpl, "Dockerfile"), resolve(dest, "Dockerfile"));
copyFileSync(resolve(tpl, "README.md"), resolve(dest, "README.md"));
console.log("  copied   requirements.txt, Dockerfile, README.md");

console.log("\npopulated:", dest);
console.log("next:  cd", JSON.stringify(dest), "&& git add -A && git commit -m 'update' && git push");
