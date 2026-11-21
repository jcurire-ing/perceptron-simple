# Laboratorio UCV - Perceptrón Simple

Implementación desde cero de un **Perceptrón Simple** en Python 3.12 para automatizar la aprobación preliminar de créditos bancarios según ingreso mensual e historial crediticio.

## Ejecución y Pruebas

    python main.py
    pytest

---

## Preguntas de Análisis

### 1. ¿Qué representan los pesos?
Los **pesos** ($w_1, w_2$) representan la **importancia o influencia** que tiene cada variable de entrada en la decisión final de la neurona. En el caso del banco, determinan cuánto influye el ingreso mensual frente al historial crediticio para aprobar o rechazar un crédito. Un peso positivo alto impulsa la aprobación; un peso negativo la frena.

### 2. ¿Qué función cumple el bias?
El **bias** (sesgo) funciona como un **umbral de decisión ajustable** que desplaza la frontera de decisión sin depender de los datos de entrada. En el contexto bancario, representa el nivel base de exigencia o rigurosidad del banco: un bias negativo exige que el cliente tenga ingresos e historial suficientemente altos para superar el umbral de activación (`>= 0`) y obtener la aprobación (`1`).

### 3. ¿Cómo aprende el perceptrón?
Aprende mediante **aprendizaje supervisado iterativo** (regla de aprendizaje del perceptrón) a lo largo de múltiples épocas (*epochs*):
1. Toma un registro de entrenamiento con sus entradas y salida esperada.
2. Calcula una predicción usando los pesos y bias actuales.
3. Calcula el error: $\text{error} = \text{esperado} - \text{predicción}$.
4. Si existe error ($\text{error} \neq 0$), actualiza cada peso y el bias proporcionalmente a la tasa de aprendizaje ($\eta$):
   $$w_i = w_i + \eta \cdot \text{error} \cdot x_i$$
   $$b = b + \eta \cdot \text{error}$$
5. Repite el ciclo hasta que las predicciones convergen sin errores.

### 4. ¿Por qué el perceptrón no puede resolver XOR?
Porque el perceptrón simple es un **clasificador lineal**: solo puede trazar **una única línea recta** (o hiperplano) para dividir las clases en el espacio. La compuerta lógica **XOR** devuelve `1` cuando las entradas son diferentes (`[0,1]` y `[1,0]`) y `0` cuando son iguales (`[0,0]` y `[1,1]`). Al ubicar estos cuatro puntos en un plano cartesiano, es geométricamente imposible separar los `1` de los `0` utilizando una sola línea recta (no es linealmente separable).

### 5. ¿Qué ventajas tiene un perceptrón multicapa?
Un **Perceptrón Multicapa (MLP)** agrega una o más **capas ocultas** entre la entrada y la salida junto con funciones de activación no lineales. Sus principales ventajas son:
* **Resuelve problemas no linealmente separables** (como XOR), ya que combina múltiples fronteras lineales para formar regiones complejas.
* **Extrae representaciones internas automáticas**, aprendiendo relaciones e interacciones ocultas entre variables.
* **Escalabilidad a tareas reales complejas**, como visión por computadora, procesamiento de lenguaje natural y modelos avanzados de riesgo crediticio.

---

## Reto MIT: El Problema XOR y su Solución Multicapa

### Investigación del problema XOR
En 1969, **Marvin Minsky y Seymour Papert** (investigadores del MIT) demostraron en su obra *Perceptrons* que un perceptrón de una sola capa no puede aprender la función lógica **XOR** (*OR exclusivo*). Este hallazgo evidenció los límites de los modelos puramente lineales.

| Entrada $X_1$ | Entrada $X_2$ | Salida XOR Esperada |
| :---: | :---: | :---: |
| 0 | 0 | **0** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

**Demostración matemática de por qué falla el perceptrón simple:**
Un perceptrón simple evalúa $w_1 x_1 + w_2 x_2 + b \ge 0$. Para resolver XOR debe cumplir cuatro desigualdades simultáneas:
1. Para `[0,0]` $\rightarrow b < 0$
2. Para `[0,1]` $\rightarrow w_2 + b \ge 0$
3. Para `[1,0]` $\rightarrow w_1 + b \ge 0$
4. Para `[1,1]` $\rightarrow w_1 + w_2 + b < 0$

Al sumar las desigualdades (2) y (3) se obtiene $w_1 + w_2 + 2b \ge 0$. Como $b < 0$ según (1), esto implica que $w_1 + w_2 + b > 0$, lo cual contradice directamente la desigualdad (4). Por tanto, no existen pesos ni bias que resuelvan XOR en una sola capa.

### Propuesta de solución con Perceptrón Multicapa (MLP)
Para resolver XOR se diseña una red neuronal con **una capa oculta de 2 neuronas** y **1 neurona de salida**, descomponiendo el problema en dos rectas:

1. **Neurona oculta 1 (Compuerta OR):** Se activa si al menos una entrada es `1` ($X_1 \lor X_2$). Traza una primera línea que separa el punto `[0,0]` del resto.
2. **Neurona oculta 2 (Compuerta NAND):** Se activa siempre que ambas entradas no sean `1` a la vez ($\neg(X_1 \land X_2)$). Traza una segunda línea que separa el punto `[1,1]` del resto.
3. **Neurona de salida (Compuerta AND):** Combina ambas salidas ocultas ($h_1 \land h_2$). Devuelve `1` únicamente cuando se cumplen ambas condiciones simultáneamente, aislando exactamente los puntos `[0,1]` y `[1,0]`.
