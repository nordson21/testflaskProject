from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


def get_photos_links_from_folder(folder_path="static/images/gallery"):
    images_urls =  [f'{folder_path}/{name}' for name in os.listdir(folder_path)]
    return images_urls

@app.route('/')
def index():  # put application's code here
    nav_act = "class=active"
    title = 'Фотограф Юлия Карелина'
    css = url_for('static', filename='styles/index.css')
    return render_template('index.html', title=title, css=css, nav_act_index=nav_act)

@app.route('/gallery')
def samples():
    nav_act = "class=active"
    title = 'Галерея'
    css = url_for('static', filename='styles/index.css')
    photos_list = get_photos_links_from_folder()
    return render_template('gallery.html', title=title, nav_act_gallery=nav_act, css=css, images_urls=photos_list)

@app.route('/about/')
@app.route('/about')
def about():
    title = 'Абамне'
    return 'Йа фатограф'

@app.route('/gallery/<gallery_id>')
def gallery(gallery_id):
    title = f'Галерея {gallery_id}'
    return f'Тут будет галерея номер {gallery_id}'

@app.errorhandler(404)
def error_404(error):
    title = f'Error'
    return 'Такой страницы нет!', 404

if __name__ == '__main__':
    app.run(debug=True)
