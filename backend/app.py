from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configuration SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trash2treasure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle Utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)

# Modèle Annonce
class Annonce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prix = db.Column(db.Float, nullable=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)

# Modèle Message
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    utilisateur_id_envoyeur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    utilisateur_id_destinataire = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation avec les utilisateurs
    utilisateur_envoyeur = db.relationship('Utilisateur', foreign_keys=[utilisateur_id_envoyeur])
    utilisateur_destinataire = db.relationship('Utilisateur', foreign_keys=[utilisateur_id_destinataire])

# Route d'inscription
@app.route('/inscription', methods=['POST'])
def inscription():
    data = request.get_json()
    nom = data['nom']
    email = data['email']
    mot_de_passe = bcrypt.generate_password_hash(data['mot_de_passe']).decode('utf-8')

    nouvel_utilisateur = Utilisateur(nom=nom, email=email, mot_de_passe=mot_de_passe)
    db.session.add(nouvel_utilisateur)
    db.session.commit()

    return jsonify({"message": "Inscription réussie"}), 201

# Route de connexion
@app.route('/connexion', methods=['POST'])
def connexion():
    data = request.get_json()
    email = data['email']
    mot_de_passe = data['mot_de_passe']

    utilisateur = Utilisateur.query.filter_by(email=email).first()

    if utilisateur and bcrypt.check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
        return jsonify({"message": "Connexion réussie", "utilisateur_id": utilisateur.id}), 200
    else:
        return jsonify({"message": "Email ou mot de passe incorrect"}), 401

# Route pour créer une annonce
@app.route('/annonce', methods=['POST'])
def creer_annonce():
    data = request.get_json()
    titre = data['titre']
    description = data['description']
    prix = data.get('prix', None)
    utilisateur_id = data['utilisateur_id']

    nouvelle_annonce = Annonce(titre=titre, description=description, prix=prix, utilisateur_id=utilisateur_id)
    db.session.add(nouvelle_annonce)
    db.session.commit()

    return jsonify({"message": "Annonce créée avec succès"}), 201

# Route pour récupérer toutes les annonces
@app.route('/annonces', methods=['GET'])
def obtenir_annonces():
    annonces = Annonce.query.all()  # Récupérer toutes les annonces
    annonces_list = []
    
    for annonce in annonces:
        annonces_list.append({
            "id": annonce.id,
            "titre": annonce.titre,
            "description": annonce.description,
            "prix": annonce.prix,
            "utilisateur_id": annonce.utilisateur_id
        })
    
    return jsonify(annonces_list), 200

# Route pour envoyer un message
@app.route('/message', methods=['POST'])
def envoyer_message():
    print("Route /message appelée")  # Ajout du print pour déboguer
    data = request.get_json()
    contenu = data['contenu']
    utilisateur_id_envoyeur = data['utilisateur_id_envoyeur']
    utilisateur_id_destinataire = data['utilisateur_id_destinataire']

    message = Message(
        contenu=contenu,
        utilisateur_id_envoyeur=utilisateur_id_envoyeur,
        utilisateur_id_destinataire=utilisateur_id_destinataire
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message envoyé avec succès"}), 201

# Route pour récupérer les messages d'un utilisateur
@app.route('/messages/<int:utilisateur_id>', methods=['GET'])
def obtenir_messages(utilisateur_id):
    print(f"Route /messages/{utilisateur_id} appelée")  # Ajout du print pour déboguer
    messages = Message.query.filter(
        (Message.utilisateur_id_envoyeur == utilisateur_id) | 
        (Message.utilisateur_id_destinataire == utilisateur_id)
    ).all()

    messages_list = []
    for message in messages:
        messages_list.append({
            "id": message.id,
            "contenu": message.contenu,
            "utilisateur_envoyeur": message.utilisateur_envoyeur.nom,
            "utilisateur_destinataire": message.utilisateur_destinataire.nom,
            "date_envoi": message.date_envoi.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(messages_list), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Assure que les tables sont créées
    app.run(debug=True)
