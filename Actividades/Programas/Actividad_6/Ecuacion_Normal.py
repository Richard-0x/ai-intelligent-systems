import numpy as np

# 1. Datos de entrenamiento simulados: área en m^2 (X) y precio en miles de dólares (y)
# Añadimos 8 ejemplos (m=8) como indicaban tus comentarios originales
X = np.array([50, 60, 70, 80, 90, 100, 110, 120])
y = np.array([160, 185, 215, 250, 275, 310, 340, 365])

m = X.size # Número de ejemplos de entrenamiento (m = 8)

# 2. Construcción de la Matriz de Diseño (X_b): agregamos columna de 1s para theta_0
X_b = np.c_[np.ones((m, 1)), X]

# 3. Aplicación de la Ecuación Normal: theta = (X^T @ X)^(-1) @ X^T @ y
theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y

# 4. Resultados de los parámetros ajustados
# Corregimos los índices: theta[0] para el intercepto y theta[1] para la pendiente
intercepto_theta0 = round(theta[0], 2)
pendiente_theta1 = round(theta[1], 2)

print(f"Modelo Ajustado: h(x) = {intercepto_theta0} + {pendiente_theta1} * x")
print(f"Intercepto (theta_0): {intercepto_theta0}")
print(f"Pendiente (theta_1): {pendiente_theta1}")

# 5. Predicción para una vivienda de 95 m^2
x_nuevo = 95
# Usamos las variables escalares extraídas en el paso 4
precio_estimado = intercepto_theta0 + pendiente_theta1 * x_nuevo

print(f"\nPrecio estimado para 95 m^2: ${round(precio_estimado, 2)} miles de dólares")