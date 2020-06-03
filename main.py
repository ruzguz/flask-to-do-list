from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from app.forms import LoginForm
import unittest
from app import create_app
from app.firestore_service import get_users, get_todos
from flask_login import login_required


## app configuration
app = create_app()

## Commands
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

## Routes
@app.route('/')
def index():
    # Getting user IP and save it in a cookie
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello')
@login_required
def hello():
    # Getting user info
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    return render_template('hello.html', **context)

## Error handlers

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html', error=error)