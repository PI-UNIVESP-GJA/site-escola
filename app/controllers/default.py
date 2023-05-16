from flask import render_template, redirect, url_for
from app import app, db, login_manager
from sqlalchemy import asc, and_
import json



@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout/')
def logout():
    logout_user()
    error = "Sessão encerrada com sucesso"
    return render_template('index.html', error=error)