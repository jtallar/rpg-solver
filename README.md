# rpg-solver

## Requerimientos
Para correr el solver, es necesario tener instalado `Python 3`. 

Además, debe instalarse `matplotlib`, lo cual se puede lograr con

`python3 -m pip install matplotlib`

### Versiones
Para el desarrollo, se utilizó la versión `Python 3.8.5`

## Ejecución
Para ejecutar el programa, se debe ejecutar desde la raíz del proyecto

`python3 main.py`

## Configuraciones
Todas las configuraciones de ejecución se establecen en el archivo `config.json`. A continuación, se explica a qué hace referencia cada configuración:
- **armas_file** indica el archivo .tsv de armas disponibles. Su ruta se indica desde la raíz del proyecto.
- **botas_file** indica el archivo .tsv de botas disponibles. Su ruta se indica desde la raíz del proyecto.
- **cascos_file** indica el archivo .tsv de cascos disponibles. Su ruta se indica desde la raíz del proyecto.
- **guantes_file** indica el archivo .tsv de guantes disponibles. Su ruta se indica desde la raíz del proyecto.
- **pecheras_file** indica el archivo .tsv de pecheras disponibles. Su ruta se indica desde la raíz del proyecto.
- **max_rows_tsv** indica la máxima cantidad de líneas a leer de cada .tsv . En el caso de los datasets provistos por la cátedra, puede indicarse el número `1000000` o superior para leerlos por completo.

- **player_class** indica el nombre de la clase de personaje a utilizar. Los valores posibles son
    - `guerrero`    --> fitness = 0.6 * Ataque + 0.6 * Defensa
    - `arquero`     --> fitness = 0.9 * Ataque + 0.1 * Defensa
    - `defensor`    --> fitness = 0.3 * Ataque + 0.8 * Defensa
    - `infiltrado`  --> fitness = 0.8 * Ataque + 0.3 * Defensa
- **N** indica el tamaño de la población por cada generación.
- **K** indica la cantidad de hijos a crear por cada iteración.

- **crossover** indica el nombre del operador de cruce a utilizar para generar un par de hijos a partir de un par de padres. Los valores posibles son
    - `one_point`   --> Cruce de un punto
    - `two_points`  --> Cruce de dos puntos
    - `ring`        --> Cruce anular
    - `uniform`     --> Cruce uniforme

- **mutation** indica el nombre del operador de mutación a utilizar para realizar mutaciones sobre los hijos generados. Los valores posibles son
    - `simple_gen`      --> Mutación gen
    - `multi_limited`   --> Mutación multigen limitada (donde M es `limited_multigen_m`)
    - `multi_uniform`   --> Mutación multigen uniforme
    - `full`            --> Mutación completa
- **mutation_probability** indica la probabilidad de mutación a utilizar en dicho operador. Debe estar entre 0 y 1.
- **limited_multigen_m** indica el valor de M para la mutación multigen limitada en caso de elegir dicho operador. Debe estar entre 1 y 6 (cantidad de genes).

- **A** indica la proporción de padres seleccionados con el método `selector_method_1`. Los restantes serán seleccionados con el método `selector_method_2`.
- **selector_method_1** indica el método de selección de padres a utilizar como método 1. Los valores posibles son
    - `elite`                    --> Selector elite
    - `roulette`                 --> Selector ruleta
    - `universal`                --> Selector universal
    - `ranking`                  --> Selector por ranking
    - `boltzmann`                --> Selector boltzmann (donde T0 es `selector_A_boltzmann_t0`, TC `selector_A_boltzmann_tc` y K es `selector_A_boltzmann_k`)
    - `deterministic_tournament` --> Selector por torneo determinístico (donde M es `selector_A_det_tournament_m`)
    - `probabilistic_tournament` --> Selector por torneo probabilístico (donde Th es `selector_A_prob_tournament_th`)
- **selector_method_2** indica el método de selección de padres a utilizar como método 2. Los valores posibles son los mismos que los de `selector_method_1`.
- **selector_A_shuffle** indica si se mezcla (true) o no (false) la salida del selector de padres previo a realizar el cruce.
- **selector_A_det_tournament_m** indica el valor de M para el selector por torneo determinístico en caso de elegir dicho selector de padres. Debe estar entre 1 y N.
- **selector_A_prob_tournament_th** indica el valor de Threshold para el selector por torneo probabilístico en caso de elegir dicho selector de padres. Debe estar entre 0.5 y 1.
- **selector_A_boltzmann_t0** indica el valor de T0 para el selector boltzmann en caso de elegir dicho selector de padres.
- **selector_A_boltzmann_tc** indica el valor de TC para el selector boltzmann en caso de elegir dicho selector de padres. Debe ser menor o igual a `selector_A_boltzmann_t0`.
- **selector_A_boltzmann_k** indica el valor de K para el selector boltzmann en caso de elegir dicho selector de padres.

