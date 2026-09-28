window.utils = window.utils || {};

(function () {
  const toText = (value, fallback = '-') => {
    if (value === null || value === undefined || value === '') return fallback;
    return String(value);
  };

  const safeJsonParse = (value, fallback = {}) => {
    try {
      return JSON.parse(value);
    } catch {
      return fallback;
    }
  };

  const formatDate = (value) => {
    if (!value) return '-';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return toText(value);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const formatTime = (value) => {
    if (!value) return '-';
    const date = new Date(`1970-01-01T${value}`);
    if (Number.isNaN(date.getTime())) return toText(value);
    return date.toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const setText = (selector, value) => {
    const el = document.querySelector(selector);
    if (el) el.textContent = toText(value);
  };

  const show = (selector) => {
    const el = document.querySelector(selector);
    if (el) el.classList.remove('hidden');
  };

  const hide = (selector) => {
    const el = document.querySelector(selector);
    if (el) el.classList.add('hidden');
  };

  window.utils.toText = toText;
  window.utils.safeJsonParse = safeJsonParse;
  window.utils.formatDate = formatDate;
  window.utils.formatTime = formatTime;
  window.utils.setText = setText;
  window.utils.show = show;
  window.utils.hide = hide;
})();