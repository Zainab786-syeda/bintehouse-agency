import os  # <-- Ye line zaroor check karein ke upar add ho
from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client
from dotenv import load_dotenv  # <-- .env file read karne ke liye

# Local computer par testing ke liye .env file load karna
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')

# -----------------------------------------------------------------
# 1. SUPABASE INTEGRATION (CLOUD DATABASE) - UPDATED CODE
# -----------------------------------------------------------------
# Ab ye direct keys ke bajaye aapki .env file ya Vercel settings se automatic uthayega
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------------------------------------------
# 2. FIX HARD NAVIGATION ROUTES (404 Error Solved)
# -----------------------------------------------------------------
@app.route('/')
@app.route('/index.html')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/blog')
@app.route('/blog.html')
def blog():
    return send_from_directory('.', 'blog.html')

@app.route('/admin-upload')
@app.route('/upload.html')
def admin_page():
    return send_from_directory('.', 'upload.html')


# -----------------------------------------------------------------
# 3. ARTICLES / BLOGS ACTIONS (DATA STORAGE & FETCHING)
# -----------------------------------------------------------------
@app.route('/add-article', methods=['POST'])
def add_article():
    title = request.form.get('title')
    content = request.form.get('content')
    
    filename = "" 
    file = request.files.get('image')
    if file and file.filename != '':
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)

    if title and content:
        try:
            data = {
                "title": title,
                "content": content,
                "image_url": filename
            }
            supabase.table("blogs").insert(data).execute()
            return "<h1>Success! Article Uploaded to Cloud Database.</h1><br><a href='/admin-upload'>Upload Another</a>"
        except Exception as e:
            return f"Supabase Cloud Error: {str(e)}", 500
            
    return "Error: Title and Content are required!", 400


@app.route('/api/articles')
def get_articles():
    try:
        response = supabase.table("blogs").select("*").order("id", desc=True).execute()
        articles = response.data
        
        output = []
        for article in articles:
            output.append({
                'title': article.get('title'), 
                'content': article.get('content'),
                'image_path': article.get('image_url')
            })
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------------
# 4. AI TOOLS ACTIONS
# -----------------------------------------------------------------
@app.route('/api/ai-tools')
def get_ai_tools():
    try:
        response = supabase.table("ai-tools").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.wsgi_app = app.wsgi_app 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
