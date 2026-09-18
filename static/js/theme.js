try {
  const savedTheme = localStorage.getItem('research-theme');
  document.documentElement.dataset.theme = savedTheme === 'dark' ? 'dark' : 'light';
} catch (_) {
  document.documentElement.dataset.theme = 'light';
}
