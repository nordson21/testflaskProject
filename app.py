from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


def get_photos_links_from_folder(folder_path="static/images/gallery"):
    images_urls = sorted([f'{folder_path}/{name}' for name in os.listdir(folder_path)])
    return images_urls


@app.route('/')
def index():  # put application's code here
    title = 'Фотограф Юлия Карелина'
    css = url_for('static', filename='styles/index.css')
    return render_template('index.html', title=title, css=css)


@app.route('/gallery')
def samples():
    title = 'Галерея'
    css = url_for('static', filename='styles/index.css')
    photos_list = get_photos_links_from_folder()
    return render_template('gallery.html', title=title, css=css, images_urls=photos_list)


@app.route('/about/')
@app.route('/about')
def about():
    # title = 'Обо мне'
    return 'Я фотограф'


@app.route('/gallery/<gallery_id>')
def gallery(gallery_id):
    # title = f'Галерея {gallery_id}'
    return f'Тут будет галерея номер {gallery_id}'


@app.errorhandler(404)
def error_404(error):
    title = f'{error}'
    return 'Такой страницы нет!', 404

@app.route('/testgallery')
def test_gallery():
    title = 'тест Галерея'
    css = url_for('static', filename='styles/testgallery.css')
    photos_list = get_photos_links_from_folder()
    return render_template('tetstgal-grid.html', title=title, css=css, images_urls=photos_list)

if __name__ == '__main__':
    app.run(debug=True)
