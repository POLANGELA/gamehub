from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from extensions import db
from models import Game, User

games_bp = Blueprint('games', __name__)

@games_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session or session.get('role') != 'developer':
        flash("Solo gli sviluppatori possono caricare giochi.")
        return redirect(url_for('home_redirect'))
    if request.method == 'POST':
        g = Game(title=request.form['title'], author=session['user'], approved=False)
        db.session.add(g)
        db.session.commit()
        flash("Gioco caricato. In attesa di approvazione.")
        return redirect(url_for('games.upload'))
    return render_template('upload.html')


@games_bp.route('/home')
def home():
    return render_template('index.html')
