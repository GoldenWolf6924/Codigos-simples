
import pyautogui
import time

try:
    while True:
        # Obtener la posición actual del ratón
        x, y = pyautogui.position()
        
        # Obtener el color del píxel en la posición actual del ratón
        current_color = pyautogui.pixel(x, y)
        
        # Imprimir la posición y el valor RGB del píxel
        print(f"Posición: ({x}, {y}), Color: {current_color}")
        
        # Esperar 2 segundos antes de revisar de nuevo
        time.sleep(2)

except KeyboardInterrupt:
    # Salida limpia cuando el usuario interrumpe el script
    print("Saliendo del script.")

except Exception as e:
    # Manejar cualquier excepción inesperada
    print(f"Ocurrió un error: {e}")
