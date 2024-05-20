import heapq
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import numpy as np  

class Node:
    def __init__(self, city, parent=None, g=0, h=0):
        self.city = city
        self.parent = parent
        self.g = g  # Costo real 
        self.h = h  # Heurística 

    def f(self):
        return self.g + self.h  # Costo total estimado de llegar al objetivo desde el nodo inicial pasando por este nodo

def heuristic(city, goal_city, heuristic_values):
    if city in heuristic_values and goal_city in heuristic_values[city]:
        return heuristic_values[city][goal_city]
    else:
        return float('inf')

def successors(city, distances):
    successors = []
    for neighbor, (distance_time, distance_miles) in distances[city].items():
        # Limpiar el nombre de la ciudad
        neighbor_cleaned = neighbor.strip().replace("'", "").replace('"', '')  # Eliminar comillas u otros caracteres no deseados
        # Verificar si la distancia no es nula
        if pd.notna(distance_miles):
            successors.append((neighbor_cleaned, int(distance_miles)))
    return successors

def astar(start_city, goal_city, heuristic_values, distances):
    open_list = []
    closed_set = set()

    start_node = Node(start_city, g=0, h=heuristic(start_city, goal_city, heuristic_values))
    heapq.heappush(open_list, (start_node.f(), id(start_node), start_node))

    while open_list:
        _, _, current_node = heapq.heappop(open_list)

        if current_node.city == goal_city:
            path = []
            while current_node:
                path.append(current_node.city)
                current_node = current_node.parent
                lista_invertida = path[::-1]
                print("Lista antes de pasarla:",lista_invertida)
            return path[::-1]

        closed_set.add(current_node.city)

        for successor_city, cost in successors(current_node.city, distances):
            if successor_city in closed_set:
                continue

            g = current_node.g + cost
            h = heuristic(successor_city, goal_city, heuristic_values)
            successor_node = Node(successor_city, parent=current_node, g=g, h=h)
            heapq.heappush(open_list, (successor_node.f(), id(successor_node), successor_node))
        
    return None

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def print_path_in_window(path, distances):
    total_distance = 0
    total_time_minutes = 0
    total_time_seconds = 0
    path_str = ""

    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i + 1]
        distance_time, distance = distances[city1][city2]

        # Verificar si distance_time es None o no
        if distance_time is not None:
            minutes, seconds = distance_time
            total_time_minutes += minutes
            total_time_seconds += seconds
            path_str += f"{city1} -> {city2}: {distance} millas, {minutes:02d}:{seconds:02d}\n"
        else:
            path_str += f"{city1} -> {city2}: {distance} millas, Tiempo no disponible\n"

        total_distance += distance

    # Convertir los segundos extras a minutos si es necesario
    total_time_minutes += total_time_seconds // 60
    total_time_seconds %= 60

    root = tk.Tk()
    root.title("Resultado")
    root.geometry("400x200")

    result_label = ttk.Label(root, text=f"Camino optimo encontrado:\n{path_str}\nDistancia total: {total_distance} millas\nTiempo total: {total_time_minutes:02d} minutos con {total_time_seconds:02d} segundos")
    result_label.pack(padx=10, pady=10)

    def close_window():
        root.destroy()

    ok_button = ttk.Button(root, text="OK", command=close_window)
    ok_button.pack(pady=5)

    root.mainloop()


def greedy_search(start_city, goal_city, heuristic_values, distances):
    open_list = []
    closed_set = set()
    ciudades_visitadas = []

    start_node = Node(start_city, h=heuristic(start_city, goal_city, heuristic_values))
    heapq.heappush(open_list, (start_node.f(), id(start_node), start_node))

    while open_list:
        _, _, current_node = heapq.heappop(open_list)

        if current_node.city == goal_city:
            path = [] 
            ciudades_visitadas.append(goal_city)
            path = ciudades_visitadas
            print("Prueba:",path)

            return path[::1]

        closed_set.add(current_node.city)

        for successor_city, cost in successors(current_node.city, distances):
            if successor_city in closed_set:
                continue
            h = heuristic(successor_city, goal_city, heuristic_values)
            successor_node = Node(successor_city, parent=current_node, h=h)
            heapq.heappush(open_list, (successor_node.f(), id(successor_node), successor_node))
            nueva_ciudad = current_node.city
            if nueva_ciudad not in ciudades_visitadas:
                ciudades_visitadas.append(nueva_ciudad)
            print(ciudades_visitadas)
    return None





