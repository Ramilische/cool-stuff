# Скрипт для запуска нового окна браузера и приложения Flask

# поменяй путь до окружения
source /home/ramilische/projects/websites/cool-stuff-that-i-like/.venv/bin/activate

# если дебажим веб-приложение, то можно раскомментировать эту строку и добавить --debug в запуск Flask
# firefox --new-window http://127.0.0.1:45678
flask --app app.py run -p 45678