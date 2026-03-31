# Скрипт для запуска нового окна браузера и приложения Flask

# поменяй путь до окружения
source /home/ramilische/projects/websites/cool-stuff-that-i-like/.venv/bin/activate

# у меня здесь firefox, но можно и в другом браузере открыть страницу
firefox --new-window http://127.0.0.1:45678
flask --app main.py run -p 45678