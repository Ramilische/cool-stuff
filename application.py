from os import getenv, path

import dotenv
from flask import Flask, render_template, url_for, redirect, request, flash
from markupsafe import Markup
from werkzeug.utils import secure_filename

from db.requests import PostRepository
from utils.md_to_html import make_post
from utils.tracks import albums, parse_tracks

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'md', 'png', 'jpg', 'jpeg', 'gif'}

nav = []

dotenv.load_dotenv('.env/config.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
    return redirect(url_for('blog'))


@app.route('/blog/category/<category>')
def blog_category(category: str):
    code, res = PostRepository.category_posts(category)
    if code == 200:
        posts = res['posts']
        ru_name = res['ru_name']
    else:
        return render_template('app/blog.html', title='Блог', nav=nav, posts=[])
    for post in posts:
        post['banner_photo_path'] = url_for('static', filename=f'img/{post["banner_photo_path"]}')
        post['content'] = make_post(post['md_file_path'])
        post['url'] = url_for('post', id=post['id'])
    return render_template('app/blog.html', title=ru_name, desc='Категория блога', nav=nav, posts=posts)


@app.route('/blog')
def blog():
    code, res = PostRepository.all_blog_posts()
    title = 'Блог'
    desc = 'Посты на различные темы. Здесь я делюсь мнением об IT, процессом разработки своих проектов, болтаю о жизни. Короче мнения одного человека обо всем и ни о чем, можешь даже не открывать'
    
    if code == 200:
        posts = res['posts']
    else:
        return render_template('app/blog.html', title=title, desc=desc, nav=nav, posts=[])
    for post in posts:
        post['banner_photo_path'] = url_for('static', filename=f'img/{post["banner_photo_path"]}')
        post['content'] = make_post(post['md_file_path'])
        post['url'] = url_for('post', id=post['id'])
    
    return render_template('app/blog.html', title=title, desc=desc, nav=nav, posts=posts)


@app.route('/post/<int:id>')
def post(id: int):
    code, res = PostRepository.get_post(post_id=id)
    if code == 200:
        post = res['post']
        return render_template('app/post.html', title=post['title'], desc=post['description'], nav=nav, content=Markup(make_post(post['md_file_path'])))
    else:
        return redirect(url_for('blog'))

@app.route('/recipe/<int:id>')
def recipe(id: int):
    code, res = PostRepository.get_recipe(post_id=id)
    if code == 200:
        post = res['post']
        return render_template('app/post.html', title=post['title'], desc=post['description'], nav=nav, content=Markup(make_post(post['md_file_path'])))
    else:
        return redirect(url_for('blog'))

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title = 'Новый пост'
    desc = 'Окно создания нового поста, сделать бы его только для админов'

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

        code, res = PostRepository.add_post(form)
        if code == 201:
            flash('Пост был создан')
        else:
            flash(f'Ошибка, {res["message"]}')
    
    return render_template('app/forms/newpost.html', title=title, desc=desc, nav=nav)

@app.route('/gallery')
def gallery():
    title = 'Галерея'
    desc = 'Здесь будет несколько категорий изображений, которые я собирал. Обои, мемы, панели из манги и т.п.'

    return render_template('app/mainpages/gallery.html', title=title, desc=desc, nav=nav)


@app.route('/music/<album_title>')
def album(album_title: str):
    title = album_title
    desc = alb['description']

    alb = dict()
    for album in albums:
        if album['title'] == album_title:
            alb = album
    
    if not alb:
        return redirect(url_for('music'))
    return render_template('app/player.html', title=title, desc=desc, nav=nav, album=alb)

@app.route('/music')
def music():
    title = 'Плейлисты'
    desc = 'Часть моей музыкальной коллекции, которой не стыдно поделиться'

    return render_template('app/mainpages/music.html', title=title, desc=desc, nav=nav, albums=albums)

@app.route('/reloadmusic')
def reload_music():
    parse_tracks()
    
    return redirect(url_for('music'))


@app.route('/recipes')
def recipes():
    code, res = PostRepository.all_recipes()
    title = 'Рецепты'
    desc = 'Здесь я делюсь рецептами, их не так уж и много. Многие из этих рецептов можно найти в Сети'

    if code == 200:
        posts = res['posts']
    else:
        return render_template('app/blog.html', title='Рецепты', nav=nav, posts=[])
    
    for post in posts:
        post['banner_photo_path'] = url_for('static', filename=f'img/{post["banner_photo_path"]}')
        post['content'] = make_post(post['md_file_path'])
        post['url'] = url_for('recipe', id=post['id'])
    
    return render_template('app/blog.html', title=title, desc=desc, nav=nav, posts=posts)
    # return render_template('app/mainpages/recipes.html', title='Рецепты', nav=nav)


@app.route('/projects')
def projects():
    title = 'Проекты'
    desc = 'Сюда я буду кидать ссылки на свои проекты: сайты, Telegram ботов, игры (если буду выкладывать в Стим)'

    return render_template('app/mainpages/projects.html', title=title, desc=desc, nav=nav)


@app.route('/recommendations')
def recommendations():
    title = 'Рекомендации'
    desc = 'Место для моих самых разных рекомендаций - от классной шавухи до интересного сайта, в котором можно залипнуть'

    return render_template('app/mainpages/recommendations.html', title=title, desc=desc, nav=nav)


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