import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_excel('data_cleaned_FP_CP.xlsx')

features = [
    'mag', 'period_days', 'duration_hours', 'depth_ppm', 'planet_radius_re',
    'insolation_se', 'eq_temp_k', 'stellar_teff_k', 'stellar_logg', 'stellar_radius_rsun',
    'depth_frac', 'rp_rs_est', 'duty_cycle', 'log_period', 'log_duration', 'log_depthppm',
]
df = df.dropna(subset=features + ['label'])  # label es 0 (False Positive) o 1 (Confirmed)
X = df[features]
y = df['label'].astype(int)

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)

joblib.dump((clf, features), "rf_exoplanet_model.joblib")
print("Modelo entrenado y guardado.")

print("Accuracy en entrenamiento:", accuracy_score(ytest, ypred))
print("Matriz de confusión:")
print(confusion_matrix(ytest, ypred))
print("Reporte completo:")
print(classification_report(ytest, ypred))
print(f"Total de datos: {len(df)}")
print(f"Entrenamiento: {len(Xtrain)}")
print(f"Pruebas: {len(Xtest)}")
