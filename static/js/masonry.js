function handleGrid(cardsData) {
    const masonryGrid = document.getElementById('masonryGrid');

    // Создание колонок
    function createColumns() {
        masonryGrid.innerHTML = '';
        const columnCount = window.innerWidth < 768 ? 1 :
            window.innerWidth < 1200 ? 2 : 3;

        for (let i = 0; i < columnCount; i++) {
            const column = document.createElement('div');
            column.className = 'column';
            column.dataset.column = i;
            masonryGrid.appendChild(column);
        }
    }

    // Создание карточки
    function createCard(cardData) {
        const card = document.createElement('div');
        card.className = 'grid-item';
        card.dataset.category = cardData.category;

        card.innerHTML = `
                    <img src="${cardData.photoname}" alt="" loading="lazy">
                    <div class="item-content">
                        <h3>${cardData.name}</h3>
                        <p><strong>Сфера:</strong> ${cardData.sphere}</p>
                        <p><strong>Город:</strong> ${cardData.city.name}</p>
                        <p><strong>Скидка:</strong> ${cardData.discount}%</p>
                        <div class="item-footer">
                            <button class="save-btn" id="popup-link" onclick="new_page('${cardData.twogislink}')">Перейти в 2ГИС</button>
                            <button class="save-btn" id="open-popup" onclick="show_popup('${cardData.name}', '${cardData.terms}')">Условия</button>
                        </div>
                    </div>
                `;

        return card;
    }

    // Распределение карточек по колонкам
    function distributeCards(cards) {
        const columns = document.querySelectorAll('.column');
        columns.forEach(column => column.innerHTML = '');

        cards.forEach((cardData, index) => {
            const card = createCard(cardData);
            const columnIndex = index % columns.length;
            columns[columnIndex].appendChild(card);
        });
    }

    // Инициализация
    function init() {
        createColumns();
        distributeCards(cardsData);

        // Обработчик изменения размера окна
        window.addEventListener('resize', function () {
            createColumns();
            distributeCards(cardsData);
        });
    }

    // Запуск инициализации
    init();
}