def get_start_goal_cities(distances, heuristic_values):
    def go_back_to_main_menu():
        root.destroy()
        ask_user_for_data()

    def ok():
        start_city = start_var.get()
        goal_city = goal_var.get()
        if search_algorithm_var.get() == "A*":
            path = astar(start_city, goal_city, heuristic_values, distances)
        else:
            path = greedy_search(start_city, goal_city, heuristic_values, distances)
        if path:
            print_path_in_window(path, distances)
        else:
            messagebox.showinfo("Error", "No se encontró un camino")
        root.destroy()  

    root = tk.Tk()
    root.title("Seleccionar ciudades")
    root.geometry("350x180")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    label_start = ttk.Label(main_frame, text="Ciudad de inicio:")
    label_start.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    start_var = tk.StringVar(root)
    start_var.set(list(distances.keys())[0])
    start_menu = ttk.Combobox(main_frame, textvariable=start_var, values=list(distances.keys()), state="readonly")
    start_menu.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    label_goal = ttk.Label(main_frame, text="Ciudad de destino:")
    label_goal.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    goal_var = tk.StringVar(root)
    goal_var.set(list(distances.keys())[0])
    goal_menu = ttk.Combobox(main_frame, textvariable=goal_var, values=list(distances.keys()), state="readonly")
    goal_menu.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    label_algorithm = ttk.Label(main_frame, text="Algoritmo de búsqueda:")
    label_algorithm.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    search_algorithm_var = tk.StringVar(root)
    search_algorithm_var.set("A*")
    search_algorithm_menu = ttk.Combobox(main_frame, textvariable=search_algorithm_var, values=["A*", "Greedy Search"], state="readonly")
    search_algorithm_menu.grid(row=2, column=1, padx=5, pady=5, sticky="we")

    ok_button = ttk.Button(main_frame, text="OK", command=ok)
    ok_button.grid(row=3, column=1, padx=(5, 0), pady=5, sticky="we")

    back_button = ttk.Button(main_frame, text="Regresar", command=go_back_to_main_menu)
    back_button.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="we")

    root.mainloop()
