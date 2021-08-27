from flask import Flask, Blueprint, render_template, redirect, url_for, request, session
from flask.helpers import flash
import csv
owners = Blueprint('owners', __name__)

users = "website/static/Owners.csv"


@owners.route('/owners/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = [f"{request.form['Name']}*#z{request.form['Password']}"]
        name = [request.form['Name']]
        with open(users, 'r+') as csvfile:
            reader = csv.reader(csvfile)
            fields = []
            fields = next(reader)
            Tokens = []
            for row in reader:
                Tokens.append(row)
            if token in Tokens:
                session['name'] = name
                session['token'] = token
                flash('Woo! Logged you in Enjoy!')
                return render_template('MM.html', name=name)
            else:
                flash(
                    "That username or password doesn't match with our's ! Is that a typo?")
                return render_template('login.html')
    else:
        if 'token' in session and 'name' in session:
            print('session login')
            with open(users, 'r+') as csvfile:
                reader = csv.reader(csvfile)
                fields = []
                fields = next(reader)
                Tokens = []
                for row in reader:
                    Tokens.append(row)
                if session['token'] in Tokens:
                    name = session['name']
                    flash('Woo! Logged you in Enjoy!')
                    return render_template('MM.html', name=name)
                else:
                    flash(
                        "That username or password doesn't match with our's ! Is that a typo?")
                return render_template('login.html')
        else:
            return render_template('login.html')
