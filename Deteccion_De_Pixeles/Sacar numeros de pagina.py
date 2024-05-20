import pyautogui
import time
import webcolors
import os

directory = "C:\\Users\\Jesus\\OneDrive\\Codes\\img"

if not os.path.exists(directory):
    os.makedirs(directory)

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_color_name(rgb_color):
    try:
        color_name = webcolors.rgb_to_name(rgb_color)
    except ValueError:
        color_name = closest_color(rgb_color)
    return color_name

i = 0

# Definición del color rojo (tomato)
tomato = (255, 61, 61)

# Dimensiones para la captura de pantalla
width = 500
height = 90

try:
    while True:
        i += 1
        x,y = (968, 484)
        w,z = (935, 457)
        a,b = (780,420)
        current_color = pyautogui.pixel(x, y)
        color_secundario = (w,z)
        color_name = get_color_name(current_color)
        
        if current_color == tomato or color_secundario == tomato:
            timestamp = time.strftime("%Y%m%d%H%M%S")
            filename = os.path.join(directory, f"screenshot_{timestamp}.png")
            
            screenshot = pyautogui.screenshot(region=(a, b, width, height))
            screenshot.save(filename)
            print("Captura de pantalla guardada como:", filename)
            time.sleep(3)
        else:
            print(f"{i}.-\tNo se detectó un cambio a color rojo. El color actual es {color_name} y la posición del mouse es ({x}, {y})")
            time.sleep(1)
except KeyboardInterrupt:
    print("Exiting the script due to KeyboardInterrupt.")
except Exception as e:
    print(f"An error occurred: {e}")