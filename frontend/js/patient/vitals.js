document.addEventListener('click', (event) => {
  const button = event.target.closest('[data-save-vitals]');
  if (!button) return;
  alert('Vitals saved');
});