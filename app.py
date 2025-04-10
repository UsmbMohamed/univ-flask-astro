from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = "clé_secrete"

db = SQLAlchemy(app)

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

        else:

            return redirect(url_for("home"))
            flash("Inscription réussie (simulée, sans base de données).", "success")


    return render_template('inscription.html')

def get_accounts():
    accounts = {}
    with open("compte.txt", "r") as f:
        for line in f:
            email, password = line.strip().split(":")
            accounts[email] = password
    return accounts


@app.route("/connexion", methods=["GET", "POST"])
def connexion():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(f"Tentative de connexion avec {email}.")
        
        accounts = get_accounts()  

        if email in accounts and accounts[email] == password:
            return redirect(url_for("home"))
            flash(f"Connexion réussie pour {email}.", "success")

        else:
            flash("Erreur de connexion : mail ou mot de passe incorrect.", "danger")
            return redirect(url_for("connexion"))

    return render_template('connexion.html')



if __name__ == "__main__":
    app.run(debug=True)
