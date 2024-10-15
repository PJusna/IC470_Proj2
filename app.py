# from flask import Flask, request, render_template, redirect
# import sqlite3

# app = Flask(__name__)

# def get_db_connection():
#     conn = sqlite3.connect('mydatabase.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     posts = conn.execute('SELECT * FROM posts').fetchall()
#     conn.close()
#     return render_template('index.html', posts=posts)

# @app.route('/post', methods=['POST'])
# def post():
#     title = request.form['title']
#     content = request.form['content']
#     conn = get_db_connection()
#     conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
#     conn.commit()
#     conn.close()
#     return redirect('/')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# Peter's Redo
from flask import Flask, request, render_template, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database connection
def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page (Only accessible if logged in)
@app.route('/')
def index():
    if 'user_id' in session:
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM posts').fetchall()
        conn.close()
        return render_template('index.html', posts=posts)
    else:
        return redirect('/login')

# Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before saving
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

# Log In Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check the username and password in the database
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            return redirect('/')
        else:
            return 'Invalid credentials'

    return render_template('login.html')

# Log Out Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

# Post a new blog entry (only allowed if logged in)
@app.route('/post', methods=['POST'])
def post():
    if 'user_id' in session:
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

<<<<<<< HEAD
=======


>>>>>>> create_account-feature
