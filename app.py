import os
from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client

app = Flask(__name__, static_folder='static')

# -----------------------------------------------------------------
# 1. SUPABASE INTEGRATION (CLOUD DATABASE)
# -----------------------------------------------------------------
# Apne Supabase Dashboard se URL aur Anon Key yahan paste karein
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"  # <-- Apni real anon key yahan likhein

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# -----------------------------------------------------------------
# 2. HTML PAGES ROUTES
# -----------------------------------------------------------------
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/blog')
def blog():
    return send_from_directory('.', 'blog.html')

@app.route('/admin-upload')
def admin_page():
    return send_from_directory('.', 'upload.html')


# -----------------------------------------------------------------
# 3. ARTICLES / BLOGS ACTIONS (DATA STORAGE & FETCHING)
# -----------------------------------------------------------------

# Naya Article Add Karne ka Route (Admin Page Se Data Cloud Par Bhejne K Liye)
@app.route('/add-article', methods=['POST'])
def add_article():
    title = request.form.get('title')
    content = request.form.get('content')
    
    # Image name handle karna (Baad mein aap isay Supabase Storage se connect kar sakti hain)
    filename = "" 
    file = request.files.get('image')
    if file and file.filename != '':
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)

    if title and content:
        try:
            # Supabase ke 'blogs' table mein data insert karein
            data = {
                "title": title,
                "content": content,
                "image_url": filename  # Aap ke database column ka naam image_url hai
            }
            supabase.table("blogs").insert(data).execute()
            
            return "<h1>Success! Article Uploaded to Cloud Database.</h1><br><a href='/admin-upload'>Upload Another</a>"
        except Exception as e:
            return f"Supabase Cloud Error: {str(e)}", 500
            
    return "Error: Title and Content are required!", 400


# Frontend Blog Page Par Articles Dikhane Ki API
@app.route('/api/articles')
def get_articles():
    try:
        # Supabase ke 'blogs' table se saara data load karein (Naye articles pehle ayen ge)
        response = supabase.table("blogs").select("*").order("id", desc=True).execute()
        articles = response.data
        
        output = []
        for article in articles:
            output.append({
                'title': article.get('title'), 
                'content': article.get('content'),
                'image_path': article.get('image_url')  # Frontend JS ko purana format hi bhej rahe hain
            })
            
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------------
# 4. AI TOOLS ACTIONS (WEBSITE DIRECTORY K LIYE)
# -----------------------------------------------------------------

# AI Tools Ko Website Par Render/Dikhane Ki API
@app.route('/api/ai-tools')
def get_ai_tools():
    try:
        # Supabase ke 'ai-tools' table se saara data utha kar lao
        response = supabase.table("ai-tools").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Vercel cloud architecture k liye application entrance entry 
app.wsgi_app = app.wsgi_app 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
