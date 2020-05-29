import noise
import numpy as np
from scipy.spatial import distance
from PIL import Image, ImageDraw


max_color = (246, 203, 29)
min_color = (255, 85, 0)


def generate_fire(n: int, width: int, scale: int, seed: int)->None:
    """
    Genera un png a partir de perlin noise en 3D
    :param seed: semilla de inicialización
    :param n: numero de secuencia
    :param width: ancho y alto de la imagen
    :param scale: es
    :return:
    """
    print("Imagen ", n)
    fire = np.zeros((width, width))
    reference_point = (width - 1, int((width - 1) - (width - 1) / 2.0))
    k = n/(13)
    for i in range(width):
        for j in range(width):
            perlin_one = noise.pnoise3((i / scale), j / scale, k, octaves=8, persistence=0.5,
                                       lacunarity=1.0, repeatx=1024, repeaty=1024,
                                       base=seed)
            perlin_two = noise.pnoise3(i / (scale / 2), j / (scale / 2) , k, octaves=8, persistence=0.4,
                                       lacunarity=2.0, repeatx=1024, repeaty=1024,
                                       base=seed)
            perlin_three = noise.pnoise3((i + 60 / scale), j - 20 / scale , k, octaves=8, persistence=1,
                                         lacunarity=0.5, repeatx=1024, repeaty=1024,
                                         base=seed)
            fire[i][j] = (perlin_one * 0.5) + (perlin_two * 0.5) + perlin_three - distance.euclidean((i + 20, j),
                                                                reference_point) / (scale * 10)
    img = generate_output(fire)
    img.save("./outputs/" + str(n) + ".png")


def generate_gif(frames: int) -> None:
    """
    Genera un gif infinito a partir de los frames
    :param frames: número de imagenes generadas
    :return:
    """
    images = []
    for img in range(frames):
        images.append(Image.open("./outputs/" + str(img) + ".png"))
    for img_back in range(frames - 2, 0, -1):
        images.append(Image.open("./outputs/" + str(img_back) + ".png"))

    images[0].save('fire.gif', save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)


def normalized_val(val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normaliza un valor entre 0 y 1 comparativamente a min_val y max_val
    :param val: valor a normalizar
    :param min_val: valor mínimo de referencia (será igual a 0)
    :param max_val: valor máximo de referencia (será igual a 1)
    :return: valor normalizado entre 0 y 1
    """
    return (val - min_val) / (max_val - min_val)


def normalized(data: [[float]]) -> [[float]]:
    """
    Normaliza una matriz, transformándola para que su valor mínimo sea 0.0 y el máximo 1.0
    :param data:
    :return:
    """
    transformed = np.copy(data)
    max_val = np.max(transformed)
    min_val = np.min(transformed)

    for r in range(len(transformed)):
        for c in range(len(transformed[r])):
            transformed[r][c] = normalized_val(transformed[r][c], min_val, max_val)
    return transformed


def get_target_color(val: float) -> (int, int, int, int):
    """
    Obtiene el color correspondiente a un valor.
    Será max_color si el valor es el valor máximo de self._data,
    min_color si es el valor mínimo y uno intermedio en otro caso
    :param val: valor del que queramos obtener el color
    :return: color RGBA con valores en el rango 0-255
    """
    normalized_ = normalized_val(val)
    target_r = int((max_color[0] - min_color[0]) * normalized_ + min_color[0])
    target_g = int((max_color[1] - min_color[1]) * normalized_ + min_color[1])
    target_b = int((max_color[2] - min_color[2]) * normalized_ + min_color[2])
    target_alpha = int(255 * normalized_ + 150)
    return target_r, target_g, target_b, target_alpha


def generate_output(data):
    """
    Genera una imagen RGBA a partir de una matriz de datos
    """
    img = Image.new('RGB', (len(data), len(data[0])))
    draw = ImageDraw.Draw(img, 'RGBA')
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            draw.point((x, y), fill=get_target_color(value))
    del draw
    return img
