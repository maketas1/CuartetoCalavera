from tkinter import *
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib

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

X = df1_copia.drop("averia", axis=1)
X = X.drop("s1", axis=1)
X = X.drop("s2", axis=1)

y = df1_copia["averia"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mode_categories = [[
    'mode0', 'mode1', 'mode2', 'mode3',
    'mode4', 'mode5', 'mode6', 'mode7', 'mode8'
]]

categoricas = ["mode"]

numericas = ['timestamp', 'pCut::Motor_Torque', 'pCut::CTRL_Position_controller::Lag_error', 'pCut::CTRL_Position_controller::Actual_position', 'pCut::CTRL_Position_controller::Actual_speed', 'pSvolFilm::CTRL_Position_controller::Actual_position', 'pSvolFilm::CTRL_Position_controller::Actual_speed', 'pSvolFilm::CTRL_Position_controller::Lag_error', 'pSpintor::VAX_speed', 'month', 'day', 'hour', 'sample_Number']

preprocessor = ColumnTransformer(
    transformers=[
        ('mode_encoder', OrdinalEncoder(categories=mode_categories), categoricas),
        ('num_scaler',StandardScaler(), numericas)
    ]
)

modelo = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
joblib.dump(modelo, "modelo.joblib")