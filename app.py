from flask import Flask, render_template, url_for, request, redirect
import os
import sqlite3
from datetime import datetime


with sqlite3.connect("site.db") as db:
    cur = db.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY NOT NULL)
            """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL , message TEXT,
            date INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id))
            """)
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, date INTEGER,
                    ip TEXT, request TEXT, agent TEXT)
                    """)
    db.commit()


def add_message_in_db(user: str, message: str):
    with sqlite3.connect("site.db") as db:
        print('db started')
        message_time = int(datetime.timestamp(datetime.now()))
        cur = db.cursor()
        cur.execute(f"""
        INSERT OR IGNORE INTO users(id) VALUES('{user}')
        """)
        cur.execute(f"""
        INSERT INTO messages (user_id, message, date) VALUES('{user}', '{message}', {message_time})
        """)
        db.commit()
        print('DB closed')

def add_request_to_db():
    with sqlite3.connect("site.db") as db:
        date = int(datetime.timestamp(datetime.now()))
        ip = request.remote_addr
        req = request.path
        user_agent = str(request.user_agent)
        print(datetime.now(), ip, req, user_agent)
        cur = db.cursor()
        cur.execute(f"""INSERT INTO requests (date, ip, request, agent) VALUES(?, ?, ?, ?)""",
                    (date, ip, req, user_agent))
        db.commit()


app = Flask(__name__)


def get_photos_links_from_folder(folder_path="static/images/gallery"):
    images_urls = sorted([f'{folder_path}/{name}' for name in os.listdir(folder_path) if os.path.isfile(folder_path + '/' + name)])
    return images_urls


@app.errorhandler(404)
def error_404(error):
    title = f'{error}'
    css = url_for('static', filename='styles/index.css')
    return render_template('404.html', title=title, css=css)


@app.route('/')
def index():  # put application's code here
    title = 'Фотограф Юлия Карелина фотосессии в Крыму'
    css = url_for('static', filename='styles/index.css')
    add_request_to_db()
    return render_template('index.html', title=title, css=css)


@app.route('/gallery')  # not used in html topnav!!!
def samples():
    title = 'Галерея'
    css = url_for('static', filename='styles/index.css')
    photos_list = get_photos_links_from_folder()
    add_request_to_db()
    return render_template('gallery.html', title=title, css=css, images_urls=photos_list)


@app.route('/about/')
@app.route('/about')
def about():
    add_request_to_db()
    # title = 'Обо мне'
    return 'Я фотограф'


@app.route('/gallery/<gallery_id>')
def gallery(gallery_id):
    title = f'Галерея {gallery_id}'
    css = url_for('static', filename='styles/index.css')
    if gallery_id in os.listdir('static/images/gallery'):
        print(request.path)
        photos_list = get_photos_links_from_folder('static/images/gallery/' + gallery_id)
        add_request_to_db()
        return render_template('gallery.html', title=title, css=css, images_urls=photos_list)
    return error_404()


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():  # put application's code here
    add_request_to_db()
    title = 'Оставить отзыв'
    css = url_for('static', filename='styles/index.css')
    client_contact = None  # Сюда примем контакт клиента.
    client_message = None  # Сюда примем сообщение клиента.
    server_message = None  # А сюда запишем сообщение от сервера.
    if request.method == 'POST':  # ну тут всё ясно, наверное.
        # Принимаем строку из формы с именем 'contact' и записываем в переменную, прилетает строка.
        client_contact = request.form.get('contact')
        # Принимаем строку из формы с именем 'message' и записываем в переменную, прилетает строка.
        client_message = request.form.get('message')
    # Если сообщение от клиента не пустое, то составляем строку-сообщение, что отзыв отправлен.
    if client_message != '' and client_contact != '' and client_message != None and client_contact != None:
        server_message = f'Вы добавили отправили контакт {client_contact} и сообщение {client_message}'
        print('Контакт клиента', client_contact)
        print('Сообщение клиента', client_message)
        add_message_in_db(client_contact, client_message)
    return render_template('leave_feedback.html', message=server_message, title=title, css=css)

@app.route('/insta')
def insta():
    add_request_to_db()
    return redirect("https://instagram.com/karelina_foto/", code=302)


@app.route('/vk')
def vk():
    add_request_to_db()
    return redirect("https://vk.com/karelinajulietta", code=302)


@app.route('/matinee_price')
def matinee_price():
    title = 'Цены на утренники'
    css = url_for('static', filename='styles/index.css')
    add_request_to_db()
    return render_template('matinee_price.html', title=title, css=css)


@app.route('/photosession_price')
def photosession_price():
    title = 'Цены на фотопроекты'
    css = url_for('static', filename='styles/index.css')
    add_request_to_db()
    return render_template('photosession_price.html', title=title, css=css)


if __name__ == '__main__':
    app.run(debug=True)