def get_predefined_data():
    distances = {
        'Los Angeles': {'San Diego': ((1, 50), 116), 'Barstow': ((1, 35), 114), 'Phoenix': ((4, 20), 372)},
        'San Diego': {'Los Angeles': ((1, 50), 116), 'Ensenada': ((3, 10), 146), 'Barstow': ((3, 20), 176), 'Phoenix': ((6, 30), 350)},
        'Ensenada': {'San Diego': ((3, 10), 146), 'Nogales': ((18, 20), 915)},
        'Barstow': {'Los Angeles': ((1, 35), 114), 'San Diego': ((3, 20), 176)},
        'Phoenix': {'Los Angeles': ((4, 20), 372), 'San Diego': ((6, 30), 350), 'Las Vegas': ((5, 50), 293), 'Flagstaff': ((3, 0), 143), 'Springerville': ((4, 20), 221), 'El Paso': ((7, 50), 429), 'Tucson': ((2, 30), 114)},
        'Nogales': {'Ensenada': ((18, 20), 915), 'Tucson': ((1, 25), 66)},
        'Tucson': {'El Paso': ((6, 0), 317), 'Nogales': ((1, 25), 66), 'Phoenix': ((2, 30), 114)},
        'El Paso': {'Tucson': ((6, 0), 317), 'Phoenix': ((7, 50), 429), 'Albuquerque': ((5, 0), 265), 'Amarillo': ((7, 50), 417), 'Big Spring': ((6, 40), 345)},
        'Big Spring': {'El Paso': ((6, 40), 345), 'Albuquerque': ((7, 50), 430), 'Amarillo': ((4, 30), 227), 'Dallas': ((5, 30), 290)},
        'Amarillo': {'Albuquerque': ((5, 30), 288), 'Lamar': ((5, 20), 275), 'Liberal': ((3, 20), 162), 'Oklahoma City': ((5, 0), 258), 'Dallas': ((6, 50), 362), 'Big Spring': ((4, 30), 227), 'El Paso': ((7, 50), 417)},
        'Dallas': {'Big Spring': ((5, 30), 290), 'Amarillo': ((6, 50), 362), 'Oklahoma City': ((4, 10), 206)},
    }

    heuristic_values = {
        'Los Angeles': {'Los Angeles': 0, 'San Diego': 115, 'Ensenada': 160, 'Barstow': 105, 'Phoenix': 340, 'Nogales': 290, 'Tucson': 480, 'El Paso': 700, 'Big Spring': 900, 'Amarillo': 950, 'Dallas':1237 },
        'San Diego': {'Los Angeles': 115, 'San Diego': 0, 'Ensenada': 140, 'Barstow': 150, 'Phoenix': 310, 'Nogales': 300, 'Tucson': 460, 'El Paso': 680, 'Big Spring': 880, 'Amarillo': 930, 'Dallas':1181 },
        'Ensenada': {'Los Angeles': 160, 'San Diego': 140, 'Ensenada': 0, 'Barstow': 100, 'Phoenix': 320, 'Nogales': 310, 'Tucson': 470, 'El Paso': 690, 'Big Spring': 890, 'Amarillo': 940, 'Dallas': 1250},
        'Barstow': {'Los Angeles': 105, 'San Diego': 150, 'Ensenada': 100, 'Barstow': 0, 'Phoenix': 250, 'Nogales': 330, 'Tucson': 490, 'El Paso': 710, 'Big Spring': 910, 'Amarillo': 960, 'Dallas': 1168},
        'Phoenix': {'Los Angeles': 340, 'San Diego': 310, 'Ensenada': 320, 'Barstow': 250, 'Phoenix': 0, 'Nogales': 180, 'Tucson': 130, 'El Paso': 350, 'Big Spring': 550, 'Amarillo': 600, 'Dallas': 884},
        'Nogales': {'Los Angeles': 290, 'San Diego': 300, 'Ensenada': 310, 'Barstow': 330, 'Phoenix': 180, 'Nogales': 0, 'Tucson': 70, 'El Paso': 260, 'Big Spring': 460, 'Amarillo': 510, 'Dallas': 930},
        'Tucson': {'Los Angeles': 480, 'San Diego': 460, 'Ensenada': 470, 'Barstow': 490, 'Phoenix': 130, 'Nogales': 70, 'Tucson': 0, 'El Paso': 210, 'Big Spring': 410, 'Amarillo': 460, 'Dallas': 826},
        'El Paso': {'Los Angeles': 700, 'San Diego': 680, 'Ensenada': 690, 'Barstow': 710, 'Phoenix': 350, 'Nogales': 260, 'Tucson': 210, 'El Paso': 0, 'Big Spring': 200, 'Amarillo': 250, 'Dallas': 570},
        'Big Spring': {'Los Angeles': 900, 'San Diego': 880, 'Ensenada': 890, 'Barstow': 910, 'Phoenix': 550, 'Nogales': 460, 'Tucson': 410, 'El Paso': 200, 'Big Spring': 0, 'Amarillo': 120, 'Dallas': 274},
        'Amarillo': {'Los Angeles': 950, 'San Diego': 930, 'Ensenada': 940, 'Barstow': 960, 'Phoenix': 600, 'Nogales': 510, 'Tucson': 460, 'El Paso': 250, 'Big Spring': 120, 'Amarillo': 0, 'Dallas': 273},
        'Dallas': {'Los Angeles': 1237, 'San Diego': 1181, 'Ensenada': 1250, 'Barstow': 1168, 'Phoenix': 884, 'Nogales': 930, 'Tucson': 826, 'El Paso': 570, 'Big Spring': 274, 'Amarillo': 273, 'Dallas': 0},
    }
    return distances, heuristic_values

