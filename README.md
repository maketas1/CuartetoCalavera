## CONTEXTO DEL PROBLEMA DESCRITO

- Realizando un análisis más exhaustivo, teníamos la idea que crear un algoritmo de clasificación relacionado con la enfermedad de la tuberculosis. Sin embargo, NO hemos encontrado un database con la cantidad de datos suficientes para poder trabajar con el tema.
- Esto nos ha hecho pensar en realizar un algoritmo que tenga beneficios para las empresas que trabajan con maquinarias de alto rendimiento y que tienen un alto coste. 

## INTRODUCCIÓN PROYECTO

Bienvenidos al repositorio oficial de una aplicación que permitirá que empresas que elaboren un sin fin de productos  se vean beneficiadas con este algoritmo que permite predecir el funcionamiento y posible tiempo de averia de una maquinaria determinada, siempre y cuando esta funcione a través de diversos sensores. Este proyecto forma parte del aprendizaje del curso Python + Inteligencia Artificial, combinando conceptos de programación estructurada, Numpy, Pandas, bases de datos, APIs y arquitectura web moderna.
 
## OBJETIVOS DEL PROYECTO

Los objetivos principales del proyecto:

1.- Realizar un algoritmo que permita estimar a través de funciones matemáticas (Numpy), el correcto funcionamiento de maquinarias que trabajen con sensores. 
2.- Utilizar gráficos que muesten y estimen correctamente los valores de/los dataset utilizados para entrenar el algoritmo.

## ANALISIS DE LA BASE DE DATOS A UTILIZAR

- Se utilizará una base de datos obtenida desde kaggle:
https://www.kaggle.com/datasets/iuryck/datasetsone-year-compiledcsv

- Esta base de datos posee más de 1000000 de filas y 14 columnas.

- Una de los analisis más importantes son las columnas, estas es la explicación de cada una:

1.-  **timestamp**	(Marca de tiempo) -> Representa el instante temporal preciso, con resolución de milisegundos, en el que el PLC (Controlador Lógico Programable) o el sistema de adquisición de datos capturó el estado de todos los sensores. Es la variable de referencia para el análisis de series temporales. 
@ Clasificación de variable: datetime, temporal.
@ Valores mínimo y máximo: 0 / 8.2

2.-  **pCut::Motor_Torque** (Par (torque) del motor en la estación o proceso “pCut”) -> Esta columna es el complemento perfecto para el Lag_error que vimos antes. Si el Lag_error nos dice cuánto se está retrasando la máquina, el Motor_Torque nos dice cuánta fuerza está teniendo que hacer para intentar cumplir con su tarea.
Registra el par de torsión (fuerza de giro) generado por el motor en la estación de corte (pCut). En un sistema de lazo cerrado, el controlador aumenta el torque cuando detecta una resistencia física para mantener la velocidad o posición programada. Se mide habitualmente en Newton-metro (Nm) o como un porcentaje del torque nominal del motor.
@ Clasificación de variable: numérica continua, float, Carga/esfuerzo.
@ Valores mínimo y máximo: -6.56 / 3.86 

3.-  **pCut::CTRL_Position_controller::Lag_error**	(Error de seguimiento (lag error) en el controlador de posición de “pCut”). -> Representa el error de seguimiento del controlador de posición en la estación de corte (pCut). Es la diferencia instantánea entre la posición teórica dictada por el perfil de movimiento (consigna) y la posición real medida por el encoder del motor. En un sistema ideal, este valor debería ser cercano a cero.
@ Clasificación de variable: numérica continua, float, Precisión.
@ Valores mínimo y máximo: -1.89 / 2.02


4.-  **pCut::CTRL_Position_controller::Actual_position** -> Con esta columna cerramos el triángulo fundamental del control de movimiento: Lo que pides (Setpoint), lo que haces (Actual Position) y la diferencia (Lag Error).
Es la lectura en tiempo real del sensor de posición (normalmente un encoder rotativo o lineal) en la estación de corte. Indica el lugar físico exacto donde se encuentra la herramienta o el material en un instante "t". A diferencia de la "posición de consigna" (que es lo que la máquina cree que debería hacer), esta es la verdad física del proceso.
@ Clasificación de variable: numérica continua, float.
@ Valores mínimo y máximo: -2039056494 / 1.91b


5.-  **pCut::CTRL_Position_controller::Actual_speed** -> (Esta columna es el "ritmo cardíaco" de la estación de corte. Mientras que la posición nos dice dónde está, la velocidad nos dice cómo de estable es el movimiento.)
Descripción ampliada:
Indica la velocidad instantánea real a la que se desplaza el eje en la estación pCut. Se obtiene generalmente calculando la tasa de cambio de la posición en el tiempo (derivada de la posición). En un entorno industrial, se suele expresar en milímetros por segundo (mm/s) o revoluciones por minuto (RPM).
@ Clasificación de variable: numérica continua, float.
@ Valores mínimo y máximo: -9,48k / 17,9k

6.-  **pSvolFilm::CTRL_Position_controller::Actual_position**	(Posición real actual en el sistema o estación “pSvolFilm”) -> Pasamos de la estación de corte (pCut) a pSvolFilm. Por el nombre, esto suena a un sistema de desbobinado o alimentación de film (lámina de plástico o papel). Aquí la dinámica cambia: ya no es un golpe seco como el corte, sino un movimiento continuo y fluido.
Registra la ubicación física exacta del eje encargado del manejo del film en la estación pSvolFilm. Mientras que en el corte la posición suele ser un recorrido de ida y vuelta, en un sistema de film, esta variable suele indicar la cantidad de material que ha pasado o la posición de un rodillo compensador (dancer arm) que mantiene la tensión.
@ Clasificación de variable: numérica continua, float.
@ Valores mínimo y máximo: 194k / 1.45b

