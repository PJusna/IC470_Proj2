import http.server
import socketserver
import sqlite3
import urllib.parse
import os

PORT = 8000  # Port to run the server

# Function to create the database and table if they don't exist
def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            attributes TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the SQLite database
def insert_submission(name, message, attributes):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO submissions (name, message, attributes) VALUES (?, ?, ?)', (name, message, attributes))
        conn.commit()
        conn.close()
        print(f"Inserted: {name}, {message}, {attributes}")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")

# Function to get all submissions from the database
def get_all_submissions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions')
    submissions = cursor.fetchall()
    conn.close()
    return submissions

# Function to render the HTML for the database page
def render_database_page():
    submissions = get_all_submissions()
    submissions_html = ""
    for submission in submissions:
        submissions_html += f"<tr><td>{submission[0]}</td><td>{submission[1]}</td><td>{submission[2]}</td><td>{submission[3]}</td></tr>"
    with open('database.html', 'r') as file:
        page = file.read()
    page = page.replace("{{ submissions }}", submissions_html)
    return page

# Custom request handler to process GET and POST requests
class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())  # Send the HTML form to the client
        elif self.path == '/database':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # get database
            database_page = render_database_page()
            self.wfile.write(database_page.encode())
            #with open('database.html', 'rb') as file:
                #self.wfile.write(file.read())
        elif self.path.startswith('/css/'):  # Serve CSS files from the /css folder
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            css_file = os.path.join(os.getcwd(), self.path[1:])  # Get the correct file path
            with open(css_file, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            name = post_data.get('name', [''])[0]
            message = post_data.get('message', [''])[0]
            attributes = post_data.get('attributes', [''])[0]

            insert_submission(name, message, attributes)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Thank you for your submission!")

# Create the server and handle requests
create_table()  # Ensure the table exists before starting the server

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving HTTP on port {PORT}")
    httpd.serve_forever()

