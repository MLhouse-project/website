/* Reading enhancements only; the complete report works without JavaScript. */
const printButton = document.querySelector('.print-button');
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
}
const contents = document.querySelector('.contents details');
if (contents && window.matchMedia('(max-width: 950px)').matches) contents.open = false;
const sectionLinks = Array.from(document.querySelectorAll('.contents nav a'));
const sections = sectionLinks.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
let scheduled = false;
function markCurrentSection() {
  let current = null;
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= 160) current = section.id;
  }
  sectionLinks.forEach(link => {
    if (link.hash === '#' + current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  scheduled = false;
}
window.addEventListener('scroll', () => {
  if (!scheduled) { scheduled = true; window.requestAnimationFrame(markCurrentSection); }
}, { passive: true });
markCurrentSection();
const disclosures = document.querySelectorAll('details');
let beforePrintState = [];
window.addEventListener('beforeprint', () => {
  beforePrintState = Array.from(disclosures, item => item.open);
  disclosures.forEach(item => { item.open = true; });
});
window.addEventListener('afterprint', () => {
  disclosures.forEach((item, index) => { item.open = beforePrintState[index]; });
});
