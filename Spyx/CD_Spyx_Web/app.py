from config import CLIENT_SECRET, TOKEN, OAUTH_URL, REDIRECT_URL
from flask import  Flask, render_template, request, session, redirect
from zenora import APIClient

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SECRET_KEY"] = "0123"
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)

@app.route('/')
def home():
    if 'token' in session:
        bearer_client = APIClient(session['token'], bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template('index.html', current_user=current_user)

    return render_template("index.html", oauth_url=OAUTH_URL)

@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, REDIRECT_URL).access_token
    session['token'] = access_token
    return redirect('/')

@app.route("/login")
def login():
    return render_template("login.html", oauth_url=OAUTH_URL)

@app.route("/invite")
def invite():
    if 'token' in session:
        return render_template("invite.html", oauth_url=OAUTH_URL)
    else:
        return render_template("login.html", oauth_url=OAUTH_URL)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)