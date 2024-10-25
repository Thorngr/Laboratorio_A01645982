import numpy as np  # Biblioteca para manejar matrices
import cv2  # OpenCV para manipulación de imágenes
import matplotlib.pyplot as plt  # Matplotlib para mostrar imágenes
import argparse  # Biblioteca para manejar argumentos desde la línea de comandos
import os  # Biblioteca para trabajar con rutas de archivos
import pytesseract  # Biblioteca para Tesseract OCR

def mul_fragker(fragment, kernel):
    # Multiplica dos matrices elemento por elemento y devuelve la suma.
    f_row, f_col = fragment.shape
    k_row, k_col = kernel.shape
    resultado = 0.0
    for row in range(f_row):
        for col in range(f_col):
            resultado += fragment[row, col] * kernel[row, col]
    return resultado

def apply_same_padding(image, kernel):
    # Calcula y aplica el padding necesario para 'same' convolución.
    pad_height = (kernel.shape[0] - 1) // 2
    pad_width = (kernel.shape[1] - 1) // 2
    image_row, image_col = image.shape
    padded_image = np.zeros((image_row + 2 * pad_height, image_col + 2 * pad_width), dtype=np.uint8)
    padded_image[pad_height:pad_height + image_row, pad_width:pad_width + image_col] = image
    return padded_image

def convolution(image, kernel, padding='none'):
    # Aplica una convolución sobre la imagen, con padding opcional.
    if padding == 'same':
        image = apply_same_padding(image, kernel)

    image_row, image_col = image.shape
    kernel_row, kernel_col = kernel.shape

    # Crear la matriz de salida
    output_row = image_row - kernel_row + 1
    output_col = image_col - kernel_col + 1
    output = np.zeros((output_row, output_col), dtype=np.float32)

    # Aplicar la convolución en la imagen
    for row in range(output.shape[0]):
        for col in range(output.shape[1]):
            fragment = image[row:row + kernel_row, col:col + kernel_col]
            output[row, col] = mul_fragker(fragment, kernel)

    return np.clip(output, 0, 255).astype(np.uint8)

def apply_gaussian_blur(image, padding='same'):
    # Aplica un filtro de blur Gaussiano.
    gaussian_kernel = (1 / 1404) * np.array([
        [0, 0, 0,  5, 0, 0, 0], 
        [0, 5, 18, 32, 18, 5, 0],
        [0, 18, 64, 100, 64, 18, 0],
        [5, 32, 100, 100, 100, 32, 5],
        [0, 18, 64, 100, 64, 18, 0],
        [0, 5, 18, 32, 18, 5, 0],
        [0, 0, 0,  5, 0, 0, 0]
    ])
    return convolution(image, gaussian_kernel, padding=padding)

def apply_log_filter(image, padding='same'):
    # Aplica el filtro Laplaciano de Gaussiano.
    log_kernel = np.array([
        [0,  0, -1,  0,  0],
        [0, -1, -2, -1,  0], 
        [-1, -2, 16, -2, -1],
        [0, -1, -2, -1,  0], 
        [0,  0, -1,  0,  0]
    ])
    return convolution(image, log_kernel, padding=padding)

def display_placas(image1, image2):
    # Muestra las placas lado a lado usando Matplotlib.
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(image1, cmap='gray')
    axes[0].set_title("Imagen Original")
    axes[0].axis('off')
    axes[1].imshow(image2, cmap='gray')
    axes[1].set_title("Imagen Procesada")
    axes[1].axis('off')
    plt.show()

def extract_text_tesseract(image, label):
    # Extrae y despliega texto de una imagen usando Tesseract.
    text = pytesseract.image_to_string(image, config='--psm 8')
    print(f"\nTexto completo detectado ({label}):")
    print(text)
    return text

def main():
    ap = argparse.ArgumentParser(description="Aplicación de OCR con Tesseract")
    ap.add_argument("-i", "--image", required=True, help="Ruta de la imagen de entrada")
    ap.add_argument("--padding", choices=['same', 'none'], default='none', help="Tipo de padding a usar")
    args = vars(ap.parse_args())

    # Leer la imagen usando la ruta proporcionada
    image_path = args["image"]
    padding = args["padding"]

    if not os.path.isfile(image_path):
        print(f"El archivo '{image_path}' no se encontró.")
        exit(1)

    # Leer la imagen
    image = cv2.imread(image_path)  

    # Extraer y mostrar texto de la imagen original
    extract_text_tesseract(image, "placa original")

    # Convertir la imagen a escala de grises para aplicar filtros
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro Gaussiano antes del filtro LoG
    blurred_image = apply_gaussian_blur(grayscale_image, padding=padding)

    # Aplicar el filtro Laplaciano de Gaussiano (LoG)
    log_image = apply_log_filter(blurred_image, padding=padding)

    # Extraer y mostrar texto de la imagen filtrada
    extract_text_tesseract(log_image, "placa con filtros")

    # Mostrar la imagen original y la procesada lado a lado
    display_placas(grayscale_image, log_image)

main()
