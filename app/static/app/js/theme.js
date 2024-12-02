document.addEventListener('DOMContentLoaded', () => {
    const buttons = {
        dark: document.getElementById('dark-mode-toggle'),
        halloween: document.getElementById('halloween-mode-toggle'),
        christmas: document.getElementById('christmasToggle'),
        light: document.getElementById('light-mode-toggle'),
    };

    const themes = ['light-mode', 'dark-mode', 'halloween-mode', 'christmas-mode'];

    const applyTheme = (theme) => {
        document.body.classList.remove(...themes);
        document.body.classList.add(theme);
        console.log(`Applied theme: ${theme}`);
        localStorage.setItem('theme', theme);
    };

    // Apply stored theme on page load
    const storedTheme = localStorage.getItem('theme') || 'light-mode';
    applyTheme(storedTheme);

    // Add event listeners to buttons
    Object.entries(buttons).forEach(([theme, button]) => {
        if (button) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                applyTheme(`${theme}-mode`);
            });
        } else {
            console.warn(`Button with ID ${theme}-mode-toggle not found.`);
        }
    });
});
