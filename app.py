from os import getenv, path, listdir

import dotenv
from flask import Flask, render_template, url_for, redirect, request, flash
from markupsafe import Markup
from werkzeug.utils import secure_filename
from tinytag import TinyTag

from db.requests import PostRepository
from db.models import init_db
from utils.md_to_html import make_post

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'md', 'png', 'jpg', 'jpeg', 'gif'}
MUSIC_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac']

app = Flask(__name__)
dotenv.load_dotenv('.env/config.env')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

nav = []
albums = []


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_tracks():
    lst = listdir('static/audio')
    folders = []
    files = []
    for item in lst:
        if any([item.endswith(ext) for ext in MUSIC_EXTENSIONS]):
            files.append(item)
        else:
            folders.append(item)

    albums.clear()

    for album in folders:
        path = f'static/audio/{album}'
        lst = listdir(path)
        desc = 'Описание отсутствует...'
        tracks = list()
        for item in lst:
            if item.endswith('.txt'):
                with open(path+'/'+item, 'r', encoding='utf-8') as file:
                    desc = file.read().strip()
                continue
            track_path = path + '/' + item
            info = TinyTag.get(track_path)

            minutes, seconds = str(int(info.duration // 60)), int(info.duration % 60)
            if seconds < 10:
                seconds = '0' + str(seconds)

            track = {'title': item, 'artist': '', 'duration': f'{minutes}:{seconds}', 'src': f'audio/{album}/{item}', 'filename': item}

            if info.title:
                track['title'] = info.title
            if info.artist:
                track['artist'] = info.artist

            tracks.append(track)
        albums.append({
            'title': album,
            'tracks': tracks,
            'description': desc
        })
    print(albums)
    


@app.route('/')
def homepage():
    return redirect(url_for('blog'))


@app.route('/blog')
def blog():
    code, res = PostRepository.all_posts()
    if code == 200:
        posts = res
    else:
        return render_template('app/blog.html', title='Блог', nav=nav, posts=[])
    for post in posts:
        post['banner_photo_path'] = url_for('static', filename=f'img/{post["banner_photo_path"]}')
        post['content'] = make_post(post['md_file_path'])
        post['url'] = url_for('post', id=post['id'])
    return render_template('app/blog.html', title='Блог', nav=nav, posts=posts)


@app.route('/post/<int:id>')
def post(id: int):
    code, post = PostRepository.get_post(post_id=id)
    if code == 200:
        return render_template('app/post.html', title='Блог', nav=nav, content=Markup(make_post(post['md_file_path'])))
    else:
        return redirect(url_for('blog'))


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        form = dict(request.form)
        # print(request.files)
        # if 'img-file' not in request.files:
        #     print('1')
        #     flash('No image file selected')
        #     return redirect(request.url)
        # img_file = request.files['img-file']
        # if img_file.filename == '':
        #     print('2')
        #     flash('No image file selected')
        #     return redirect(request.url)
        # if img_file and allowed_file(img_file.filename):
        #     filename = secure_filename(img_file.filename)
        #     img_file.save(path.join(app.config['UPLOAD_FOLDER'], 'img', filename))
        #     return redirect(url_for('download_file', name=filename))

        code, message = PostRepository.add_post(form)
        if code == 201:
            flash('Пост был создан')
        else:
            flash('Ошибка')
        
        code, message = PostRepository.add_post()
    return render_template('app/forms/newpost.html', title='Новый пост', nav=nav)


@app.route('/gallery')
def gallery():
    return render_template('app/mainpages/gallery.html', title='Галерея', nav=nav)


@app.route('/music/<title>')
def album(title: str):
    alb = dict()
    for album in albums:
        print(album)
        if album['title'] == title:
            alb = album
    
    return render_template('app/player.html', title=title, nav=nav, album=alb)


@app.route('/music')
def music():
    return render_template('app/mainpages/music.html', title='Плейлисты', nav=nav, albums=albums)

@app.route('/player')
def player():
    return render_template('app/donors/testplayer.html')

@app.route('/reloadmusic')
def reload_music():
    parse_tracks()
    
    return redirect(url_for('music'))


@app.route('/recipes')
def recipes():
    return render_template('app/mainpages/recipes.html', title='Рецепты', nav=nav)


@app.route('/projects')
def projects():
    return render_template('app/mainpages/projects.html', title='Проекты', nav=nav)


@app.route('/recommendations')
def recommendations():
    return render_template('app/mainpages/recommendations.html', title='Рекомендации', nav=nav)


with app.test_request_context('/', method='GET'):
    nav = [
    {
        'url': url_for('blog'),
        'title': 'Блог'
    },
    {
        'url': url_for('gallery'),
        'title': 'Галерея'
    },
    {
        'url': url_for('music'),
        'title': 'Музыка'
    },
    {
        'url': url_for('recipes'),
        'title': 'Рецепты'
    },
    {
        'url': url_for('projects'),
        'title': 'Проекты'
    },
    {
        'url': url_for('recommendations'),
        'title': 'Рекомендации'
    }
    ]