from queue import PriorityQueue
import random
import tkinter as tk
from tkinter import messagebox
import threading
import time


# Principales Diferencias:
# Precisión de la Estimación:

# Manhattan: Más precisa porque considera la distancia real que cada ficha debe recorrer
# Fichas Mal Colocadas: Menos precisa porque solo cuenta si una ficha está o no en su lugar
# Complejidad del Cálculo:

# Manhattan: Más compleja de calcular (requiere calcular distancias)
# Fichas Mal Colocadas: Más simple (solo requiere comparaciones)
# Eficiencia en la Búsqueda:

# Manhattan: Generalmente encuentra la solución explorando menos nodos
# Fichas Mal Colocadas: Suele explorar más nodos para encontrar la solución
# Admisibilidad:

# Ambas son admisibles (nunca sobreestiman el costo real)
# Manhattan es más consistente en su estimación

#La Distancia de Manhattan es generalmente la mejor opción para resolver el 8-puzzle porque:

# Proporciona una mejor estimación del costo real
# Resulta en búsquedas más eficientes
# Encuentra soluciones más óptimas
# Las Fichas Mal Colocadas pueden ser útiles cuando:

# Se necesita una implementación más simple
# El costo computacional de calcular la heurística es una preocupación
# Se están comparando diferentes heurísticas para fines educativos

# Definición del estado objetivo y direcciones posibles
# goal_state: Lista que representa el estado objetivo del puzzle.
# directions: Diccionario que mapea las direcciones de movimiento a sus desplazamientos en la lista del estado.
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
directions = {'up': -3, 'down': 3, 'left': -1, 'right': 1}

# Funciones del Puzzle
# Imprime el estado actual del tablero en formato 3x3.
def print_board(state):
    for i in range(0, len(state), 3):
        print(state[i:i+3])
    print()

# Esta función:

# Copia el estado actual.
# Encuentra el índice del espacio vacío (0).
# Calcula el índice de la posición a intercambiar según la dirección.
# Verifica si el movimiento es válido (no permite movimientos fuera de los límites del tablero).
# Si es válido, intercambia el espacio vacío con la ficha adyacente en la dirección indicada.
# Retorna el nuevo estado después del movimiento.
def move(state, direction):
    new_state = state[:]
    index = new_state.index(0)
    swap_index = index + direction
    if 0 <= swap_index < len(new_state):
        # Evitar movimientos inválidos (ej. mover izquierda desde columna 0)
        if direction == -1 and index % 3 == 0:
            return None
        if direction == 1 and swap_index % 3 == 0:
            return None
        new_state[index], new_state[swap_index] = new_state[swap_index], new_state[index]
        return new_state
    return None

def is_solvable(state):
    inversion_count = 0
    array = [tile for tile in state if tile != 0]
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                inversion_count += 1
    return inversion_count % 2 == 0
# Cuenta el número de inversiones en el estado.
# Una inversión es un par de fichas en el orden incorrecto.
# Si el número de inversiones es par, el puzzle es resoluble.

