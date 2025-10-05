from flask import send_from_directory, Flask, render_template, request
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os
import pandas as pd
import joblib

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

rf_model, model_features = joblib.load("rf_exoplanet_model.joblib")

def predict_planets(df):
    input_df = df.copy()
    input_df = input_df.reindex(columns=model_features, fill_value=0)
    input_df = input_df.fillna(0)
    for col in model_features:
        input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)
    pred = rf_model.predict(input_df)
    if 'id' in df.columns:
        return pd.DataFrame({'id': df['id'].astype(str), 'prediction': pred})
    elif 'pl_name' in df.columns:
        return pd.DataFrame({'id': df['pl_name'].astype(str), 'prediction': pred})
    else:
        return pd.DataFrame({'id': range(len(pred)), 'prediction': pred})

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    message = ""
    metrics = ""
    result_file = None
    result_table = None
    if request.method == 'POST':
        f = request.files['dataset']
        filename = f.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        message = 'File uploaded successfully!'

        try:
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(filepath, engine='python')
            elif filename.lower().endswith('.xlsx'):
                df = pd.read_excel(filepath)
        except Exception as e:
            message = f'You must upload a CSV or Excel file'
            return render_template('index.html', message=message)

        # Ejecutar modelo de IA sobre df
        prediction_df = predict_planets(df)
        prediction_df['id'] = prediction_df['id'].astype(str)

        if 'label' in df.columns:
            y_true = df['label'].astype(int)
            y_pred = prediction_df['prediction']
            acc = accuracy_score(y_true, y_pred)
            cm = confusion_matrix(y_true, y_pred)
            cr = classification_report(y_true, y_pred)

            metrics = f"Accuracy: {acc:.4f}\nConfusion Matrix:\n{cm}\nReport:\n{cr}"

        # Guardar datos de salida para descargar
        output_filename = 'result_' + filename.replace('.xlsx', '.csv')
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        prediction_df.to_csv(output_filepath, index=False)

        result_file = output_filename
        result_table = prediction_df.to_html(classes='table table-striped')

    return render_template('index.html', message=message, result_file=result_file, result_table=result_table, metrics=metrics)


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

