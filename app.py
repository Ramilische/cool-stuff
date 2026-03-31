from flask import Flask, render_template, url_for

app = Flask(__name__)

nav = []


@app.route('/')
def homepage():
    return render_template('homepage.html', title='Домашняя страница', nav=nav)


@app.route('/about')
def about():
    return render_template('about.html', title='О сайте', nav=nav)


with app.test_request_context('/', method='GET'):
    nav = [
    {
        'url': url_for('homepage'),
        'title': 'Главная страница'
    },
    {
        'url': url_for('about'),
        'title': 'О сайте'
    }
    ]