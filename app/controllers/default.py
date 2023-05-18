from flask import Flask, jsonify,render_template, redirect, url_for
from app import app, db, login_manager
from sqlalchemy import asc, and_
import csv
#import pandas as pd
#import numpy as np


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/")
def index():
  with open("BCG.csv") as file:
   reader = csv.reader(file, delimiter = ';')
   header = next(reader)
   return render_template("index.html", header=header, rows=reader)