from flask import Flask, render_template, url_for

app = Flask(__name__)


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
    return render_template('gallery.html', title=title, nav_act_gallery=nav_act)

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
