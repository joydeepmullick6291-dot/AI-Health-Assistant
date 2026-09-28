(function () {
  const root = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  let currentTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

  root.setAttribute('data-theme', currentTheme);

  const updateToggle = () => {
    if (!toggle) return;
    toggle.textContent = currentTheme === 'dark' ? '☼' : '◐';
    toggle.setAttribute(
      'aria-label',
      currentTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
    );
  };

  updateToggle();

  toggle?.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', currentTheme);
    updateToggle();
  });
})();