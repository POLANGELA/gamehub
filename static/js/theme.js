function toggleTheme() {
    const html = document.documentElement;
    html.classList.toggle('dark');
    localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
}
window.onload = function() {
    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('dark');
    }
}
