from flask import send_from_directory, Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def predict_planets(df):
    # Simulación IA: predice 0 o 1 random para cada fila
    import numpy as np
    df['prediction'] = np.random.choice([0, 1], size=len(df))

    # PONER LAS COLUMNAS QUE SEAN
    return df[['id', 'prediction']]

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    message = ""
    result_file = None
    result_table = None
    if request.method == 'POST':
        f = request.files['dataset']
        filename = f.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        message = 'File uploaded successfully!'

        df = pd.read_excel(filepath)

        # Ejecutar modelo de IA sobre df
        prediction_df = predict_planets(df)
        prediction_df['id'] = prediction_df['id'].astype(str)


        # Guardar datos de salida para descargar
        output_filename = 'result_' + filename.replace('.xlsx', '.csv')
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        prediction_df.to_csv(output_filepath, index=False)

        result_file = output_filename
        result_table = prediction_df.to_html(classes='table table-striped')

    return render_template('index.html', message=message, result_file=result_file, result_table=result_table)


@app.route("/uploads")
def list_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_links = [f"<a href='/uploads/{file}'>{file}</a>" for file in files]
    return "<h2>Uploaded Files</h2>" + "<br>".join(file_links)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

