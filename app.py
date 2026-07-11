import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_admin import Admin

app = Flask(__name__, static_folder='static')

# تصاویر محفوظ کرنے کا فولڈر (Vercel پر یہ صرف عارضی کام کرے گا)
UPLOAD_FOLDER = os.path.join('/tmp', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# ایڈمن پینل شروع کریں
admin = Admin(app, name='Bintehouse Admin', template_mode='bootstrap4')

# Vercel کے لیے ڈیٹا بیس کو /tmp فولڈر میں شفٹ کیا گیا ہے تاکہ کریش نہ ہو
DB_PATH = os.path.join('/tmp', 'database.db')

def init_db():
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

# ایپ چلنے سے پہلے ڈیٹا بیس بنا دیں
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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if title and content:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, image_path) VALUES (?, ?, ?)', 
                       (title, content, filename))
        conn.commit()
        conn.close()
        return "<h1>Success! Article with Image Uploaded.</h1><br><a href='/admin-upload'>Upload Another</a>"
    return "Error: Title and Content are required!", 400

@app.route('/api/articles')
def get_articles():
    try:
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
