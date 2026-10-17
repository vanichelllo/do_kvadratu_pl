// Адмінка завдань: формули $…$ у списку, попередньому перегляді й масовому редагуванні
// відмальовуються так само, як на сайті (поля введення MathJax не чіпає)
window.MathJax = {
    tex: {inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], processEscapes: true},
    svg: {fontCache: 'global'}
};
(function () {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
    script.async = true;
    document.head.appendChild(script);
})();
