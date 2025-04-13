from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = "clé_secrete"


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categorie = db.Column(db.String(100), nullable=False)
    marque = db.Column(db.String(100), nullable=False)
    modele = db.Column(db.String(100), nullable=False)
    date_sortie = db.Column(db.String(10), nullable=False)
    score = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Camera('{self.categorie}', '{self.marque}', '{self.modele}')"


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/appareil-photo")
def appareils():
    return render_template('appareils.html')


@app.route("/telescopes")
def telescopes():
    return render_template('telescopes.html')


@app.route("/photographies")
def photos():
    return render_template('photos.html')


"""flask shell 
    >>> from app impoer db
    >>> db.create_all()
    >>> exit"""

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        print("----- Nouvelle tentative d'inscription -----")
        print(f"Nom d'utilisateur : {username}")
        print(f"Email : {email}")

        if password != password_confirm:
            flash("Erreur : les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("inscription"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "warning")
            return redirect(url_for("inscription"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))
        flash("Inscription réussie.", "success")

    return render_template('inscription.html')


@app.route("/connexion", methods=["GET", "POST"])
def connexion():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(f"Tentative de connexion avec {email}.")
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for("home"))
            flash(f"Connexion réussie pour {email}.", "success")

        else:
            flash("Erreur de connexion : mail ou mot de passe incorrect.", "danger")
            return redirect(url_for("connexion"))

    return render_template('connexion.html')



if __name__ == "__main__":
    app.run(debug=True)
