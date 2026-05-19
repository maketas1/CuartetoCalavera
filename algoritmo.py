import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

model = RandomForestClassifier()

def entrenamiento():
    global model
    df1 = pd.read_csv('One_year_compiled.csv')

    df1_copia = df1.copy()
    df1_copia = np.round(df1_copia, 1)

    df1_copia["averia"] = (
        (df1_copia["pCut::CTRL_Position_controller::Lag_error"] < 0) |
        (df1_copia["pSvolFilm::CTRL_Position_controller::Lag_error"] < 0) |
        (df1_copia["pCut::CTRL_Position_controller::Lag_error"] > 1.7) |
        (df1_copia["pSvolFilm::CTRL_Position_controller::Lag_error"] > 3)
    ).astype(int)

    df1_copia["averia"].value_counts()

    df1_copia["s1"] = (
        (df1_copia["pCut::CTRL_Position_controller::Lag_error"] < 0) |
        (df1_copia["pCut::CTRL_Position_controller::Lag_error"] > 1.7)
    ).astype(int)

    df1_copia["s1"].value_counts()

    df1_copia["s2"] = (
        (df1_copia["pSvolFilm::CTRL_Position_controller::Lag_error"] < 0) |
        (df1_copia["pSvolFilm::CTRL_Position_controller::Lag_error"] > 3)
    ).astype(int)

    df1_copia["s2"].value_counts()

    df1_copia1 = df1_copia.drop("mode", axis=1)
    X = df1_copia1.drop("averia", axis=1)
    X = X.drop("s1", axis=1)
    X = X.drop("s2", axis=1)

    X1 = np.array(df1_copia[['mode']])

    y = df1_copia["averia"]

    encoder = OrdinalEncoder(
        categories=[['mode0', 'mode1', 'mode2', 'mode3', 'mode4', 'mode5', 'mode6', 'mode7', 'mode8']]
    )
    X['mode'] = encoder.fit_transform(X1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Precisión del Random Forest: {accuracy * 100:.2f}%')

def prediccion(datos: dict):
    # Variable en la que se almacenen los valores en un map
    # Map to dataframe
    global model
    X = pd.DataFrame(datos)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    prediccion = model.predict(X_scaled)[0]

    probabilidad = model.predict_proba(X_scaled)[0][prediccion]*100

    resultado = "Avería" if prediccion == 1 else "Funcionamiento Correcto"

    return f"\nPredicción: {resultado} ({probabilidad:.2f}% de confianza)"