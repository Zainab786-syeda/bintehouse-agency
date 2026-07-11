import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

# تصاویر محفوظ کرنے کا فولڈر
UPLOAD_FOLDER = os.path.join('/tmp', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# کلاؤڈ کے لیے ڈیٹا بیس کا راستہ
DB_PATH = os.path.join('/tmp', 'database.db')

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database init error: {e}")

# ایپ لوڈ ہونے پر ڈیٹا بیس سیٹ کریں
init_db()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/blog')
def blog():
    return send_from_directory('.', 'blog.html')

@app.route('/admin-upload')
def admin_page():
    return send_from_directory('.', 'upload.html')

@app.route('/add-article', methods=['POST'])
def add_article():
    title = request.form.get('title')
    content = request.form.get('content')
    file = request.files.get('image')
    
    filename = ""
    if file and file.filename != '':
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if title and content:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (title, content, image_path) VALUES (?, ?, ?)', 
                           (title, content, filename))
            conn.commit()
            conn.close()
            return "<h1>Success! Article Uploaded.</h1><br><a href='/admin-upload'>Upload Another</a>"
        except Exception as e:
            return f"Database Error: {str(e)}", 500
    return "Error: Title and Content are required!", 400

@app.route('/api/articles')
def get_articles():
    try:
        if not os.path.exists(DB_PATH):
            return jsonify([])
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles ORDER BY id DESC')
        articles = cursor.fetchall()
        
        output = []
        for article in articles:
            output.append({
                'title': article['title'], 
                'content': article['content'],
                'image_path': article['image_path']
            })
        conn.close()
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel کلاؤڈ کے لیے انٹری پوائنٹ فراہم کرنا
app.wsgi_app = app.wsgi_app 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
