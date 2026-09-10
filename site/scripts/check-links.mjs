// Post-build link check: every internal href/src in dist must resolve to a
// real file. Guards against broken nav links (e.g. a Starlight sidebar entry
// that got locale-prefixed into a 404) reaching production — the class of
// bug a build alone will never catch.
//
// Usage: node scripts/check-links.mjs [distDir]   (default: dist)

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const distDir = path.resolve(siteRoot, process.argv[2] ?? 'dist');

// URL base from astro.config (e.g. '/flowtest'): root-relative URLs in built
// HTML carry this prefix; on the filesystem (dist = site root) it is stripped.
const config = fs.readFileSync(path.join(siteRoot, 'astro.config.mjs'), 'utf8');
const base = (config.match(/base:\s*'([^']+)'/)?.[1] ?? '/').replace(/\/+$/, '');

const htmlFiles = [];
(function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.html')) htmlFiles.push(full);
  }
})(distDir);

if (htmlFiles.length === 0) {
  console.error(`check-links: no HTML files under ${distDir} — wrong dir?`);
  process.exit(2);
}

const EXTERNAL = /^(https?:|mailto:|data:|#)/;
const broken = [];

// Directories resolve via their index.html; extensionless routes via .html.
function resolvesTo(p) {
  if (fs.existsSync(p)) {
    if (fs.statSync(p).isFile()) return true;
    if (fs.existsSync(path.join(p, 'index.html'))) return true;
  }
  return fs.existsSync(p + '.html');
}

for (const file of htmlFiles) {
  const html = fs.readFileSync(file, 'utf8');
  for (const [, value] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    if (EXTERNAL.test(value)) continue;
    const clean = value.split('#')[0].split('?')[0];
    if (!clean) continue; // pure fragment link
    let resolved;
    if (clean.startsWith('/')) {
      if (!clean.startsWith(base + '/') && clean !== base) {
        broken.push({ file: path.relative(distDir, file), value, resolved: 'outside site base ' + base });
        continue;
      }
      resolved = path.join(distDir, clean.slice(base.length) || '/');
    } else {
      resolved = path.resolve(path.dirname(file), clean);
    }
    if (!resolvesTo(resolved)) {
      broken.push({ file: path.relative(distDir, file), value, resolved: path.relative(distDir, resolved) });
    }
  }
}

if (broken.length > 0) {
  console.error(`check-links: ${broken.length} broken internal link(s):`);
  for (const b of broken) console.error(`  ${b.file}: "${b.value}" → ${b.resolved} (missing)`);
  process.exit(1);
}

console.log(`check-links: ${htmlFiles.length} pages, all internal links resolve.`);
