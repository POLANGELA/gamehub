
from extensions import db
from app import app
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    # Verifica se l'amministratore esiste già
    if not User.query.filter_by(username='amministratore').first():
        admin = User(
            username='amministratore',
            password=generate_password_hash('28091997'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Utente amministratore creato.")
    else:
        print("ℹ️ Utente amministratore già esistente.")

    print("✅ Database inizializzato.")
