from flask import Flask, request, make_response, redirect

app = Flask(__name__)

@app.route('/')
def index():
    # Getting user IP and save it in a cookie
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response



@app.route('/hello')
def hello():
    # Getting user IP
    user_ip = request.cookies.get('user_ip')
    
    return('Hello world from Flask!!! - Your IP is {}'.format(user_ip))