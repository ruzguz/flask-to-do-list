from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user

from app.forms import LoginForm
from app.firestore_service import get_user
from app.models import UserModel, UserData

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': LoginForm(),
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        # Get user from database
        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            # Getting password from DB
            password_from_db = user_doc.to_dict()['password']

            # Check is password is correct
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Welcome back')

                redirect(url_for('hello'))
            else: # wrong password
                flash('Wrong password')
        else: # User not found
            flash('User doesn\'t exists')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Come back soon!!!')

    return redirect(url_for('auth.login'))

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form,
    }

    if signup_form.validate_on_submit():
        pass

    return render_template('signup.html', **context)

