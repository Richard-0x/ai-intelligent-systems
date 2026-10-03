"""
Algoritmo Genético Simple en Python
Asignatura: Sistemas Inteligentes - Unidad 4: Modelos Evolutivos

Objetivo: Maximizar f(x) = x^2 para x en el intervalo entero [0, 31]
Codificación: Cadenas binarias de 5 bits (2^5 = 32 combinaciones)
"""

import random

def funcion_aptitud(x):
    """Calcula la aptitud del individuo: f(x) = x^2."""
    return x**2

def binario_a_decimal(cadena_binaria):
    """Convierte una cadena binaria de 5 bits a su valor entero."""
    return int(cadena_binaria, 2)

def crear_poblacion_inicial(tamano_poblacion=4, bits=5):
    """Genera una población inicial de cadenas binarias aleatorias."""
    return [
        format(random.randint(0, (2**bits) - 1), f"0{bits}b")
        for _ in range(tamano_poblacion)
    ]

def seleccion_ruleta(poblacion, aptitudes):
    """Selecciona un individuo de forma proporcional a su aptitud (Selección por Ruleta)."""
    suma_aptitud = sum(aptitudes)
    if suma_aptitud == 0:
        return random.choice(poblacion)

    probabilidades = [f / suma_aptitud for f in aptitudes]
    r = random.random()
    acumulado = 0.0

    for individuo, prob in zip(poblacion, probabilidades):
        acumulado += prob
        if r <= acumulado:
            return individuo
    return poblacion[-1]

def cruza_un_punto(padre1, padre2, probabilidad_cruza=0.8):
    """Combina dos padres en un punto de corte aleatorio para generar dos hijos."""
    if random.random() < probabilidad_cruza:
        punto = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1, padre2

def mutacion(individuo, probabilidad_mutacion=0.05):
    """Invierte bits aleatoriamente con una probabilidad p_m (Bit-flip mutation)."""
    individuo_mutado = list(individuo)
    for i in range(len(individuo_mutado)):
        if random.random() < probabilidad_mutacion:
            individuo_mutado[i] = "1" if individuo_mutado[i] == "0" else "0"
    return "".join(individuo_mutado)

def ejecutar_algoritmo_genetico(
    tamano_poblacion=4,
    generaciones=10,
    probabilidad_cruza=0.8,
    probabilidad_mutacion=0.05,
    semilla=42,
):
    """Ejecuta el ciclo evolutivo completo."""
    if semilla is not None:
        random.seed(semilla)

    poblacion = crear_poblacion_inicial(tamano_poblacion)

    print("==================================================")
    print("      EJECUCIÓN DEL ALGORITMO GENÉTICO            ")
    print("==================================================")
    print(f"Población: {tamano_poblacion} | Generaciones Máx: {generaciones}")
    print(f"Prob. Cruza: {probabilidad_cruza} | Prob. Mutación: {probabilidad_mutacion}\n")

    for gen in range(1, generaciones + 1):
        valores_x = [binario_a_decimal(ind) for ind in poblacion]
        aptitudes = [funcion_aptitud(x) for x in valores_x]

        aptitud_max = max(aptitudes)
        aptitud_prom = sum(aptitudes) / tamano_poblacion
        mejor_ind = poblacion[aptitudes.index(aptitud_max)]
        mejor_x = binario_a_decimal(mejor_ind)

        print(f"--- Generación {gen} ---")
        for i, ind in enumerate(poblacion):
            print(
                f"  Individuo {i+1}: Binario={ind} | x={valores_x[i]:2d} | Aptitud f(x)={aptitudes[i]:4d}"
            )

        print(f"  >> Mejor Solución Actual: x = {mejor_x} (Aptitud = {aptitud_max})")
        print(f"  >> Aptitud Promedio: {aptitud_prom:.2f}\n")

        if mejor_x == 31:
            print("¡Óptimo global alcanzado (x = 31, f(31) = 961)!")
            break

        nueva_poblacion = [mejor_ind]

        while len(nueva_poblacion) < tamano_poblacion:
            padre1 = seleccion_ruleta(poblacion, aptitudes)
            padre2 = seleccion_ruleta(poblacion, aptitudes)

            hijo1, hijo2 = cruza_un_punto(padre1, padre2, probabilidad_cruza)

            hijo1 = mutacion(hijo1, probabilidad_mutacion)
            hijo2 = mutacion(hijo2, probabilidad_mutacion)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < tamano_poblacion:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

if __name__ == "__main__":
    ejecutar_algoritmo_genetico()