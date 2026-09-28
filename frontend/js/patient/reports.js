document.addEventListener('click', (event) => {
  const button = event.target.closest('[data-download-report]');
  if (!button) return;
  alert('Downloading report');
});