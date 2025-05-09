from flask import Flask, render_template, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = 'f9a8d6c7413f4e3c9c7a9a84e17db5f6'  # Secure key for session

# GitHub OAuth credentials (replace with your actual keys)
GITHUB_CLIENT_ID = 'Ov23lioN9ML67y2VsT1V'
GITHUB_CLIENT_SECRET = '6b10cc364a33441dac00a3360e57cbcd4d12bc68'

# Home route (login page)
@app.route('/')
def login():
    return render_template('login.html')

# Signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# GitHub OAuth login (forces re-authentication using unique state)
@app.route('/login/github')
def login_github():
    session.clear()  # Clear session to enforce fresh login
    github_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&scope=read:user"
        f"&allow_signup=false"
        f"&redirect_uri=http://localhost:5000/login/github/callback"
        f"&state=force_login"  # Optional: adds uniqueness to force consent
    )
    return redirect(github_url)

# GitHub callback route
@app.route('/login/github/callback')
def github_callback():
    code = request.args.get('code')

    if not code:
        return "Authorization failed: No code returned."

    # Exchange code for access token
    token_res = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code
        },
        headers={'Accept': 'application/json'}
    )

    token_json = token_res.json()
    access_token = token_json.get('access_token')

    if not access_token:
        return "Authorization failed: No access token received."

    # Get user info from GitHub
    user_res = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': f'token {access_token}'}
    )
    user_info = user_res.json()

    # Store user info in session
    session['user'] = user_info

    return render_template('dashboard.html', user=user_info)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
