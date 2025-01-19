document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle Setup
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i');
    const html = document.documentElement;
    
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme') || (prefersDark ? 'dark' : 'light');
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Initialize all dropdowns
    const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
    const dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl)
    });
    
    // Translation Setup for Summary Card
    const summaryDropdown = document.querySelector('.summary-dropdown .dropdown-menu');
    if (summaryDropdown) {
        summaryDropdown.addEventListener('click', async (e) => {
            if (e.target.classList.contains('dropdown-item')) {
                const language = e.target.textContent;
                const summaryContent = document.querySelector('.summary-content');
                if (summaryContent) {
                    try {
                        const response = await fetch('/translate', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                text: summaryContent.textContent,
                                language: language
                            })
                        });
                        const data = await response.json();
                        if (data.success && data.translated) {
                            summaryContent.textContent = data.translated;
                        }
                    } catch (error) {
                        console.error('Translation error:', error);
                    }
                }
            }
        });
    }
    
    // Progress Bar Setup
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.getElementById('progressBar').style.width = scrolled + '%';
    });

    // Copy Button Setup
    const copyButton = document.getElementById('copyButton');
    if (copyButton) {
        copyButton.addEventListener('click', () => {
            const summary = document.querySelector('.summary-content').innerText;
            navigator.clipboard.writeText(summary);
            copyButton.innerHTML = '<i class="bi bi-check"></i> Copied!';
            setTimeout(() => {
                copyButton.innerHTML = '<i class="bi bi-clipboard"></i> Copy';
            }, 2000);
        });
    }

    // Initialize Reading Time
    calculateReadingTime();

    // Helper Functions
    function updateThemeIcon(theme) {
        themeIcon.className = theme === 'dark' 
            ? 'bi bi-sun-fill' 
            : 'bi bi-moon-stars';
    }
    function calculateReadingTime() {
        const content = document.querySelector('.summary-content');
        if (content) {
            const words = content.innerText.split(' ').length;
            const readingTime = Math.ceil(words / 200);
            document.querySelector('.reading-time').innerText = 
                `${readingTime} min read • ${words} words`;
        }
    }
    async function translatePage(language) {
        try {
            const content = document.querySelector('.summary-content');
            if (!content) return;

            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: content.textContent,
                    language: language
                })
            });
            const data = await response.json();
            if (data.success && data.translated) {
                content.textContent = data.translated;
            } else {
                console.error('Translation failed:', data.error);
            }
        } catch (error) {
            console.error('Translation error:', error);
        }
    }
});