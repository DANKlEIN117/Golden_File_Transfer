from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)

# 🔑 Save uploads directly into Desktop/uploads
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
UPLOAD_FOLDER = os.path.join(DESKTOP, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Main HTML with gold styling
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phone ↔ PC File Transfer</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #fafafa; padding:20px; color:#333; }
        .container { max-width: 700px; margin: auto; }
        h1 { text-align:center; color: #b8860b; margin-bottom:30px; font-size: 2em; }
        .card {
            background: white; padding: 25px; margin-bottom: 25px;
            border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h2 { margin-top:0; color:#444; font-size:1.3em; }
        .custom-file {
            display: inline-block;
            background: #b8860b;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            transition: background 0.3s, transform 0.2s;
        }
        .custom-file:hover {
            background: #daa520;
            transform: scale(1.05);
        }
        .custom-file input[type="file"] { display: none; } /* hide ugly default */
        button {
            margin-top: 10px; padding: 10px 18px;
            background: #333; color:white; border:none;
            border-radius: 6px; cursor:pointer;
            font-size: 0.95em;
        }
        button:hover { background: #555; }
        ul { list-style:none; padding:0; }
        li {
            margin:8px 0; padding:10px;
            border:1px solid #eee;
            border-radius:8px;
            background:#fff8dc;
        }
        a { text-decoration:none; color:#b8860b; font-weight:500; }
        a:hover { text-decoration:underline; color:#daa520; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📡 Phone ↔ PC Transfer</h1>

        <div class="card">
            <h2>📤 Upload Files (Multiple)</h2>
            <form method="POST" enctype="multipart/form-data" action="/upload">
                <label class="custom-file">
                    <input type="file" name="files" multiple>
                    ✨ Choose Files
                </label><br>
                <button type="submit">Upload Files</button>
            </form>
        </div>

        <div class="card">
            <h2>📂 Upload Folder</h2>
            <form method="POST" enctype="multipart/form-data" action="/upload_folder">
                <label class="custom-file">
                    <input type="file" name="folder" webkitdirectory directory multiple>
                    📁 Choose Folder
                </label><br>
                <button type="submit">Upload Folder</button>
            </form>
        </div>

        <div class="card">
            <h2>📥 Download (PC → Phone)</h2>
            <ul>
                {% for file in files %}
                    <li><a href="/download/{{ file }}">{{ file }}</a></li>
                {% endfor %}
            </ul>
        </div>
    </div>
</body>
</html>
"""

# Success page
SUCCESS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Upload Success</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background:#fafafa; }
        .success {
            max-width: 500px; margin: 80px auto; background: white;
            padding: 30px; border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }
        h2 { color: #b8860b; }
        a {
            display:inline-block; margin-top:20px; text-decoration:none;
            color:white; background:#b8860b; padding:10px 20px;
            border-radius:8px;
        }
        a:hover { background:#daa520; }
    </style>
</head>
<body>
    <div class="success">
        <h2>✅ Upload Successful</h2>
        <p>{{ message }}</p>
        <a href="/">⬅ Go Back</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_PAGE, files=files)

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("files")
    saved_files = []
    for file in uploaded_files:
        if file.filename:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            saved_files.append(file.filename)
    return render_template_string(SUCCESS_PAGE, message=f"{len(saved_files)} files saved to Desktop/uploads")

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    uploaded_files = request.files.getlist("folder")
    saved_files = []
    for file in uploaded_files:
        if file.filename:
            # Keep folder structure inside Desktop/uploads
            folder_path = os.path.join(UPLOAD_FOLDER, file.filename)
            os.makedirs(os.path.dirname(folder_path), exist_ok=True)
            file.save(folder_path)
            saved_files.append(file.filename)
    return render_template_string(SUCCESS_PAGE, message=f"Folder uploaded with {len(saved_files)} files")

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
