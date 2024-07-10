from flask import Flask, request, render_template_string, redirect, session, send_from_directory
from flask_session import Session
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_page = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>🌐 Administrator Verwaltung</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@400;700&display=swap');
      body, html {
        height: 100%;
        background-color: #2f3136;
        user-select: none;
        font-family: 'Helvetica Neue', Arial, sans-serif;
      }
      .container {
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .login-box {
        width: 100%;
        max-width: 400px;
        background-color: #23272a;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        color: white;
        user-select: none;
      }
      .form-control {
        background-color: #2f3136;
        border: 1px solid #2f3136;
        color: white;
        user-select: none;
        caret-color: transparent;
      }
      .form-control:focus {
        background-color: #2f3136;
        border: 1px solid #7289da;
        box-shadow: none;
      }
      .input-group-text {
        background-color: #2f3136;
        border: 1px solid #2f3136;
        color: white;
      }
      .btn-primary {
        background-color: #7289da;
        border: none;
        cursor: pointer;
      }
      .text-center {
        text-align: center;
      }
      label, h2, .alert {
        user-select: none;
      }
      .shake {
        animation: shake 0.5s;
        animation-iteration-count: 1;
      }
      @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        50% { transform: translateX(5px); }
        75% { transform: translateX(-5px); }
        100% { transform: translateX(0); }
      }
      .alert-danger {
        background-color: #ff4f4f;
        color: black;
        font-weight: bold;
      }
      .loader {
        border: 8px solid #f3f3f3;
        border-top: 8px solid #7289da;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 2s linear infinite;
        margin: 20px auto;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      .form-control::selection {
        background: none;
      }
      .form-control {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }
      .input-group-append {
        cursor: pointer;
      }
      #login-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        text-align: center;
        z-index: 1000;
        padding-top: 200px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="login-box">
        <h2 class="text-center">Login</h2>
        <form id="loginForm">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" required oncopy="return false" onpaste="return false" oncut="return false" ondrag="return false" ondrop="return false" autocapitalize="none">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-group">
              <input type="password" class="form-control" id="password" required oncopy="return false" onpaste="return false" oncut="return false" ondrag="return false" ondrop="return false">
              <div class="input-group-append">
                <span class="input-group-text" onclick="togglePassword()">
                  <i class="fas fa-eye" id="eyeIcon"></i>
                </span>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary btn-block" id="loginButton">Login</button>
        </form>
        <div id="result" class="mt-3"></div>
      </div>
    </div>
    <div id="login-overlay">
      <h2>Bitte warten...</h2>
      <div class="loader"></div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script>
      function togglePassword() {
        const passwordField = document.getElementById('password');
        const eyeIcon = document.getElementById('eyeIcon');
        if (passwordField.type === 'password') {
          passwordField.type = 'text';
          eyeIcon.classList.remove('fa-eye');
          eyeIcon.classList.add('fa-eye-slash');
        } else {
          passwordField.type = 'password';
          eyeIcon.classList.remove('fa-eye-slash');
          eyeIcon.classList.add('fa-eye');
        }
      }

      $('#loginForm').on('submit', function(event) {
        event.preventDefault();
        const username = $('#username').val();
        const password = $('#password').val();

        if (!username || !password) {
          $('#result').html('<div class="alert alert-danger">Error: Username and password are required</div>');
          return;
        }

        if (username === 'admin' && password === 'root') {
          $('#result').html('');
          $('#username').prop('disabled', true);
          $('#password').prop('disabled', true);
          $('#loginButton').prop('disabled', true);
          $('#login-overlay').css('display', 'block');
          setTimeout(function() {
            $.post('/set_session', function() {
              // Start the admin dashboard script
              fetch('/start_dashboard')
                .then(() => {
                  window.location.href = "http://127.0.0.1:5001/admindashboard&online=true";
                });
            });
          }, 3000); // Redirect to /admindashboard&online=true after 3 seconds
        } else {
          $('#result').html('<div class="alert alert-danger">Error: Invalid username or password</div>');
          $('#loginButton').addClass('shake');
          setTimeout(function() {
            $('#loginButton').removeClass('shake');
          }, 500);
        }
      });
    </script>
  </body>
</html>
'''

@app.route('/adminportal/<path:path>')
def send_adminportal(path):
    return send_from_directory('adminportal', path)

@app.route('/adminportal')
def login():
    return render_template_string(login_page)

@app.route('/set_session', methods=['POST'])
def set_session():
    session['logged_in'] = True
    return '', 204

@app.route('/start_dashboard')
def start_dashboard():
    subprocess.Popen(['python', '../admindashboard/admindashboard.py'], shell=True)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)