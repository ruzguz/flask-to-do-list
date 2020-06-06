from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from app.forms import LoginForm, TodoForm, DeleteForm, UpdateForm
import unittest
from app import create_app
from app.firestore_service import get_users, get_todos, create_todo, delete_todo, update_todo
from flask_login import login_required, current_user


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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    # Getting user info
    user_ip = session.get('user_ip')
    username = current_user.username
    todo_form = TodoForm()
    delete_form = DeleteForm()
    update_form = UpdateForm()


    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form 
    }

    if todo_form.validate_on_submit():
        description = todo_form.description.data

        create_todo(username, description)
        flash('Task created successfully')

    return render_template('hello.html', **context)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.username
    delete_todo(user_id, todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.username
    update_todo(user_id, todo_id, done)
    return redirect(url_for('hello'))

## Error handlers

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html', error=error)