- **B** indica la proporción de jugadores de reemplazo seleccionados con el método `selector_method_3`. Los restantes serán seleccionados con el método `selector_method_4`.
- **selector_method_3** indica el método de selección de reemplazo a utilizar como método 3. Los valores posibles son
    - `elite`                    --> Selector elite
    - `roulette`                 --> Selector ruleta
    - `universal`                --> Selector universal
    - `ranking`                  --> Selector por ranking
    - `boltzmann`                --> Selector boltzmann (donde T0 es `selector_B_boltzmann_t0`, TC `selector_B_boltzmann_tc` y K es `selector_B_boltzmann_k`)
    - `deterministic_tournament` --> Selector por torneo determinístico (donde M es `selector_B_det_tournament_m`)
    - `probabilistic_tournament` --> Selector por torneo probabilístico (donde Th es `selector_B_prob_tournament_th`)
- **selector_method_4** indica el método de selección de reemplazo a utilizar como método 4. Los valores posibles son los mismos que los de `selector_method_3`.
- **selector_B_det_tournament_m** indica el valor de M para el selector por torneo determinístico en caso de elegir dicho selector de reemplazo. Debe estar entre 1 y N.
- **selector_B_prob_tournament_th** indica el valor de Threshold para el selector por torneo probabilístico en caso de elegir dicho selector de reeplazo. Debe estar entre 0.5 y 1.
- **selector_B_boltzmann_t0** indica el valor de T0 para el selector boltzmann en caso de elegir dicho selector de reemplazo.
- **selector_B_boltzmann_tc** indica el valor de TC para el selector boltzmann en caso de elegir dicho selector de reemplazo. Debe ser menor o igual a `selector_B_boltzmann_t0`.
- **selector_B_boltzmann_k** indica el valor de K para el selector boltzmann en caso de elegir dicho selector de padres.

- **implementation** indica el nombre del método de implementación a utilizar para conformar la nueva generación. Los valores posibles son
    - `fill-all`      --> Implementación Fill-All
    - `fill-parent`   --> Implementación Fill-Parent

- **stopper_time_on** indica si se utiliza (true) o no (false) el criterio de corte por tiempo con parámetro `stop_time_sec`.
- **stop_time_sec** indica la cantidad de segundos máxima de ejecución para el algoritmo genético en caso de habilitar el criterio de corte por tiempo.
- **stopper_generation_count_on** indica si se utiliza (true) o no (false) el criterio de corte por cantidad de generaciones con parámetro `stop_generation_count`.
- **stop_generation_count** indica la cantidad de generaciones máxima para el algoritmo genético en caso de habilitar el criterio de corte por cantidad de generaciones.
- **stopper_diversity_on** indica si se utiliza (true) o no (false) el criterio de corte por diversidad con parámetro `stop_diversity_proportion`.
- **stop_diversity_proportion** indica la diversidad a alcanzar con el algoritmo genético en caso de habilitar el criterio de corte por diversidad. Debe estar entre 0 y 1.
- **stopper_acceptable_on** indica si se utiliza (true) o no (false) el criterio de corte por solución aceptable con parámetro `stop_acceptable_fitness`.
- **stop_acceptable_fitness** indica el fitness mínimo a alcanzar con el algoritmo genético en caso de habilitar el criterio de corte por solución aceptable.
- **stopper_structural_on** indica si se utiliza (true) o no (false) el criterio de corte por estructura con parámetros `stop_structural_gen_count` y `stop_structural_proportion`.
- **stop_structural_gen_count** indica la cantidad de generaciones durante la cual la población no debe cambiar para interrumpir el algoritmo genético en caso de habilitar el criterio de corte por estructura.
- **stop_structural_proportion** indica la proporción de los individuos que deben repetirse como mínimo para considerar que la población no cambió respecto a la generación anterior en caso de habilitar el criterio de corte por estructura. Debe estar entre 0 y 1.
- **stopper_content_on** indica si se utiliza (true) o no (false) el criterio de corte por contenido con parámetro `stop_content_gen_count`.
- **stop_content_gen_count** indica la la cantidad de generaciones durante la cual el mejor fitness no debe cambiar para interrumpir el algoritmo genético en caso de habilitar el criterio de corte por contenido.

- **fitness_delta** indica la tolerancia absoluta a considerar para determinar que dos valores de fitness son iguales. Debe ser un valor en la forma 1eX.

- **random_seed_on** indica si se utiliza (true) o no (false) una semilla particular para la generación de valores aleatorios, donde el valor es `random_seed`. Permite realizar ejecuciones determinísticas.
- **random_seed** indica el valor utilizar como semilla para la generación de valores aleatorios en caso de habilitar el uso de una semilla particular.

- **print_stats** indica si se desea imprimir los valores obtenidos de fitness, diversidad y cambios generación a generación.
- **plot** indica si se desea imprimir el gráfico en tiempo real con los valores de fitness y diversidad obtenidos generación a generación.
- **plot_interval_time** indica el tiempo a esperar entre cada generación para una visualización correcta del gráfico en tiempo real en caso de habilitar el plotteo.

# TODO: Buscar buenos ejemplos para poner aca
### Ejemplo 1
{
}

### Ejemplo 2
{
}

## Presentación
Link a la presentación completa
https://docs.google.com/presentation/d/13eVKhDZRQHDlqhr1fGPwJmzhBG4xjHJRJcl9RUmLvPc/edit?usp=sharing