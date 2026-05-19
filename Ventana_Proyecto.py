from tkinter import *
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

entrenado = False

pantalla_completa = True

ventana_proyecto = Tk()

ventana_proyecto.iconbitmap("Eve.ico")

ventana_proyecto.title("EvAI")

ventana_proyecto.geometry(f"{ventana_proyecto.winfo_screenwidth()}x{ventana_proyecto.winfo_screenheight()}+0+0")

ventana_proyecto.resizable(False, False)

ventana_proyecto.attributes("-fullscreen", pantalla_completa)

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

def prediccion(datos: dict):
    # Variable en la que se almacenen los valores en un map
    # Map to dataframe
    global model
    X = pd.DataFrame([datos])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    prediccion = model.predict(X_scaled)[0]

    probabilidad = model.predict_proba(X_scaled)[0][prediccion]*100

    resultado = "Avería" if prediccion == 1 else "Funcionamiento Correcto"

    return f"{resultado} ({probabilidad:.2f}% de probabilidad)"

def p_completa(event):
    global pantalla_completa
    pantalla_completa = not pantalla_completa
    ventana_proyecto.attributes("-fullscreen", pantalla_completa)

def cerrar(event):
    ventana_proyecto.destroy()

def envio():
    global entrenado
    if not entrenado:
        # resultado.config(text = "Entrenando Modelo...")
        entrenamiento()
        entrenado = True
    dict_formulario = {
        "timestamp": float(timestamp.get("1.0", END)),
        "pCut::Motor_Torque": float(pcut_motor_torque.get("1.0", END)),
        "pCut::CTRL_Position_controller::Lag_error": float(pcut_ctrl_position_controller_lag_error.get("1.0", END)),
        "pCut::CTRL_Position_controller::Actual_position": float(pcut_ctrl_position_controller_actual_position.get("1.0", END)),
        "pCut::CTRL_Position_controller::Actual_speed": float(pcut_ctrl_position_controller_actual_speed.get("1.0", END)),
        "pSvolFilm::CTRL_Position_controller::Actual_position": float(psvolfilm_ctrl_position_controller_actual_position.get("1.0", END)),
        "pSvolFilm::CTRL_Position_controller::Actual_speed": float(psvolfilm_ctrl_position_controller_actual_speed.get("1.0", END)),
        "pSvolFilm::CTRL_Position_controller::Lag_error": float(psvolfilm_ctrl_position_controller_lag_error.get("1.0", END)),
        "pSpintor::VAX_speed": float(pspintor_vax_speed.get("1.0", END)),
        "month": int(month.get("1.0", END)),
        "day": int(day.get("1.0", END)),
        "hour": int(hour.get("1.0", END)),
        "sample_Number": int(sample_number.get("1.0", END)),
        "mode": int(mode.get("1.0", END))
    }
    # resultado.config(text = "Cargando Resultado...")
    # var_resultado = prediccion(dict_formulario)
    # if var_resultado == "Avería":
        # resultado.config(text = f"{var_resultado}", fg = "red")
    # elif var_resultado == "Funcionamiento Correcto":
    resultado.config(text = f"{prediccion(dict_formulario)}")
    

ventana_proyecto.bind("<Escape>", cerrar)

ventana_proyecto.bind("<F11>", p_completa)

marco = Frame()

marco.pack(fill = "both", expand = "True")

marco.config(bg = "black", width = "600", height="600")

title = Label(marco, text = f"-- [EvAI] --", fg = "lime", bg = "black", font = ("Comic Sans MS", 16))

title.place(relx = 0.45, rely = 0.025)

