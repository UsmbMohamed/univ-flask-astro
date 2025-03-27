from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route("/")
def home():
    """HTML Index page"""
    return render_template('index.html')

@app.route("/appareil-photo")
def appareils():
    """HTML appareil-photo page"""
    return render_template('appareils.html')

@app.route("/telescopes")
def telescopes():
    """HTML telescope page"""
    return render_template('telescopes.html')

@app.route("/photographies")
def photos():
    """HTML photo page"""
    return render_template('photos.html')

@app.route("/connexion")
def connexion():
    """HTML connexion page"""
    return render_template('connexion.html')

@app.route("/inscription")
def inscription():
    """HTML inscription page"""
    return render_template('inscription.html')


if __name__ == "__main__":
    app.run(debug=True)
