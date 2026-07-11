from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')

# 1. ڈیٹا بیس اور ٹیبل بنانے کا فنکشن
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # یہاں ہم ایک ٹیبل بنا رہے ہیں جس میں آرٹیکلز کا ڈیٹا سیو ہوگا
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ڈیٹا بیس کو شروع کرنا
init_db()

# 2. ہوم پیج کا راستہ
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# 3. بلاگ پیج کا راستہ (یہاں ڈیٹا بیس سے آرٹیکلز نظر آئیں گے)
@app.route('/blog')
def blog():
    return send_from_directory('.', 'blog.html')

# 4. خفیہ اپلوڈ پیج کا راستہ (جہاں آپ فارم کھولیں گی)
@app.route('/admin-upload')
def admin_page():
    return send_from_directory('.', 'upload.html')

# 5. فارم کا ڈیٹا وصول کر کے ڈیٹا بیس میں سیو کرنے کا راستہ
@app.route('/add-article', methods=['POST'])
def add_article():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return "<h1>Success! Article uploaded to Database.</h1><br><a href='/admin-upload'>Upload Another</a>"
    return "Error: Title and Content are required!"

if __name__ == '__main__':
    print("Bintehouse Python Backend with Database is starting...")
    app.run(debug=True, port=5000)
