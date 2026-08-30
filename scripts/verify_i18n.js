const fs = require('node:fs');

const html = fs.readFileSync('index.html', 'utf8');

// Verify all required IDs and classes exist in index.html
const requiredIds = [
  'btnLangId',
  'btnLangEn',
  'table-of-contents',
  'overview',
  'original-links--references',
  'quickstart',
  'automated-cli-installer-zimbra-link-installersh',
  'dependencies',
  'download-verification-status--legend',
  'build-systems--source-compilation-guide',
  'configuration',
  'security-architecture--comprehensive-cve-matrix-20162026',
  'operational-best-practices-rfc-2119',
  'strategic-migration--upgrade-methodology',
  'running-tests',
  'ecosystem-tools--repositories',
  'contributing',
  'official-contact--author',
  'license'
];

console.log('--- Checking Required Section IDs ---');
let missingIds = 0;
for (const id of requiredIds) {
  if (!html.includes(`id="${id}"`)) {
    console.error(`MISSING ID: #${id}`);
    missingIds++;
  } else {
    console.log(`  ✓ #${id} exists`);
  }
}

console.log('\n--- Checking CSS Rules for Dual Language ---');
const hasIdCss = html.includes('html[lang="id"] .lang-en');
const hasEnCss = html.includes('html[lang="en"] .lang-id');
console.log('  html[lang="id"] .lang-en hidden:', hasIdCss);
console.log('  html[lang="en"] .lang-id hidden:', hasEnCss);

console.log('\n--- Checking Bilingual Content Elements ---');
const langIdMatches = (html.match(/class="[^"]*lang-id[^"]*"/g) || []).length;
const langEnMatches = (html.match(/class="[^"]*lang-en[^"]*"/g) || []).length;
console.log(`  Found ${langIdMatches} elements with .lang-id`);
console.log(`  Found ${langEnMatches} elements with .lang-en`);

if (missingIds === 0 && hasIdCss && hasEnCss && langIdMatches > 0 && langEnMatches > 0) {
  console.log('\n✅ ALL BILINGUAL I18N CHECKS PASSED PERFECTLY!');
  process.exit(0);
} else {
  console.error('\n❌ SOME CHECKS FAILED!');
  process.exit(1);
}
