from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from app.forms import LoginForm
import unittest
from app import create_app


## app configuration
app = create_app()

## Commands
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


## Vars
todos = [ 'TODO 1', 'TODO 2', 'TODO 3' ]

## Routes
@app.route('/')
def index():
    # Getting user IP and save it in a cookie
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # Getting user info
    user_ip = session.get('user_ip')
    username = session.get('username')

    # Instantiate login form
    login_form = LoginForm()

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Username registered successfully')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)

## Error handlers

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html', error=error)