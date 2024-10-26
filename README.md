# deteccion_placas.py

README

Este proyecto dentro del respositorio utiliza Teserract OCR (Reconocimiento Optico de caracteres) para extraer texto de cualquier imagen, aunque el programa está diseñado con un enfoque en extraer los caracteres de una placa vehicular. El programa procesa la imagen utilizando los filtros de desenfoque Gaussiano y Laplacian of Gaussian (LoG) antes de extraer el texto usando Teserract para obtener resultados certeros. El programa despliega los caracteres detectados por Teserract con la imagen original y la imagen procesada.

# Librerías Utilizadas

OpenCV: Lee los valores de la imagen y los convierte a escala gris.

NumPy: Para operaciones con matrices, ayuda a la convolución y a aplicar los filtros.

Matplotlib: Para visualizar las imágenes (original y procesada) lado a lado.

Tesseract OCR: Extrae el texto de imágenes.

Argparse: Maneja los argumentos de la línea de comandos.

OS: Permite manipular y verificar rutas de archivos.

# Funcionamiento

El programa toma una imagen de los argumentos de la línea de comandos, procesa la imagen y extrae el texto usando Tesseract:

1. OpenCV lee la imagen desde un archivo
2. Aplica desenfoque Gaussiano y filtro LoG.
3. Tesseract extrae el texto de la imagen original y la procesada.
4. Se despliega la imagen original y la procesada lado a lado.

**Uso**

python deteccion_placas.py --image nombre/de/imagen.jpg --padding same

Argumentos:

1. \- -image: Ruta a la imagen.
2. \- -padding: Tipo de padding a aplicar (same o none). ‘none’ es default y recomendado pero dependerá .

**Ejemplo:**

python deteccion_placas.py --image placa.jpg --padding same

Este proyecto demuestra como el uso de métodos sofisticados como OCR junto con métodos numéricos de procesamiento de imágenes pueden mejorar la detección de texto en imágenes ruidosas.

# Juegos

**figuras.py**

Este código dibuja figuras utilizando el modulo _turtle_. Permite dibujar líneas, cuadrados, círculos, rectángulos y triángulos. El usuario decide el tamaño de las figuras mediante 2 clics que marcan los limites de la misma. Permite cambiar de color (tecla ‘R’ para ‘Red’, ‘Y’ para ‘Yellow’, etc.) y retroceder una acción al presionar ‘U’. La figura dibujada también es controlada mediante el teclado (‘L’ para ‘line’, ‘C’ para ‘circle’, etc).

**snake.py**

Este programa es un juego de snake donde la serpiente y la comida empiezan siendo colores nuevos y diferentes uno del otro. La serpiente se controla mediante las flechas del teclado. Cada que la serpiente toque la comida con su cabeza, se lo “comerá” y aumentara de tamaño 1 punto como un juego normal de snake. Sin embargo, para aumentar el nivel de dificultad, la comida también se moverá hacia una dirección al azar.

**pacman.py**

Este programa es un juego de Pac-Man en Python que utiliza el modulo _turtle_. El jugador controla a Pac-Man, coleccionando puntos y evitar los fantasmas. Las flechas del teclado mueven a Pac-Man en la dirección indicada siempre y cuando no haya una pared inmediatamente. Los fantasmas se mueven hacia Pac-Man siempre que les sea posible.

**tiro.py**

Este programa es un juego donde el usuario controla un cañon colocado en la esquina inferior izquierda de la pantalla que dispara un cañon en dirección del mouse cuando el jugador haga clic. El proyectil sigue la trayectoria de un tiro parabólico – es decir, esta afectada por la “gravedad”. El objetivo del juego es eliminar los targets con las bolas que dispara el cañon. El juego nunca termina, si un target sale de la zona de disparos antes de que el jugador lo elimine, regresará a su posición inicial.

**juego_memoria.py**

Este programa es un memorama en un tablero 8x8. El jugador debe de hacer clic sobre los cuadros para revelar el número y así poder descubrir todos los pares. Cuando el jugador descrube un par, los bloques seleccionados se mantendrán desplegando la parte de la imagen correspondiente a su posición. Cuando el jugador descubre todos los pares, la imagen completa se desplegará al lado del mensaje “Ganaste!”