def load_data_from_user():
    def select_distances_file():
        distances_file_path = filedialog.askopenfilename(title="Seleccionar archivo de distancias")
        if distances_file_path:
            heuristic_values_button["state"] = "normal"
            distances_entry.insert(tk.END, distances_file_path)

    def select_heuristic_values_file():
        heuristic_values_file_path = filedialog.askopenfilename(title="Seleccionar archivo de valores heurísticos")
        if heuristic_values_file_path:
            load_data_button["state"] = "normal"
            heuristic_values_entry.insert(tk.END, heuristic_values_file_path)

   

    def load_data():
        distances_file_path = distances_entry.get()
        heuristic_values_file_path = heuristic_values_entry.get()
        load_data_from_excel(distances_file_path, heuristic_values_file_path)


    def go_back_to_main_menu():
        root.destroy()
        ask_user_for_data()

    root = tk.Tk()
    root.title("Cargar datos desde archivos")
    root.geometry("565x160")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    distances_label = ttk.Label(main_frame, text="Archivo de distancias con tiempos:")
    distances_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    distances_entry = ttk.Entry(main_frame, width=40)
    distances_entry.grid(row=0, column=1, padx=5, pady=5)

    distances_button = ttk.Button(main_frame, text="Seleccionar", command=select_distances_file)
    distances_button.grid(row=0, column=2, padx=5, pady=5)

    heuristic_values_label = ttk.Label(main_frame, text="Archivo de valores heurísticos:")
    heuristic_values_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    heuristic_values_entry = ttk.Entry(main_frame, width=40)
    heuristic_values_entry.grid(row=1, column=1, padx=5, pady=5)

    heuristic_values_button = ttk.Button(main_frame, text="Seleccionar", command=select_heuristic_values_file, state="disabled")
    heuristic_values_button.grid(row=1, column=2, padx=5, pady=5)

    load_data_button = ttk.Button(main_frame, text="Cargar Datos", command=load_data, state="disabled")
    load_data_button.grid(row=3, column=0, padx=(5, 2), pady=5, sticky="we", columnspan=3)

    back_button = ttk.Button(main_frame, text="Regresar", command=go_back_to_main_menu)
    back_button.grid(row=4, column=0, padx=(5, 2), pady=5, sticky="we", columnspan=3)

    root.mainloop()

def load_data_from_excel(distances_file_path, heuristic_values_file_path):
    if not distances_file_path or not heuristic_values_file_path:
        messagebox.showinfo("Error", "Por favor seleccione ambos archivos.")
        return

    try:
        distances_df = pd.read_excel(distances_file_path, index_col=0)
        heuristic_values_df = pd.read_excel(heuristic_values_file_path, index_col=0)
    except Exception as e:
        messagebox.showinfo("Error", f"Error al cargar archivos: {str(e)}")
        return

    distances = {}
    heuristic_values = {}

    # Procesar el archivo de distancias
    for city in distances_df.index:
        distances[city] = {}

        for column in distances_df.columns:
            # Obtener el valor de la celda
            distance_time_str = str(distances_df.loc[city, column]).strip()

            # Verificar si el valor no es NaN y no está vacío
            if distance_time_str and distance_time_str != 'nan':
                # Verificar si la cadena contiene una coma antes de intentar dividirla
                if ',' in distance_time_str:
                    distance, time = distance_time_str.split(',')  # Dividir la cadena por la coma

                    # Convertir la distancia a un entero y el tiempo a minutos y segundos
                    distance = int(distance)
                    time_parts = time.split(':')
                    minutes = int(time_parts[0])
                    seconds = int(time_parts[1])

                    # Guardar la distancia y el tiempo en la estructura de datos
                    distances[city][column] = ((minutes, seconds), distance)
                else:
                    # Manejar el caso donde no hay una coma en la cadena
                    print(f"Error: La cadena '{distance_time_str}' no contiene una coma.")


    # Procesar el archivo de valores heurísticos
    for city in heuristic_values_df.index:
        heuristic_values[city] = {}

        for column in heuristic_values_df.columns:
            heuristic_values[city][column] = int(heuristic_values_df.loc[city, column])

    get_start_goal_cities(distances, heuristic_values)


def ask_user_for_data():
    def load_predefined_data():
        distances, heuristic_values = get_predefined_data()
        get_start_goal_cities(distances, heuristic_values)

    def load_data_from_files():
        load_data_from_user()

    root = tk.Tk()
    root.title("Planificador de rutas")
    root.geometry("340x85")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    predefined_data_button = ttk.Button(main_frame, text="Usar datos predefinidos", command=load_predefined_data, width=50)
    predefined_data_button.grid(row=0, column=0, padx=5, pady=5, sticky="we")

    load_data_files_button = ttk.Button(main_frame, text="Importar desde archivos", command=load_data_from_files, width=50)
    load_data_files_button.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    root.mainloop()

if __name__ == "__main__":
    ask_user_for_data()


