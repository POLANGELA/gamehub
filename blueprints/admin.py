from flask import Blueprint, render_template, redirect, session, flash, url_for
from extensions import db
from models import Game

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/pending')
def pending():
    if session.get('role') != 'admin':
        flash("Accesso riservato all'amministratore.")
        return redirect(url_for('home_redirect'))
    games = Game.query.filter_by(approved=False).all()
    return render_template('admin_pending.html', games=games)
