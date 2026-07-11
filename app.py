import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_admin import Admin # Flask-Admin امپورٹ کریں

app = Flask(__name__, static_folder='static')

# تصاویر محفوظ کرنے کا فولڈر سیٹ کریں
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# ایڈمن پینل شروع کریں
admin = Admin(app, name='Bintehouse Admin', template_mode='bootstrap4')

# ڈیٹا بیس کو شروع کرنا (تصویر کے کالم کے ساتھ)
def init_db():
    conn = sqlite3.connect('database.db')
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

init_db()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/blog')
def blog():
    # بلاگ دکھانے کے لیے آپ render_template بھی استعمال کر سکتی ہیں
    return send_from_directory('.', 'blog.html')

@app.route('/admin-upload')
def admin_page():
    return send_from_directory('.', 'upload.html')

# نیا آرٹیکل اور تصویر اپ لوڈ کرنے کا راستہ
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
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, image_path) VALUES (?, ?, ?)', 
                       (title, content, filename))
        conn.commit()
        conn.close()
        return "<h1>Success! Article with Image Uploaded.</h1><br><a href='/admin-upload'>Upload Another</a>"
    return "Error: Title and Content are required!"

# ڈیٹا بیس سے تمام آرٹیکلز حاصل کرنے کی API
@app.route('/api/articles')
def get_articles():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY id DESC')
    articles = cursor.fetchall()
    
    output = # یہاں بریکٹ کا اضافہ کر کے سنٹیکس ایرر ٹھیک کیا گیا ہے
    for article in articles:
        output.append({
            'title': article['title'], 
            'content': article['content'],
            'image_path': article['image_path']
        })
    conn.close()
    return jsonify(output)

if __name__ == '__main__':
    # پورٹ 5000 پر سرور چلانا
    app.run(debug=True, port=5000)
