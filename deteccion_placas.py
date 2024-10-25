import numpy as np  # Biblioteca para manejar matrices
import cv2  # OpenCV para manipulación de imágenes
import matplotlib.pyplot as plt  # Matplotlib para mostrar imágenes
import argparse  # Biblioteca para manejar argumentos desde la línea de comandos
import os  # Biblioteca para trabajar con rutas de archivos
import easyocr  # Biblioteca para OCR

def mul_fragker(fragment, kernel):
    """Multiplica dos matrices elemento por elemento y devuelve la suma."""
    f_row, f_col = fragment.shape
    k_row, k_col = kernel.shape
    resultado = 0.0
    for row in range(f_row):
        for col in range(f_col):
            resultado += fragment[row, col] * kernel[row, col]
    return resultado

def apply_padding(image, pad_height, pad_width):
    """Aplica padding (relleno) con ceros alrededor de la imagen."""
    image_row, image_col = image.shape[:2]
    padded_image = np.zeros((image_row + 2 * pad_height, image_col + 2 * pad_width, 3), dtype=np.uint8)
    padded_image[pad_height:pad_height + image_row, pad_width:pad_width + image_col] = image
    return padded_image

def same_padding(image, kernel):
    """Calcula y aplica el padding necesario para 'same' convolución."""
    pad_height = (kernel.shape[0] - 1) // 2
    pad_width = (kernel.shape[1] - 1) // 2
    return apply_padding(image, pad_height, pad_width)

def convolution(image, kernel, padding=None):
    """Aplica una convolución sobre cada canal de color, con o sin padding."""
    if padding == 'same':
        image = same_padding(image, kernel)

    image_row, image_col, num_channels = image.shape
    kernel_row, kernel_col = kernel.shape

    # Crear la matriz de salida
    output_row = image_row - kernel_row + 1
    output_col = image_col - kernel_col + 1
    output = np.zeros((output_row, output_col, num_channels), dtype=np.float32)

    # Aplicar la convolución en cada canal por separado
    for channel in range(num_channels):
        for row in range(output.shape[0]):
            for col in range(output.shape[1]):
                fragment = image[row:row + kernel_row, col:col + kernel_col, channel]
                output[row, col, channel] = mul_fragker(fragment, kernel)

    return np.clip(output, 0, 255).astype(np.uint8)

def apply_sobel(image, padding='none'):
    """Aplica los filtros Sobel horizontal y vertical y combina los resultados."""
    # Definir los kernels Sobel
    sobel_horizontal = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ])

    sobel_vertical = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    # Aplicar convolución con ambos kernels
    horizontal_output = convolution(image, sobel_horizontal, padding=padding)
    vertical_output = convolution(image, sobel_vertical, padding=padding)

    # Combinar las dos imágenes usando la magnitud de gradiente
    combined_output = np.sqrt(np.square(horizontal_output.astype(np.float32)) +
                              np.square(vertical_output.astype(np.float32)))

    return np.clip(combined_output, 0, 255).astype(np.uint8)

def display_images_side_by_side(image1, image2):
    """Muestra dos imágenes lado a lado usando Matplotlib."""
    image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(image1_rgb)
    axes[0].set_title("Imagen Original")
    axes[0].axis('off')
    axes[1].imshow(image2_rgb)
    axes[1].set_title("Imagen Procesada")
    axes[1].axis('off')
    plt.show()

def extract_text_easyocr(image):
    """Extrae texto de una imagen usando EasyOCR."""
    reader = easyocr.Reader(['en'], gpu=True)  # Inicializar el lector
    results = reader.readtext(image)

    # Mostrar los resultados
    text = ""
    print("Texto Detectado:")
    for (bbox, text_result, prob) in results:
        print(f"Texto: '{text_result}', Confianza: {prob}")
        text += text_result + " "
    return text

def main():
    # Configurar argparse para recibir argumentos por línea de comandos
    ap = argparse.ArgumentParser(description="Aplicación de filtro Sobel y OCR con EasyOCR")
    ap.add_argument("-i", "--image", required=True, help="Ruta de la imagen de entrada")
    ap.add_argument("--padding", choices=['same', 'none'], default='none',
                    help="Selecciona el tipo de padding: 'same' para padding igual al tamaño de entrada, 'none' para sin padding")
    args = vars(ap.parse_args())

    # Leer la imagen usando la ruta proporcionada
    image_path = args["image"]
    if not os.path.isfile(image_path):
        print(f"El archivo '{image_path}' no se encontró.")
        exit(1)

    image = cv2.imread(image_path)  # Leer imagen en color

    # Aplicar los filtros Sobel horizontal y vertical, y combinar los resultados
    padding = args["padding"]
    output_image = apply_sobel(image, padding=padding)

    # Mostrar la imagen original y la procesada lado a lado
    display_images_side_by_side(image, output_image)

    # Extraer y mostrar el texto de la imagen procesada
    detected_text = extract_text_easyocr(output_image)
    print("\nTexto Completo Detectado:")
    print(detected_text)

if __name__ == "__main__":
    main()
