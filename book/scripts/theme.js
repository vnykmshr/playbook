// Theme toggle: auto → light → dark → auto
// Persists choice in localStorage. "auto" follows system preference.
(function () {
  var KEY = 'pb-theme';
  var MODES = ['auto', 'light', 'dark'];
  var LABELS = { auto: 'Auto', light: 'Light', dark: 'Dark' };

  function apply(mode) {
    if (mode === 'auto') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', mode);
    }
  }

  function current() {
    return localStorage.getItem(KEY) || 'auto';
  }

  function next(mode) {
    return MODES[(MODES.indexOf(mode) + 1) % MODES.length];
  }

  // Apply saved preference before paint
  apply(current());

  // Wire up toggle buttons once DOM is ready
  document.addEventListener('DOMContentLoaded', function () {
    var buttons = document.querySelectorAll('.theme-toggle');
    var mode = current();

    buttons.forEach(function (btn) {
      btn.textContent = LABELS[mode];
      btn.addEventListener('click', function () {
        mode = next(mode);
        localStorage.setItem(KEY, mode);
        apply(mode);
        buttons.forEach(function (b) { b.textContent = LABELS[mode]; });
      });
    });
  });
})();
