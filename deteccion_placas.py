import numpy as np  # Biblioteca para manejar matrices
import cv2  # OpenCV para manipulación de imágenes
import matplotlib.pyplot as plt  # Matplotlib para mostrar imágenes
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

def convolution(image, kernel):
    """Aplica una convolución válida (sin padding) sobre cada canal de color."""
    image_row, image_col, num_channels = image.shape
    kernel_row, kernel_col = kernel.shape

    output = np.zeros((image_row - kernel_row + 1, image_col - kernel_col + 1, num_channels), dtype=np.float32)

    for channel in range(num_channels):
        for row in range(output.shape[0]):
            for col in range(output.shape[1]):
                fragment = image[row:row + kernel_row, col:col + kernel_col, channel]
                output[row, col, channel] = mul_fragker(fragment, kernel)

    return np.clip(output, 0, 255).astype(np.uint8)

def read_image(image_path):
    """Lee una imagen en color desde la ruta dada."""
    return cv2.imread(image_path)  # Leer imagen en color (BGR)

def save_image(image, output_path):
    """Guarda la imagen en la ruta especificada."""
    cv2.imwrite(output_path, image)

def display_images_side_by_side(image1, image2):
    """Muestra dos imágenes lado a lado usando Matplotlib."""
    # Convertir de BGR a RGB para que Matplotlib muestre los colores correctamente
    image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Crear figura con 2 columnas

    # Mostrar la imagen original
    axes[0].imshow(image1_rgb)
    axes[0].set_title("Imagen Original")
    axes[0].axis('off')  # Ocultar ejes

    # Mostrar la imagen procesada
    axes[1].imshow(image2_rgb)
    axes[1].set_title("Imagen Procesada")
    axes[1].axis('off')  # Ocultar ejes

    plt.show()  # Mostrar ambas imágenes en la misma ventana

if __name__ == "__main__":
    # Pedir al usuario el nombre del archivo de la imagen
    image_name = input("Ingresa el nombre de la imagen (con extensión, por ejemplo, 'imagen.jpg'): ")

    # Verificar si el archivo existe en la carpeta actual
    if not os.path.isfile(image_name):
        print(f"El archivo '{image_name}' no se encontró en la carpeta actual.")
        exit(1)

    # Leer la imagen de entrada
    input_image = read_image(image_name)

    # Definir un kernel Sobel
    sobel_kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    # Aplicar la convolución
    output_image = convolution(input_image, sobel_kernel)

    # Mostrar las imágenes lado a lado
    display_images_side_by_side(input_image, output_image)

    # Guardar la imagen procesada
    output_name = f"procesado_{image_name}"
    save_image(output_image, output_name)

    print(f"La imagen procesada se guardó como '{output_name}'.")
