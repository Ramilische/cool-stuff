from flask import Flask, render_template, url_for, redirect
from db.requests import PostRepository
from db.models import init_db

app = Flask(__name__)

nav = []


@app.route('/')
def homepage():
    return redirect(url_for('blog'))


@app.route('/blog')
def blog():
    return render_template('app/blog.html', title='Блог', nav=nav)


@app.route('/gallery')
def gallery():
    return render_template('app/gallery.html', title='Галерея', nav=nav)


@app.route('/music')
def music():
    return render_template('app/music.html', title='Музыка', nav=nav)


@app.route('/recipes')
def recipes():
    return render_template('app/recipes.html', title='Рецепты', nav=nav)


@app.route('/projects')
def projects():
    return render_template('app/projects.html', title='Проекты', nav=nav)


@app.route('/recommendations')
def recommendations():
    return render_template('app/recommendations.html', title='Рекомендации', nav=nav)


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