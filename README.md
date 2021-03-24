# sokoban-solver

## TODO: CHANGE TO TP2

## Requerimientos
Para correr el solver de Sokoban, es necesario tener instalado `Python 3`.

### Versiones
Para el desarrollo, se utilizó la versión `Python 3.8.5`

## Ejecución
Para ejecutar el programa, se debe ejecutar desde la raíz del proyecto

`python3 main.py`

Si se desea, puede redirigirse la salida a un archivo usando `>`.

## Configuraciones
Todas las configuraciones de ejecución se establecen en el archivo `config.json`. A continuación, se explica a qué hace referencia cada configuración:
- **level** indica el archivo con el mapa a resolver. Su ruta se indica desde la raíz del proyecto.
- **algorithm** indica el algoritmo a utilizar, siendo válidos BFS, DFS, IDDFS, GGS, ASS e IDASS.
- **max_depth** indica la máxima profundidad a alcanzar para evitar ejecuciones extremadamente largas.
- **max_expanded_nodes** indica la máxima cantidad de nodos a expandir para evitar ejecuciones extremadamente largas.
- **iddfs_step** indica el step deseado entre iteración e iteración de IDDFS en caso de elegir dicho algoritmo. La máxima profundidad comenzará en iddfs_step y luego irá aumentando de a iddfs_step.
- **print** indica si se desea imprimir el camino solución o no (en caso de encontrar uno).
- **print_time** indica el tiempo entre la impresión de cada paso del camino solución (en caso de habilitar la impresión).
- **heuristic** indica el número de heurística a utilizar en caso de utilizar un algoritmo informado. Los valores posibles son
    - 1 --> Distancia manhattan desde el sokoban a la caja más cercana (que no esté en un objetivo).
    - 2 --> Distancia manhattan desde cualquier caja (que no esté en un objetivo) a su objetivo más cercano.
    - 3 --> Suma de distancias manhattan desde cada caja hasta su objetivo más cercano (con O(N^2)).
    - 4 --> Suma de distancias manhattan desde cada caja hasta su objetivo más cercano (con O(N)).
    - 5 --> Suma de las heurísticas 1 y 4.

### Ejemplo 1
{
	"level": "levels/level_medium.txt",
	"algorithm": "BFS",
	"max_depth": 1000000,
	"max_expanded_nodes": 1000000,
	"iddfs_step": 1,
	"print": true,
	"print_time": 0.2,
	"heuristic": 4
}

### Ejemplo 2
{
	"level": "levels/level_soko04.txt",
	"algorithm": "GGS",
	"max_depth": 1000000,
	"max_expanded_nodes": 1000000,
	"iddfs_step": 1,
	"print": true,
	"print_time": 0.2,
	"heuristic": 4
}

## Presentación
Link a la presentación completa
https://docs.google.com/presentation/d/101K4dIfjdomfYOhC5ezxS_zSoD9b9U4eDP1iNeP-s08/edit?usp=sharing