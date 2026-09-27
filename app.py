from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'cyber_shield_super_secret_key_2026'

# ডেমো ইউজার স্টোর (টেস্টিংয়ের জন্য)
users_db = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash("All fields are required!")
            return redirect(url_for('register'))

        if username in users_db:
            flash("Operator identity already exists!")
            return redirect(url_for('register'))

        # পাসওয়ার্ড সেভ করা
        users_db[username] = password
        flash("Registration successful! Authorize your access.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if username in users_db and users_db[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials or unauthorized node!")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)