ts_etiqueta = Label(marco, text = f"timestamp:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

ts_etiqueta.place(relx = 0.009, rely = 0.1)

timestamp = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

timestamp.pack()

timestamp.place(relx = 0.1, rely = 0.1)

pcmt_etiqueta = Label(marco, text = f"pCut::Motor_Torque:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

pcmt_etiqueta.place(relx = 0.305, rely = 0.1)

pcut_motor_torque = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

pcut_motor_torque.pack()

pcut_motor_torque.place(relx = 0.47, rely = 0.1)

pccpcle_etiqueta = Label(marco, text = f"pCut::Lag_error:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

pccpcle_etiqueta.place(relx = 0.675, rely = 0.1)

pcut_ctrl_position_controller_lag_error = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

pcut_ctrl_position_controller_lag_error.pack()

pcut_ctrl_position_controller_lag_error.place(relx = 0.81, rely = 0.1)

pccpcap_etiqueta = Label(marco, text = f"pCut::Ac_position:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

pccpcap_etiqueta.place(relx = 0.009, rely = 0.25)

pcut_ctrl_position_controller_actual_position = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

pcut_ctrl_position_controller_actual_position.pack()

pcut_ctrl_position_controller_actual_position.place(relx = 0.155, rely = 0.25)

pccpcas_etiqueta = Label(marco, text = f"pCut::Ac_speed:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

pccpcas_etiqueta.place(relx = 0.34, rely = 0.25)

pcut_ctrl_position_controller_actual_speed = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

pcut_ctrl_position_controller_actual_speed.pack()

pcut_ctrl_position_controller_actual_speed.place(relx = 0.47, rely = 0.25)

psvfcpcap_etiqueta = Label(marco, text = f"pSvolFilm::Ac_position:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

psvfcpcap_etiqueta.place(relx = 0.63, rely = 0.25)

psvolfilm_ctrl_position_controller_actual_position = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

psvolfilm_ctrl_position_controller_actual_position.pack()

psvolfilm_ctrl_position_controller_actual_position.place(relx = 0.81, rely = 0.25)

psvfcpcas_etiqueta = Label(marco, text = f"pSvolFilm::Ac_speed:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

psvfcpcas_etiqueta.place(relx = 0.009, rely = 0.35)

psvolfilm_ctrl_position_controller_actual_speed = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

psvolfilm_ctrl_position_controller_actual_speed.pack()

psvolfilm_ctrl_position_controller_actual_speed.place(relx = 0.17, rely = 0.35)

psvfcpcle_etiqueta = Label(marco, text = f"pSvolFilm::L_error:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

psvfcpcle_etiqueta.place(relx = 0.32, rely = 0.35)

psvolfilm_ctrl_position_controller_lag_error = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

psvolfilm_ctrl_position_controller_lag_error.pack()

psvolfilm_ctrl_position_controller_lag_error.place(relx = 0.475, rely = 0.35)

pspvs_etiqueta = Label(marco, text = f"pSpintor::VAX_speed:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

pspvs_etiqueta.place(relx = 0.635, rely = 0.35)

pspintor_vax_speed = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

pspintor_vax_speed.pack()

pspintor_vax_speed.place(relx = 0.81, rely = 0.35)

month_etiqueta = Label(marco, text = f"month:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

month_etiqueta.place(relx = 0.009, rely = 0.45)

month = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

month.pack()

month.place(relx = 0.07, rely = 0.45)

day_etiqueta = Label(marco, text = f"day:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

day_etiqueta.place(relx = 0.425, rely = 0.45)

day = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

day.pack()

day.place(relx = 0.47, rely = 0.45)

hour_etiqueta = Label(marco, text = f"hour:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

hour_etiqueta.place(relx = 0.757, rely = 0.45)

hour = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

hour.pack()

hour.place(relx = 0.81, rely = 0.45)

sn_etiqueta = Label(marco, text = f"sample_Number:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

sn_etiqueta.place(relx = 0.2, rely = 0.55)

sample_number = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

sample_number.pack()

sample_number.place(relx = 0.335, rely = 0.55)

mode_etiqueta = Label(marco, text = f"mode:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

mode_etiqueta.place(relx = 0.5, rely = 0.55)

mode = Text(marco, width = 15, height = 1, font = ("Comic Sans MS", 14))

mode.pack()

mode.place(relx = 0.557, rely = 0.55)

enviar = Button(ventana_proyecto, text = "Enviar", width = 20, cursor = "hand2", command = envio)

enviar.place(relx = 0.44, rely = 0.65)

r_etiqueta = Label(marco, text = f"Resultado:", fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

r_etiqueta.place(relx = 0.457, rely = 0.75)

resultado = Label(marco, text = "", width = 60, fg = "lime", bg = "black", font = ("Comic Sans MS", 15))

resultado.place(relx = 0.21, rely = 0.85)

ventana_proyecto.mainloop()