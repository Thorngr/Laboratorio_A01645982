import numpy as np  # Biblioteca para manejar matrices
import cv2  # OpenCV para manipulación de imágenes
import matplotlib.pyplot as plt  # Matplotlib para mostrar imágenes
import argparse  # Biblioteca para manejar argumentos desde la línea de comandos
import os  # Biblioteca para trabajar con rutas de archivos

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

def main():
    # Configurar argparse para recibir argumentos por línea de comandos
    ap = argparse.ArgumentParser(description="Aplicación de filtro Sobel a una imagen")
    ap.add_argument("-i", "--image", required=True, help="Ruta de la imagen de entrada")
    ap.add_argument("--padding", choices=['same', 'none'], default='none',
                    help="Selecciona el tipo de padding: 'same' para padding de salida igual al tamaño de entrada, 'none' para sin padding")
    args = vars(ap.parse_args())

    # Leer la imagen usando la ruta proporcionada
    image_path = args["image"]
    if not os.path.isfile(image_path):
        print(f"El archivo '{image_path}' no se encontró.")
        exit(1)

    image = cv2.imread(image_path)  # Leer imagen en color

    # Definir el kernel Sobel
    sobel_kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    # Aplicar la convolución con o sin padding
    padding = args["padding"]
    output_image = convolution(image, sobel_kernel, padding=padding)

    # Mostrar la imagen original y la procesada lado a lado
    display_images_side_by_side(image, output_image)

if __name__ == "__main__":
    main()