7.-  **pSvolFilm::CTRL_Position_controller::Actual_speed**	Velocidad real actual en el sistema “pSvolFilm” -> Al tratarse de la estación pSvolFilm, esta velocidad es el factor determinante para que el material no se rompa ni se amontone.
Representa la velocidad lineal o rotacional real del eje de alimentación de film. A diferencia de un eje de corte que acelera y frena bruscamente, la velocidad en pSvolFilm suele buscar un estado estacionario (constante) para garantizar que el material fluya sin tirones. Es la métrica que nos dice qué tan rápido se está desenrollando o transportando la lámina.
@ Clasificación de variable: numérica continua, float.
@ Valores mínimo y máximo: -20.1 - 18k 

8.-  **pSvolFilm::CTRL_Position_controller::Lag_error** -> En un controlador de posición (position controller), el Lag_error es la diferencia matemática entre la posición que el algoritmo le ordena a la máquina tener y la posición real que los sensores reportan en un momento exacto "t" (tiempo continuo).
Ahora bien, es importante conocer: 

Si estás buscando predecir el "buen o mal funcionamiento", el comportamiento de esta columna te da pistas directas sobre la salud mecánica:

Desgaste Mecánico: Si el error de lag aumenta gradualmente con los días, es muy probable que haya fricción excesiva, falta de lubricación o desgaste en las guías.

Holguras (Backlash): Si el error salta bruscamente cuando la máquina cambia de dirección, tienes un problema de juego mecánico.

Sobrecarga: Un pico repentino en el Lag_error suele indicar que la maquinaria encontró una resistencia física que no pudo superar a la velocidad prevista (un atasco o una pieza mal colocada).

Sintonización del Control (PID): Si el error oscila mucho, el controlador no está bien ajustado para la carga actual.

Con respecto a "t": Es crucial tener el tiempo en este punto, ya que:

En tu base de datos, el error de lag no se analiza de forma aislada, sino en función de cómo evoluciona:
"t_0" (Estado ideal): La máquina recibe la orden de moverse y el motor responde casi al instante. El error es cercano a cero.
"t_{n}" (El retraso): Debido a la inercia, el rozamiento o el peso de la pieza, la parte mecánica siempre va un "pelín" por detrás de la orden eléctrica. Ese "retraso" es el que se mide en cada instante.
@ Clasificación de variable: numérica continua, float.
@ Valores mínimo y máximo: -0.91 / 3.57

9.-  **pSpintor::VAX_speed** -> El nombre pSpintor suena a una estación de giro o torsión (posiblemente un cabezal giratorio o un eje principal de tracción). Y el prefijo VAX suele referirse a un Eje Virtual (Virtual Axis) o a un valor de referencia de alta precisión.
Indica la velocidad del eje virtual (o eje maestro de referencia) en la estación de giro pSpintor. A diferencia de las velocidades "Actual", la VAX_speed suele representar la velocidad teórica ideal que el sistema intenta alcanzar para que el resto de los ejes (como el corte y el film) se sincronicen con ella. Es el "metrónomo" que marca el ritmo de toda la maquinaria.
@ Clasificación de variable: numérica continua, float.
@ Valores mínimo y máximo: 0 / 3,6k

10.- **month** -> Valores mínimo y máximo: 1 al 12

11.- **day** -> Valores mínimo y máximo: 1 al 31

12.- **hour** -> Valores mínimo y máximo: 00 a 23

### ESTAS 3 COLUMNAS, 10, 11 Y 12, REPRESENTAN LA DESCOMPOSICIÓN DE LA MARCA DEL TIEMPO  ORIGINAL EN UNIDADES DISCRETAS.
@ Clasificación de variable: numericas discretas int, temporal. 


13.- **sample_Number** -> Es un contador secuencial y único asignado a cada fila de datos. A diferencia del timestamp, que mide el tiempo real, el sample_Number mide el orden de captura. En sistemas de alta velocidad, es el identificador que asegura que no se ha perdido ningún paquete de información entre el sensor y la base de datos.
@ Clasificación de variable: numerica discreta, int64. 
@ Valores mínimo y máximo: 0 / 518

14.- **mode** -> En sistemas industriales, cada número suele corresponder a una fase específica del ciclo de trabajo o a una configuración de producto distinta.
Variable categórica que define el estado operativo de la máquina. Estos 6 modos actúan como el "contexto" de todos los demás sensores. Lo que en el Mode2 puede ser una velocidad normal, en el Mode5 podría ser una anomalía crítica.

(Hipótesis común en este tipo de máquinas):

Modos de Preparación (ej. 1-2): Homing (búsqueda de cero), limpieza o enhebrado del film (pSvolFilm). Aquí el torque es bajo y las velocidades son lentas.

Modos de Producción (ej. 3-4): Diferentes velocidades de crucero o distintos tamaños de corte en pCut. Aquí es donde el Lag_error es más sensible.

Modos de Mantenimiento/Fallo (ej. 5-6): Estados de pausa, error o recuperación tras una parada de emergencia.
@ Clasificación de variable: Categórica ordinal, int (contexto).
@ Valores mínimo y máximo: mode1 / mode7

## ES FUNDAMENTAL REVISAR ESTOS DATOS, NO HE CONSEGUIDO ABRIR LA BASE DE DATOS PARA REVISAR SI ESTA INFORMACIÓN PUEDE ESTAR RELACIONADA CON NUESTRA MAQUINARIA (KRY).




"""esto es importante... 

¿Qué tenemos que saber de cada columna?
Definición._.
Unidad de medida ._.
Tipo de variable (si es categórica necesitamos saber los valores únicos y su distribución)
Gráficos y preprocesamiento aplicado"""
