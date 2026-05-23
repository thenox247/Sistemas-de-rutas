import heapq

grafo = {
    'Terminal': {
        'Centro': 4,
        'Hospital': 6,
        'Aeropuerto': 8
    },

    'Centro': {
        'Terminal': 4,
        'Universidad': 5,
        'Estadio': 3,
        'Mercado': 2,
        'Biblioteca': 4
    },

    'Hospital': {
        'Terminal': 6,
        'Estadio': 2,
        'Barrio Norte': 4
    },

    'Estadio': {
        'Centro': 3,
        'Hospital': 2,
        'Universidad': 4,
        'Parque Central': 2
    },

    'Universidad': {
        'Centro': 5,
        'Estadio': 4,
        'Biblioteca': 2,
        'Colegio': 3
    },

    'Mercado': {
        'Centro': 2,
        'Parque Central': 3,
        'Barrio Sur': 5
    },

    'Biblioteca': {
        'Centro': 4,
        'Universidad': 2,
        'Colegio': 2
    },

    'Colegio': {
        'Universidad': 3,
        'Biblioteca': 2,
        'Barrio Norte': 4
    },

    'Parque Central': {
        'Estadio': 2,
        'Mercado': 3,
        'Barrio Sur': 2
    },

    'Barrio Norte': {
        'Hospital': 4,
        'Colegio': 4,
        'Aeropuerto': 5
    },

    'Barrio Sur': {
        'Mercado': 5,
        'Parque Central': 2,
        'Terminal': 7
    },

    'Aeropuerto': {
        'Terminal': 8,
        'Barrio Norte': 5
    }
}


# Heurística (estimación al destino)

heuristica = {
    'Terminal': 10,
    'Centro': 5,
    'Hospital': 7,
    'Estadio': 4,
    'Universidad': 0,
    'Mercado': 6,
    'Biblioteca': 2,
    'Colegio': 3,
    'Parque Central': 5,
    'Barrio Norte': 6,
    'Barrio Sur': 7,
    'Aeropuerto': 9
}


# Tiempo entre estaciones (minutos)

tiempos = {
    ('Terminal', 'Centro'): 8,
    ('Centro', 'Terminal'): 8,

    ('Terminal', 'Hospital'): 12,
    ('Hospital', 'Terminal'): 12,

    ('Terminal', 'Aeropuerto'): 15,
    ('Aeropuerto', 'Terminal'): 15,

    ('Centro', 'Universidad'): 10,
    ('Universidad', 'Centro'): 10,

    ('Centro', 'Estadio'): 6,
    ('Estadio', 'Centro'): 6,

    ('Centro', 'Mercado'): 4,
    ('Mercado', 'Centro'): 4,

    ('Centro', 'Biblioteca'): 7,
    ('Biblioteca', 'Centro'): 7,

    ('Hospital', 'Estadio'): 4,
    ('Estadio', 'Hospital'): 4,

    ('Hospital', 'Barrio Norte'): 8,
    ('Barrio Norte', 'Hospital'): 8,

    ('Estadio', 'Universidad'): 7,
    ('Universidad', 'Estadio'): 7,

    ('Estadio', 'Parque Central'): 5,
    ('Parque Central', 'Estadio'): 5,

    ('Universidad', 'Biblioteca'): 3,
    ('Biblioteca', 'Universidad'): 3,

    ('Universidad', 'Colegio'): 5,
    ('Colegio', 'Universidad'): 5,

    ('Mercado', 'Parque Central'): 6,
    ('Parque Central', 'Mercado'): 6,

    ('Mercado', 'Barrio Sur'): 12,
    ('Barrio Sur', 'Mercado'): 12,

    ('Biblioteca', 'Colegio'): 4,
    ('Colegio', 'Biblioteca'): 4,

    ('Colegio', 'Barrio Norte'): 8,
    ('Barrio Norte', 'Colegio'): 8,

    ('Parque Central', 'Barrio Sur'): 5,
    ('Barrio Sur', 'Parque Central'): 5,

    ('Barrio Norte', 'Aeropuerto'): 10,
    ('Aeropuerto', 'Barrio Norte'): 10
}


# Reglas aplicadas

def aplicar_reglas(origen, destino, costo):

    # Regla 1: rutas congestionadas
    rutas_congestionadas = [
        ('Centro', 'Estadio'),
        ('Mercado', 'Centro'),
        ('Terminal', 'Centro')
    ]

    if (origen, destino) in rutas_congestionadas:
        costo += 3

    # Regla 2: prioridad hospitalaria
    if destino == 'Hospital':
        costo -= 1

    # Regla 3: tráfico al aeropuerto
    if destino == 'Aeropuerto':
        costo += 2

    return costo


# Algoritmo A*

def a_estrella(inicio, objetivo):

    cola = []
    heapq.heappush(cola, (0, inicio))

    costos = {inicio: 0}
    camino = {}

    while cola:

        _, actual = heapq.heappop(cola)

        if actual == objetivo:

            ruta = []

            while actual in camino:
                ruta.append(actual)
                actual = camino[actual]

            ruta.append(inicio)
            ruta.reverse()

            return ruta, costos[objetivo]

        for vecino, costo in grafo[actual].items():

            costo_ajustado = aplicar_reglas(
                actual,
                vecino,
                costo
            )

            nuevo_costo = (
                costos[actual] +
                costo_ajustado
            )

            if vecino not in costos or nuevo_costo < costos[vecino]:

                costos[vecino] = nuevo_costo

                prioridad = (
                    nuevo_costo +
                    heuristica[vecino]
                )

                heapq.heappush(
                    cola,
                    (prioridad, vecino)
                )

                camino[vecino] = actual

    return None, None


# Calculo del tiempo de la ruta

def calcular_tiempo(ruta):

    tiempo_total = 0

    for i in range(len(ruta) - 1):

        origen = ruta[i]
        destino = ruta[i + 1]

        tiempo_total += tiempos.get(
            (origen, destino),
            0
        )

    return tiempo_total


# interfaz

print("\n================================")
print(" SISTEMA INTELIGENTE DE RUTAS ")
print("================================")

print("\nEstaciones disponibles:")

for estacion in grafo:
    print("-", estacion)

inicio = input(
    "\nIngrese punto de inicio: "
)

destino = input(
    "Ingrese destino: "
)

# Validación
if inicio not in grafo or destino not in grafo:

    print("\nError: Estación no encontrada.")

else:

    ruta, costo = a_estrella(
        inicio,
        destino
    )

    if ruta:

        tiempo_total = calcular_tiempo(ruta)

        print("\n===== RESULTADO =====")
        print("Mejor ruta encontrada:")

        print(" -> ".join(ruta))

        print(
            "\nCosto total:",
            costo
        )

        print(
            "Tiempo estimado:",
            tiempo_total,
            "minutos"
        )

    else:
        print(
            "\nNo se encontró una ruta."
        )