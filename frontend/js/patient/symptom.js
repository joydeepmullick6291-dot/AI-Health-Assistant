document.addEventListener('click', (event) => {
  const button = event.target.closest('[data-run-prediction]');
  if (!button) return;
  alert('Prediction started');
});