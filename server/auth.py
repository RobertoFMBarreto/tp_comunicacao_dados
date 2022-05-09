from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    if not request.user_agent.platform:
        data = request.get_json()
        email = data['email']
        names = data['name'].split(" ")
        fullName = ''
        for i in range(0, len(names)):
            if i < len(names) - 1:
                fullName += names[i].capitalize() + " "
            else:
                fullName += names[i].capitalize()
        password = data['password']

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            return "Email já existe", 400

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=fullName,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return "OK"
    else:
        email = request.form.get('email')
        names = request.form.get('name').split(" ")
        fullName = ''
        for i in range(0, len(names)):
            if i < len(names) - 1:
                fullName += names[i].capitalize() + " "
            else:
                fullName += names[i].capitalize()

        password = request.form.get('password')

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email já em utilização')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=fullName,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    if not request.user_agent.platform:
        data = request.get_json()
        # login code goes here
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            # if the user doesn't exist or password is wrong, reload the page
            return 'Erro! Por favor verifique as suas credenciais e tente denovo.', 400

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=False)
        return "OK"

    else:
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Erro! Por favor verifique as suas credenciais e tente denovo.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('auth.login'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "OK" if not request.user_agent.platform else redirect(url_for('main.index'))
