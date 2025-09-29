from flask import Flask, render_template, reques
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['dataset']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        return '¡Archivo subido exitosamente!'
    return '''
    <h1>Sube tu dataset</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="dataset">
      <input type="submit">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
