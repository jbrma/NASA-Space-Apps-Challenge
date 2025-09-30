from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    message = ""
    if request.method == 'POST':
        f = request.files['dataset']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        message = 'File uploaded successfully!'
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
