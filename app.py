import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# ڈیٹا بیس کنکشن کا فنکشن
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # ڈیٹا کو ڈکشنری کی شکل میں حاصل کرنے کے لیے
    return conn

# ڈیٹا بیس اور ٹیبل کی ابتدائی ترتیب
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# بلاگ پیج کے لیے ڈیٹا بیس سے آرٹیکلز حاصل کرنا
@app.route('/api/articles')
def get_articles():
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles ORDER BY id DESC').fetchall()
    conn.close()
    
    # ڈیٹا کو لسٹ میں تبدیل کرنا تاکہ JavaScript اسے پڑھ سکے
    output =
    for article in articles:
        output.append({'title': article['title'], 'content': article['content']})
    return jsonify(output)

# نیا آرٹیکل اپ لوڈ کرنے کا راستہ
@app.route('/add-article', methods=['POST'])
def add_article():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        conn = get_db_connection()
        conn.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return "<h1>Success! Article uploaded.</h1><br><a href='/admin-upload'>Back</a>"
    return "Error: Title and Content are required!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
