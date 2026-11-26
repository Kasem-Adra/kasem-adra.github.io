(() => {
    const key = 'kasemadra-theme';
    const system = window.matchMedia('(prefers-color-scheme: dark)');
    const root = document.documentElement;
    let preference;
    try {
        preference = localStorage.getItem(key);
    } catch {
        // The theme can still be changed for this page.
    }
    if (preference !== 'light' && preference !== 'dark') preference = null;

    function apply(theme) {
        root.dataset.theme = theme;
        const button = document.querySelector('.theme-toggle');
        if (!button) return;
        button.setAttribute('aria-pressed', String(theme === 'dark'));
        button.firstElementChild.textContent = theme === 'dark' ? '☀' : '☾';
    }

    function systemTheme() {
        return system.matches ? 'dark' : 'light';
    }

    apply(preference || systemTheme());
    document.addEventListener('DOMContentLoaded', () => {
        const button = document.querySelector('.theme-toggle');
        if (!button) return;
        apply(preference || systemTheme());
        button.hidden = false;
        button.addEventListener('click', () => {
            preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
            apply(preference);
            try {
                localStorage.setItem(key, preference);
            } catch {
                // The selected theme stays active on this page.
            }
        });
    });
    system.addEventListener('change', () => {
        if (!preference) apply(systemTheme());
    });
})();