def manhattan_distance(state):
    distance = 0
    for i, value in enumerate(state):
        if value != 0:
            target_index = goal_state.index(value)
            distance += abs(target_index // 3 - i // 3) + abs(target_index % 3 - i % 3)
    return distance


# Esta heurística:

# Cuenta cuántas fichas no están en su posición objetivo.
# Ofrece una estimación menos precisa que la distancia de Manhattan, pero es más rápida de calcular.
def misplaced_tiles(state):
    return sum(1 for i, value in enumerate(state) if value != 0 and value != goal_state[i])


# Explicación:

# visited: Conjunto para almacenar los estados ya visitados.
# pq: Cola de prioridad que ordena los estados según su costo total estimado (g(n) + h(n)).
# En cada iteración:
# Se extrae el estado con menor costo estimado.
# Se agrega el nodo al grafo si se está visualizando.
# Se verifica si es el estado objetivo.
# Se marcan los estados como visitados.
# Se generan los estados sucesores aplicando movimientos válidos.
# Se calculan los costos y prioridades para los sucesores y se agregan a la cola.
def a_star(initial_state, heuristic):
    visited = set()
    pq = PriorityQueue()
    pq.put((0, initial_state, []))

    while not pq.empty():
        _, state, path = pq.get()
        if state == goal_state:
            return path
        visited.add(tuple(state))
        for direction, shift in directions.items():
            new_state = move(state, shift)
            if new_state and tuple(new_state) not in visited:
                cost = len(path) + 1
                heuristic_cost = heuristic(new_state)
                priority = cost + heuristic_cost
                pq.put((priority, new_state, path + [direction]))
    return None

def generate_solvable_puzzle():
    state = list(range(9))
    while True:
        random.shuffle(state)
        if is_solvable(state):
            return state

# Clase de la Interfaz Gráfica
# Crea la ventana principal y define sus propiedades.
# Genera el estado inicial del puzzle.
# Configura los botones para resolver el puzzle con distintas heurísticas y para reiniciar el puzzle.
class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle Solver")

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.buttons = []
        self.state = generate_solvable_puzzle()
        self.update_board()

        self.solve_button_manhattan = tk.Button(master, text="Resolver con Manhattan", command=self.solve_manhattan)
        self.solve_button_manhattan.pack(pady=5)

        self.solve_button_misplaced = tk.Button(master, text="Resolver con Fichas Mal Colocadas", command=self.solve_misplaced)
        self.solve_button_misplaced.pack(pady=5)

        self.reset_button = tk.Button(master, text="Generar Nuevo Puzzle", command=self.reset_puzzle)
        self.reset_button.pack(pady=5)

    def update_board(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(9):
            tile = self.state[i]
            if tile == 0:
                text = ""
                bg = "lightgray"
            else:
                text = str(tile)
                bg = "lightblue"
            button = tk.Button(self.frame, text=text, width=4, height=2, font=("Helvetica", 24), bg=bg)
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

    def reset_puzzle(self):
        self.state = generate_solvable_puzzle()
        self.update_board()

    def solve_manhattan(self):
        threading.Thread(target=self.solve, args=(manhattan_distance, "Manhattan")).start()
        #nician el proceso de resolución utilizando la heurística seleccionada.
    # Utilizan hilos para evitar que la interfaz se congele durante la ejecución.


    def solve_misplaced(self):
        threading.Thread(target=self.solve, args=(misplaced_tiles, "Fichas Mal Colocadas")).start()

    def solve(self, heuristic, heuristic_name):
        self.disable_buttons()
        print("Resolviendo con A* ({})...".format(heuristic_name))
        solution = a_star(self.state, heuristic)
        if solution:
            print("Ruta:", solution)
            print("Número de pasos:", len(solution))
            for move_direction in solution:
                time.sleep(0.5)  # Pausa para visualizar los movimientos
                self.state = self.apply_move(self.state, move_direction)
                self.update_board()
            messagebox.showinfo("Solución", f"Solución encontrada con {heuristic_name} en {len(solution)} pasos.")
        else:
            messagebox.showerror("Error", "No se encontró solución.")
        self.enable_buttons()
        #         Deshabilitar Botones: Evita interacciones mientras el algoritmo se ejecuta.
        # Crear Grafo: Se inicializa un grafo dirigido para almacenar el árbol de búsqueda.
        # Ejecutar A*: Se llama al algoritmo A* con el estado actual, la heurística y el grafo.
        # Actualizar Tablero: Si se encuentra una solución, se muestra cada movimiento paso a paso.
        # Visualizar Grafo: Se llama a show_graph para mostrar el árbol de búsqueda.
        # Mostrar Mensajes: Informa al usuario si se encontró una solución y cuántos pasos tomó.
        # Habilitar Botones: Permite nuevas interacciones al finalizar.

    def apply_move(self, state, direction):
        shift = directions[direction]
        return move(state, shift) or state

    def disable_buttons(self):
        self.solve_button_manhattan.config(state=tk.DISABLED)
        self.solve_button_misplaced.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.solve_button_manhattan.config(state=tk.NORMAL)
        self.solve_button_misplaced.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

# Función Principal

def main():
    root = tk.Tk()
    gui = EightPuzzleGUI(root)
    root.mainloop()


# Verificar la solvabilidad del estado inicial
initial_state = gui = None  # Inicialización de GUI en main
# main() se llamará después de la definición completa
main()
