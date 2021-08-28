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
lots_info = "website/static/lot.data"


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
        session['token'] = token
        session['name'] = name
        return redirect('/dashboard')
    else:
        if 'token' in session and 'name' in session:
            print('session login')
            return redirect('/dashboard')
        else:
            return render_template('login.html')


@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        data = open(lots_info, 'r')
        display = data.read().split('^')
        data.close()
        if request.form['Search'] in display:
            return redirect(f"/lots/{str(request.form['Search'])}")
        else:
            flash('No lots found in that location')
            return render_template('MM.html')
    else:
        if 'token' in session and 'name' in session:
            token = session['token']
            name = session['name']
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
                    session.pop('token')
                    session.pop('name')
                    flash(
                        "That username or password doesn't match with our's ! Is that a typo?")
                    return redirect('/login')
        else:
            return redirect('/login')


@views.route('/lots/<pin>')
def lots(pin):
    print(pin)
    data = open(lots_info, 'r')
    display = data.read().split('^')
    data.close()
    print(display)
    matches = []
    for i in range(len(display)):
        if display[i] == pin:
            matches.append(i)
    display_id = []
    display_name = []
    print(matches)
    for i in range(len(matches)):
        display_id.append(display[int(matches[i])+1])
        display_name.append(display[int(matches[i])+2])
    print(display_id)
    print(display_name)
    return render_template('lots.html', lot_name=display_name, lot_id=display_id)


@views.route('/logout')
def logout():
    if 'token' in session and 'name' in session:
        session.pop('token')
        session.pop('name')
    flash('You have been logged out')
    return redirect('/login')
