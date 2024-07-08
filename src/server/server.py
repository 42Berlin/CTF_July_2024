import subprocess
import jwt
import datetime
import os

from functools import wraps
from multiprocessing import Process
from flask import Flask, request, redirect, url_for, render_template_string, make_response, abort, send_file


flag_app = Flask(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CUEgEDR1Vsw1yTgEhXWawE2v1CKA+N/tPPmtlyQqaiE='


# FLAG FOUND! -> MyFlag{fjb73j_sj}
USERNAME = 'administrator'
PASSWORD = 'Best42TeamEver'

FILE_DIRECTORY = '/home/adrian/app/files'


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            token = jwt.encode({
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            response = make_response(redirect(url_for('home')))
            response.set_cookie('token', token)
            return response
        else:
            return "Invalid credentials"
    
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <title>Admin Login</title>
      </head>
      <body>
        <div class="container">
          <div class="row mt-5">
            <div class="col-md-6 offset-md-3">
              <h1>Admin Login</h1>
              <form method="post">
                <div class="form-group">
                  <label for="username">Username:</label>
                  <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="form-group">
                  <label for="password">Password:</label>
                  <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
              </form>
            </div>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
      </body>
    </html>
    ''')


@app.route('/keepGoingYouGettingBetter')
def flag_fuzzing():
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <title>Fuzzing Flag!</title>
      </head>
      <body>
        <div class="container">
          <div class="row mt-5">
            <div class="col-md-6 offset-md-3">
              <h1>FLAG FOUND! MyFlag{K4M1ql_6x}</h1>
            </div>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
      </body>
    </html>
    '''


@app.route('/admin', methods=['GET', 'POST'])
@token_required
def home():
    result = ''
    if request.method == 'POST':
        command = request.form['command']
        try:
            result = subprocess.run(f'./check_command.sh {command}', shell=True, capture_output=True, text=True).stdout
        except subprocess.CalledProcessError as e:
            result = f"Error executing command: {e}"
    
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
      <title>Admin Command Tool</title>
      <style>
        .result-box {
          background-color: #f8f9fa;
          border: 1px solid #dee2e6;
          padding: 20px;
          border-radius: 5px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="row mt-5">
          <div class="col-md-12">
            <h1>Admin Command Tool</h1>
            <p>This tool allows administrators to check the system sttaus. Please enter one of the following commands:</p>
            <ul>
              <li>STATUS: Displays current system uptime.</li>
              <li>DISK: Displays disk usage information.</li>
              <li>CPU: Displays CPU usage information.</li>
            </ul>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col-md-6">
            <form method="post">
              <div class="form-group">
                <label for="command">Command:</label>
                <input type="text" class="form-control" id="command" name="command" placeholder="Enter command">
              </div>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
          </div>
          <div class="col-md-6">
            <div class="result-box">
              <h3>Result</h3>
              <p>{{ result }}</p>
            </div>
          </div>
        </div>
      </div>
      <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
      <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    </body>
    </html>
    ''', result=result)


@app.route('/<path:req_path>')
def dir_listing(req_path):
    abs_path = os.path.join(FILE_DIRECTORY, req_path)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = os.listdir(abs_path)
    
    return render_template_string('''
    <ul>
      {% for file in files %}
      <li>
          <a href="{{ (request.path + '/' if request.path != '/' else '') + file }}">
              {{ (request.path + '/' if request.path != '/' else '') + file }}
          </a>
      </li>
      {% endfor %}
    </ul>
    ''', files=files)


@app.route('/')
def root():
    return redirect(url_for('home'))


@flag_app.route('/')
def flag_root():
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <title>Port Scanning Flag!</title>
      </head>
      <body>
        <div class="container">
          <div class="row mt-5">
            <div class="col-md-6 offset-md-3">
              <h1>FLAG FOUND! MyFlag{PmRf31_sj}</h1>
            </div>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
      </body>
    </html>
    '''


def run_admin_server():
    app.run(host='0.0.0.0', port=4242)


def run_flag_server():
    flag_app.run(host='0.0.0.0', port=42424)


if __name__ == "__main__":
    admin_server = Process(target=run_admin_server)
    flag_server = Process(target=run_flag_server)

    admin_server.start()
    flag_server.start()

    admin_server.join()
    flag_server.join()
