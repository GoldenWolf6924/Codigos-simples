import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from openpyxl import Workbook

# Especifica la ruta completa a tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Si es necesarios cambiar ruta

def preprocess_image(image):
    image = image.convert('L')  
    image = image.filter(ImageFilter.MedianFilter()) 
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2) 
    return image

def extract_text_from_image(image):
    try:
        image = preprocess_image(image)
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text.strip()
    except Exception as e:
        print(f"Se produjo un error al abrir la imagen: {e}")
        return ""

def process_images_in_folder(folder_path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Imagen", "Texto Extraído"])
    
    images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for image_name in images:
        image_path = os.path.join(folder_path, image_name)
        print(f"Procesando imagen: {image_path}")
        image = Image.open(image_path)
        extracted_text = extract_text_from_image(image)
        print("Texto extraído de la imagen:")
        print(extracted_text)
        print("-" * 50)
        
        ws.append([image_name, extracted_text])
    
    excel_file_path = os.path.join(folder_path, "extracted_text.xlsx")
    wb.save(excel_file_path)
    print(f"Se ha guardado el archivo Excel con el texto extraído en: {excel_file_path}")

if __name__ == "__main__":
    folder_path = "C:/Users/Jesus/OneDrive/Codes/img"  
    print(f"Procesando imágenes en la carpeta: {folder_path}")
    process_images_in_folder(folder_path)
