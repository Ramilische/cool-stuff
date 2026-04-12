(function () {
    
    // ---------- DOM элементы ----------
    const playlistContainer = document.getElementById('playlistContainer');
    const nowTitle = document.getElementById('nowTitle');
    const nowArtist = document.getElementById('nowArtist');
    const nowCover = document.getElementById('nowCover');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const progressSlider = document.getElementById('progressSlider');
    const currentTimeSpan = document.getElementById('currentTime');
    const durationTimeSpan = document.getElementById('durationTime');
    const volumeSlider = document.getElementById('volumeSlider');
    const volumeIcon = document.getElementById('volumeIcon');

    // ---------- Состояние плеера ----------
    let currentTrackIndex = 0;           // индекс активного трека
    let isPlaying = false;
    let audio = new Audio();
    let trackElements = [];              // массив DOM-элементов треков

    // Инициализация громкости
    audio.volume = 0.5;
    volumeSlider.value = '0.5';
    playIcon.hidden = false;
    pauseIcon.hidden = true;

    // ---------- Вспомогательные функции ----------
    function formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    // Обновить UI плеера (название, обложка)
    function updatePlayerUI() {
        const track = tracks[currentTrackIndex];
        nowTitle.textContent = track.title;
        nowArtist.textContent = track.artist;
        // Меняем иконку обложки
        nowCover.innerHTML = `<i class="fas ${track.coverIcon}"></i>`;
      
        // Подсветка активного трека в списке
        trackElements.forEach((el, idx) => {
            if (idx === currentTrackIndex) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        });
    }

    // Загрузить трек по индексу (но не играть автоматически, только подготовить)
    function loadTrack(index) {
        if (!tracks[index]) return;
        const wasPlaying = isPlaying;
      
        // Если аудио уже играло, остановим
        audio.pause();
      
        const track = tracks[index];
        audio.src = track.src;
        audio.load();
      
        currentTrackIndex = index;
        updatePlayerUI();
      
        // Сброс прогресса
        progressSlider.value = 0;
        currentTimeSpan.textContent = '0:00';
      
        // Если трек играл до переключения — начинаем играть новый
        if (wasPlaying) {
            const playPromise = audio.play();
            if (playPromise !== undefined) {
                playPromise.catch(e => {
                    console.warn('Автовоспроизведение заблокировано, нажмите play');
                    isPlaying = false;
                    updatePlayButton();
                });
            }
            isPlaying = true;
        } else {
            isPlaying = false;
        }
        updatePlayButton();
    }

    // Воспроизведение / пауза
    function togglePlay() {
        if (!audio.src || audio.src === window.location.href) {
            // Если источник не задан (напр. при первой загрузке) — загружаем первый трек
            if (tracks.length > 0) {
                loadTrack(0);
            } else {
                return;
            }
        }
      
        if (isPlaying) {
            audio.pause();
            isPlaying = false;
        } else {
            const playPromise = audio.play();
            if (playPromise !== undefined) {
                playPromise.then(() => {
                isPlaying = true;
            }).catch(err => {
                console.warn('Ошибка воспроизведения:', err);
                isPlaying = false;
            }).finally(() => {
                updatePlayButton();
            });
            }
        }
        updatePlayButton();
    }

    function updatePlayButton() {
        if (isPlaying) {
            playIcon.hidden = true;
            pauseIcon.hidden = false;
        }
        else {
            playIcon.hidden = false;
            pauseIcon.hidden = true;
        }
    }

    // Следующий трек
    function nextTrack() {
        if (tracks.length === 0) return;
        let nextIndex = (currentTrackIndex + 1) % tracks.length;
        loadTrack(nextIndex);
        if (!isPlaying) {
            // если не играло — после загрузки начнём играть (loadTrack учтёт wasPlaying)
            // но loadTrack смотрит на isPlaying до смены, поэтому явно запустим
            if (!isPlaying) {
                audio.play().then(() => { isPlaying = true; updatePlayButton(); }).catch(()=>{});
            }
        }
    }

    // Предыдущий трек
    function prevTrack() {
        if (tracks.length === 0) return;
        let prevIndex = (currentTrackIndex - 1 + tracks.length) % tracks.length;
        loadTrack(prevIndex);
        if (!isPlaying) {
            audio.play().then(() => { isPlaying = true; updatePlayButton(); }).catch(()=>{});
        }
    }

    // Обновление прогресса (timeupdate)
    function updateProgress() {
        if (audio.duration) {
            const percent = (audio.currentTime / audio.duration) * 100;
            progressSlider.value = percent;
            currentTimeSpan.textContent = formatTime(audio.currentTime);
            durationTimeSpan.textContent = formatTime(audio.duration);
        } else {
            durationTimeSpan.textContent = tracks[currentTrackIndex]?.duration || '0:00';
        }
    }

    // Перемотка при изменении слайдера
    function seekAudio() {
        if (!audio.duration) return;
        const seekTime = (progressSlider.value / 100) * audio.duration;
        audio.currentTime = seekTime;
    }

    // Изменение громкости
    function setVolume() {
        audio.volume = volumeSlider.value;
        // Меняем иконку громкости
        const vol = audio.volume;
        if (vol === 0) {
            volumeIcon.className = 'fas fa-volume-mute volume-icon';
        } else if (vol < 0.5) {
            volumeIcon.className = 'fas fa-volume-down volume-icon';
        } else {
            volumeIcon.className = 'fas fa-volume-up volume-icon';
        }
    }

    // Обработка окончания трека
    function onTrackEnded() {
        // Автоматически следующий трек
        nextTrack();
    }

    // Создание элементов списка треков
    function renderPlaylist() {
        playlistContainer.innerHTML = '';
        trackElements = [];
      
        tracks.forEach((track, index) => {
            const item = document.createElement('div');
            item.className = 'track-item';
            if (index === currentTrackIndex) item.classList.add('active');
        
            // Информация
            const infoDiv = document.createElement('div');
            infoDiv.className = 'track-info';
            infoDiv.innerHTML = `
            <div class="track-title">${track.title}</div>
            <div class="track-artist">${track.artist}</div>
            `;
        
            // Длительность
            const durationSpan = document.createElement('span');
            durationSpan.className = 'track-duration';
            durationSpan.textContent = track.duration;
        
            // Иконка play при наведении
            const playIndicator = document.createElement('span');
            playIndicator.className = 'play-icon';
            playIndicator.innerHTML = '<i class="fas fa-play"></i>';
        
            item.appendChild(infoDiv);
            item.appendChild(durationSpan);
            item.appendChild(playIndicator);
        
            // Клик по треку — воспроизвести
            item.addEventListener('click', (e) => {
                // Если трек уже активен, просто переключаем play/pause
                if (currentTrackIndex === index) {
                    togglePlay();
                } else {
                    // Меняем трек и начинаем воспроизведение
                    loadTrack(index);
                    // Запускаем проигрывание
                    audio.play().then(() => {
                        isPlaying = true;
                        updatePlayButton();
                    }).catch(err => {
                        console.warn('Ошибка при клике на трек:', err);
                    });
                }
            });
        
            playlistContainer.appendChild(item);
            trackElements.push(item);
        });
      
        // Если треки есть, загрузим первый, но не запускаем авто-плей (пользователь сам нажмёт)
        if (tracks.length > 0) {
            // Инициализация: загружаем первый трек в плеер (без автовоспроизведения)
            audio.src = tracks[0].src;
            audio.load();
            currentTrackIndex = 0;
            updatePlayerUI();
            durationTimeSpan.textContent = tracks[0].duration;
            currentTimeSpan.textContent = '0:00';
        }
    }

    // ---------- Привязка событий ----------
    function bindEvents() {
        // Управление плеером
        playPauseBtn.addEventListener('click', togglePlay);
        prevBtn.addEventListener('click', prevTrack);
        nextBtn.addEventListener('click', nextTrack);
      
        // Аудио события
        audio.addEventListener('timeupdate', updateProgress);
        audio.addEventListener('loadedmetadata', () => {
            durationTimeSpan.textContent = formatTime(audio.duration);
            // если длительность из метаданных отличается от статичной, обновим
            const track = tracks[currentTrackIndex];
            if (track) {
                // можно оставить статичную, но показываем реальную
            }
        });
        audio.addEventListener('ended', onTrackEnded);
        audio.addEventListener('play', () => {
            isPlaying = true;
            updatePlayButton();
        });
        audio.addEventListener('pause', () => {
            isPlaying = false;
            updatePlayButton();
        });
        audio.addEventListener('error', (e) => {
            console.error('Ошибка загрузки аудио:', e);
            alert('Не удалось загрузить трек. Возможно, ссылка недоступна.');
            isPlaying = false;
            updatePlayButton();
        });
      
        // Прогресс слайдер
        progressSlider.addEventListener('input', seekAudio);
      
        // Громкость
        volumeSlider.addEventListener('input', setVolume);
      
        // Дополнительно: клик по иконке громкости для mute/unmute (опционально)
        volumeIcon.addEventListener('click', () => {
            if (audio.volume > 0) {
                audio.volume = 0;
                volumeSlider.value = 0;
            } else {
                audio.volume = 0.8;
            volumeSlider.value = 0.8;
            }
            setVolume();
        });
    }

    // ---------- Инициализация ----------
    function init() {
        renderPlaylist();
        bindEvents();
        setVolume(); // установить иконку громкости
      
        // Предзагрузка первого трека без автовоспроизведения
        if (tracks.length > 0) {
            audio.src = tracks[0].src;
            audio.load();
            updatePlayerUI();
            durationTimeSpan.textContent = tracks[0].duration;
        }
    }

    init();
})();