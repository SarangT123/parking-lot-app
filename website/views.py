from flask import Flask, Blueprint, render_template, redirect, url_for, request, session
import csv

from datetime import timedelta
from flask.helpers import flash


views = Blueprint('views', __name__)


@views.before_request
def make_session_permanent():
    session.permanent = True
    views.permanent_session_lifetime = timedelta(hours=100)


users = "website/static/Users.csv"
email = "website/static/Email.csv"


@views.route('/')
def home():
    print(session['name'])
    if 'token' in session:
        return redirect('/login')
    else:
        return redirect('/register')


@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        with open(users, 'r+') as csvfile:
            reader = csv.reader(csvfile)
            fields = []
            fields = next(reader)
            Tokens = []
            for row in reader:
                Tokens.append(row)
            usr_token = [
                f"{request.form['Name']}*#z{request.form['Password']}"]
            if usr_token in Tokens:
                return render_template("auth.html")
            else:
                with open(email, 'r+') as emailreader:
                    reader = csv.reader(emailreader)
                    feilds = []
                    feilds = next(reader)
                    emails = []
                    for row in reader:
                        emails.append(row)
                    usr_email = [str(request.form['Email'])]
                    if usr_email in emails:
                        return render_template('auth.html')
                    else:
                        writer = csv.writer(csvfile)
                        token_w = [
                            [f"{request.form['Name']}*#z{request.form['Password']}"]]
                        writer.writerows(token_w)
                        writer = csv.writer(emailreader)
                        email_w = [[str(request.form['Email'])]]
                        writer.writerows(email_w)
                        session['token'] = usr_token
                        session['name'] = [f"{request.form['Name']}"]
                        flash('Woo! Logged you in Enjoy!')
                        return redirect('/login')

    else:
        return render_template("auth.html", LR="Register")


@views.route('/login', methods=['GET', 'POST'])
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


@views.route('/logout')
def logout():
    if 'token' in session and 'name' in session:
        session.pop('token')
        session.pop('name')
    flash('You have been logged out')
    return redirect('/login')
