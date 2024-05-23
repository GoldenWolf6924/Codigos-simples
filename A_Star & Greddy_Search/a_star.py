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
       
        neighbor_cleaned = neighbor.strip().replace("'", "").replace('"', '')  
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
        'Los Angeles': {'San Diego': ((1, 43), 116), 'Barstow': ((1, 38), 114), 'Phoenix': ((5, 17), 372)},
        'San Diego': {'Los Angeles': ((1, 43), 116), 'Ensenada': ((2, 9), 146), 'Barstow': ((2, 31), 176), 'Phoenix': ((5, 13), 350)},
        'Ensenada': {'San Diego': ((2, 9), 146), 'Nogales': ((9, 58), 915)},
        'Barstow': {'Los Angeles': ((1, 38), 114), 'San Diego': ((2, 31), 176)},
        'Phoenix': {'Los Angeles': ((5, 17), 372), 'San Diego': ((5, 13), 350), 'Las Vegas': ((5, 33), 293), 'Flagstaff': ((2, 7), 143), 'Springerville': ((4, 5), 221), 'El Paso': ((6, 15), 429), 'Tucson': ((1, 44), 114)},
        'Nogales': {'Ensenada': ((9, 58), 915), 'Tucson': ((1, 2), 66)},
        'Tucson': {'El Paso': ((4, 38), 317), 'Nogales': ((1, 2), 66), 'Phoenix': ((1, 44), 114)},
        'El Paso': {'Tucson': ((4, 38), 317), 'Phoenix': ((6, 15), 429), 'Albuquerque': ((3, 54), 265), 'Amarillo': ((8, 17), 417), 'Big Spring': ((5, 25), 345)},
        'Big Spring': {'El Paso': ((5, 25), 345), 'Albuquerque': ((7, 27), 430), 'Amarillo': ((3, 56), 227), 'Dallas': ((4, 35), 290)},
        'Amarillo': {'Albuquerque': ((4, 11), 288), 'Lamar': ((3, 36), 215), 'Liberal': ((3, 5), 162), 'Oklahoma City': ((3, 43), 258), 'Dallas': ((5, 29), 362), 'Big Spring': ((3, 56), 227), 'El Paso': ((8, 17), 417)},
        'Dallas': {'Big Spring': ((4, 35), 290), 'Amarillo': ((5, 29), 362), 'Oklahoma City': ((3, 6), 206)},
    }

    heuristic_values = {
        'Los Angeles': {'Los Angeles': 0, 'San Diego': 111.38, 'Ensenada': 179.05, 'Barstow': 90.66, 'Phoenix': 356.90, 'Nogales': 464.13, 'Tucson': 439.21, 'El Paso': 699.37, 'Big Spring': 977.12, 'Amarillo': 935.37, 'Dallas':1237.77 },
        'San Diego': {'Los Angeles': 111.38, 'San Diego': 0, 'Ensenada': 67.82, 'Barstow': 151.04, 'Phoenix': 299.03, 'Nogales': 376.64, 'Tucson': 362.54, 'El Paso': 626.88, 'Big Spring': 914.36, 'Amarillo': 894.35, 'Dallas':1181.78 },
        'Ensenada': {'Los Angeles': 179.05, 'San Diego': 67.82, 'Ensenada': 0, 'Barstow': 211.71, 'Phoenix': 285.74, 'Nogales': 355.41, 'Tucson': 330.50, 'El Paso':593.66 , 'Big Spring': 885.94, 'Amarillo': 880.89, 'Dallas':1156.78 },
        'Barstow': {'Los Angeles': 90.66, 'San Diego': 151.04, 'Ensenada': 211.71, 'Barstow': 0, 'Phoenix': 300.39, 'Nogales': 429.76 , 'Tucson': 394.59, 'El Paso': 645.27, 'Big Spring': 913.11, 'Amarillo': 858.89, 'Dallas':1168.24 },
        'Phoenix': {'Los Angeles': 356.90, 'San Diego': 299.03, 'Ensenada': 285.74, 'Barstow': 300.39, 'Phoenix': 0, 'Nogales': 160.71 , 'Tucson': 106.15 , 'El Paso':345.05  , 'Big Spring': 620.67 , 'Amarillo': 596.52, 'Dallas':884.49 },
        'Nogales': {'Los Angeles': 464.13, 'San Diego': 376.64, 'Ensenada': 355.41, 'Barstow': 429.76 , 'Phoenix': 160.71 , 'Nogales': 0, 'Tucson': 99.68 , 'El Paso': 263.94, 'Big Spring':559.78 , 'Amarillo': 590.52, 'Dallas':834.03 },
        'Tucson': {'Los Angeles': 439.21, 'San Diego': 362.54, 'Ensenada': 330.50, 'Barstow': 394.59, 'Phoenix': 106.15 , 'Nogales':99.68  , 'Tucson': 0, 'El Paso': 264.38, 'Big Spring': 554.99, 'Amarillo':564.01 , 'Dallas':826.29  },
        'El Paso': {'Los Angeles': 699.37, 'San Diego':626.88 , 'Ensenada':593.66 , 'Barstow': 645.27, 'Phoenix':345.05  , 'Nogales':263.94 , 'Tucson': 264.38, 'El Paso': 0, 'Big Spring': 295.97, 'Amarillo': 358.86 , 'Dallas':570.60 },
        'Big Spring': {'Los Angeles': 977.12, 'San Diego':914.36 , 'Ensenada':885.94 , 'Barstow':913.11 , 'Phoenix':620.67  , 'Nogales':559.78 , 'Tucson': 554.99, 'El Paso':295.97 , 'Big Spring': 0, 'Amarillo': 206.01, 'Dallas':274.97 },
        'Amarillo': {'Los Angeles': 935.37, 'San Diego': 894.35, 'Ensenada': 880.89, 'Barstow': 858.89, 'Phoenix':596.52 , 'Nogales':590.52 , 'Tucson': 564.01, 'El Paso': 358.86 , 'Big Spring':206.01 , 'Amarillo': 0, 'Dallas': 333.68},
        'Dallas': {'Los Angeles': 1237.77, 'San Diego': 1181.78, 'Ensenada': 1156.78, 'Barstow': 1168.24, 'Phoenix': 884.49, 'Nogales': 834.03, 'Tucson': 826.29 , 'El Paso': 570.60, 'Big Spring':274.97 , 'Amarillo':333.68 , 'Dallas': 0},
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


