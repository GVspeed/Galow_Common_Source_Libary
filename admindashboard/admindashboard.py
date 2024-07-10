from flask import Flask, session, redirect, url_for, render_template_string
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

admin_dashboard_page = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Administrator Dashboard</title>
    <style>
      body, html {
        height: 100%;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Arial, sans-serif;
        background-color: #2f3136;
        color: white;
      }
    </style>
  </head>
  <body>
    <h1>Administrator Dashboard</h1>
  </body>
</html>
'''

@app.route('/admindashboard&online=true')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect("http://127.0.0.1:5000/adminportal")
    return render_template_string(admin_dashboard_page)

if __name__ == '__main__':
    app.run(debug=True, port=5001)