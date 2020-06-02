from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap


## app configuration
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'DONT TELL THE SECRET'


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


@app.route('/hello')
def hello():
    # Getting user IP
    user_ip = session.get('user_ip')
    
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }
    
    return render_template('hello.html', **context)

## Error handlers

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html', error=error)