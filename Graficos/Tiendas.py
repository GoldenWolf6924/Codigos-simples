import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime
import calendar

class Evento:
    def __init__(self, nombre, fecha_inicio, fecha_final):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final

def seleccionar_fecha_inicio():
    def guardar_fecha():
        global fecha_inicio
        fecha_inicio = cal.selection_get()
        lbl_fecha_inicio.config(text=f"Fecha de inicio seleccionada: {fecha_inicio}")
        top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    btn_guardar = tk.Button(top, text="Guardar fecha", command=guardar_fecha)
    btn_guardar.pack(pady=10)

def seleccionar_fecha_final():
    def guardar_fecha():
        global fecha_final
        fecha_final = cal.selection_get()
        lbl_fecha_final.config(text=f"Fecha final seleccionada: {fecha_final}")
        top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    btn_guardar = tk.Button(top, text="Guardar fecha", command=guardar_fecha)
    btn_guardar.pack(pady=10)

def agregar_evento():
    nombre_evento = entry_evento.get()
    if not nombre_evento:
        messagebox.showwarning("Advertencia", "Por favor ingresa el nombre del evento.")
    elif fecha_inicio and fecha_final:
        eventos.append(Evento(nombre_evento, fecha_inicio, fecha_final))
        listbox_eventos.insert(tk.END, f"{nombre_evento}: {fecha_inicio} - {fecha_final}")
        entry_evento.delete(0, tk.END)
        lbl_fecha_inicio.config(text="Fecha de inicio no seleccionada")
        lbl_fecha_final.config(text="Fecha final no seleccionada")
    else:
        messagebox.showwarning("Advertencia", "Por favor selecciona ambas fechas.")

def cambiar_nombre_evento():
    selected_index = listbox_eventos.curselection()
    if not selected_index:
        messagebox.showwarning("Advertencia", "Por favor selecciona un evento para cambiar su nombre.")
        return

    old_event = eventos[selected_index[0]]
    new_name = tk.simpledialog.askstring("Cambiar Nombre", f"Ingrese el nuevo nombre para {old_event.nombre}")
    if new_name:
        old_event.nombre = new_name
        listbox_eventos.delete(selected_index)
        listbox_eventos.insert(selected_index, f"{old_event.nombre}: {old_event.fecha_inicio} - {old_event.fecha_final}")



def find_next_weekday(date, weekday):
    """
    Función auxiliar para encontrar el próximo día de la semana dado una fecha
    """
    days_ahead = weekday - date.weekday()
    if days_ahead < 0:  # El día ya es después del día de la semana deseado
        days_ahead += 7
    return date + datetime.timedelta(days_ahead)


def graficar_semanas():
    if not eventos:
        messagebox.showwarning("Advertencia", "Por favor agrega al menos un evento.")
        return

    # Obtener una lista de colores disponibles en matplotlib
    colores = list(mcolors.TABLEAU_COLORS.values())
    color_map = {}
    color_index = 0

    fecha_inicio_min = min(evento.fecha_inicio for evento in eventos)
    fecha_final_max = max(evento.fecha_final for evento in eventos)

    semanas = []
    fecha_inicio_semana = fecha_inicio_min - timedelta(days=fecha_inicio_min.weekday())
    fecha_final_semana = fecha_final_max - timedelta(days=fecha_final_max.weekday()) + timedelta(days=7)
    fecha_actual = fecha_inicio_semana
    while fecha_actual <= fecha_final_semana:
        semanas.append(fecha_actual)
        fecha_actual += timedelta(weeks=1)

    fig, ax = plt.subplots(figsize=(10, 5))

    for evento in eventos:
        if evento.nombre not in color_map:
            color_map[evento.nombre] = colores[color_index % len(colores)]
            color_index += 1

        # Ajustar la fecha de inicio al siguiente día hábil si es fin de semana
        fecha_inicio_evento = find_next_weekday(evento.fecha_inicio, 0)  # 0 representa lunes

        # Calcular la semana de inicio y fin del evento
        semana_inicio_evento = (fecha_inicio_evento - fecha_inicio_semana).days // 7
        semana_fin_evento = (evento.fecha_final - fecha_inicio_semana).days // 7

        # Dibujar la barra horizontal para cada semana del evento
        for i in range(semana_inicio_evento, semana_fin_evento + 1):
            ax.broken_barh([(i, 1)], (eventos.index(evento), 1), facecolors=color_map[evento.nombre])

    ax.set_yticks([i + 0.5 for i in range(len(eventos))])
    ax.set_yticklabels([evento.nombre for evento in eventos])
    ax.set_xticks(range(len(semanas)))
    ax.set_xticklabels([semana.strftime('%d/%m/%Y') for semana in semanas], rotation=45)
    ax.set_xlim(0, len(semanas))  # Ajustar el límite del eje x para que termine una semana después del último evento
    ax.set_xlabel('Fechas')
    ax.set_ylabel('Eventos')
    ax.set_title('Eventos por Semana')
    plt.tight_layout()
    plt.show()



root = tk.Tk()
root.title("Selector de Fechas")

eventos = []
fecha_inicio = None
fecha_final = None

# Etiqueta y entrada para el nombre del evento
lbl_evento = tk.Label(root, text="Nombre del evento:")
lbl_evento.pack(pady=10)

entry_evento = tk.Entry(root, width=50)
entry_evento.pack(pady=10)

lbl_fecha_inicio = tk.Label(root, text="Fecha de inicio no seleccionada")
lbl_fecha_inicio.pack(pady=10)

btn_fecha_inicio = tk.Button(root, text="Seleccionar Fecha de Inicio", command=seleccionar_fecha_inicio)
btn_fecha_inicio.pack(pady=10)

lbl_fecha_final = tk.Label(root, text="Fecha final no seleccionada")
lbl_fecha_final.pack(pady=10)

btn_fecha_final = tk.Button(root, text="Seleccionar Fecha Final", command=seleccionar_fecha_final)
btn_fecha_final.pack(pady=10)

btn_agregar_evento = tk.Button(root, text="Agregar Evento", command=agregar_evento)
btn_agregar_evento.pack(pady=10)

btn_cambiar_nombre = tk.Button(root, text="Cambiar Nombre", command=cambiar_nombre_evento)
btn_cambiar_nombre.pack(pady=10)

btn_graficar_semanas = tk.Button(root, text="Graficar Semanas", command=graficar_semanas)
btn_graficar_semanas.pack(pady=20)

listbox_eventos = tk.Listbox(root, width=80)
listbox_eventos.pack(pady=10)

root.mainloop()
