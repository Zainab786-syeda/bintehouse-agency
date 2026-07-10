document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-box');
    const toolCards = document.querySelectorAll('.tool-card');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();

            toolCards.forEach(card => {
                const toolName = card.querySelector('h3').textContent.toLowerCase();
                const toolDesc = card.querySelector('p').textContent.toLowerCase();

                // اگر سرچ کیا گیا لفظ نام یا ڈسکرپشن میں موجود ہو تو کارڈ دکھائیں، ورنہ چھپا دیں
                if (toolName.includes(searchTerm) || toolDesc.includes(searchTerm)) {
                    card.style.display = 'flex';
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0';
                }
            });
        });
    }
});
