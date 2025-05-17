from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os, random, zipfile
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = 'uploads'
GAMES_FOLDER = 'static/games'
ALLOWED_EXTENSIONS = {'zip'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GAMES_FOLDER, exist_ok=True)

users = {}
games = []
played_stats = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    username = session.get('user')
    stats = {}
    if username:
        stats = played_stats.get(username, {'total': 0, 'played': 0})
    return render_template('index.html', user=username, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            flash("Username già registrato.")
            return redirect(url_for('register'))
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        users[username] = {'password': password, 'role': role}
        played_stats[username] = {'total': 0, 'played': 0}
        flash("Registrazione completata.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['role'] = user['role']
            return redirect(url_for('index'))
        flash("Credenziali non valide.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session or session.get('role') != 'developer':
        flash("Accesso riservato agli sviluppatori.")
        return redirect(url_for('index'))
    if request.method == 'POST':
        file = request.files['zipfile']
        title = request.form['title'].replace(" ", "_")
        if file and allowed_file(file.filename):
            folder_path = os.path.join(GAMES_FOLDER, title)
            if os.path.exists(folder_path):
                flash("Gioco già esistente.")
                return redirect(request.url)
            temp_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            file.save(temp_path)
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                if 'index.html' not in zip_ref.namelist():
                    flash("Lo zip deve contenere un index.html.")
                    return redirect(request.url)
                os.makedirs(folder_path)
                zip_ref.extractall(folder_path)
                games.append(title)
                for user in played_stats:
                    played_stats[user]['total'] = len(games)
            os.remove(temp_path)
            flash("Gioco caricato con successo!")
            return redirect(url_for('upload'))
        else:
            flash("File non valido. Carica uno ZIP con index.html.")
    return render_template('upload.html')

@app.route('/play')
def play():
    if not games:
        return "Nessun gioco disponibile."
    selected = random.choice(games)
    user = session.get('user')
    if user:
        played_stats[user]['played'] += 1
    return render_template('play.html', game=selected)

@app.route('/fullscreen/<game>')
def fullscreen(game):
    return render_template('fullscreen.html', game=game)
