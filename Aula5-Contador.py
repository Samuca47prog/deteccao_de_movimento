# https://en.wikipedia.org/wiki/Kernel_%28image_processing%29

import numpy as np
import cv2
import sys


nome_video = "Ponte.mp4"
VIDEO = "C:/Users/samue/OneDrive/Documentos/Programming/Alura/deteccao_de_movimento/videos/" + nome_video

# Define os tipos de algoritmos
algorithm_types = ['KNN', 'GMG', 'CNT', 'MOG', 'MOG2']
algorithm_type = algorithm_types[1]


def Kernel(KERNEL_TYPE):
    if KERNEL_TYPE == 'dilation':
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    if KERNEL_TYPE == 'opening':
        kernel = np.ones((3,3), np.uint8)
    if KERNEL_TYPE == 'closing':
        kernel = np.ones((3, 3), np.uint8)
    return kernel

# print("Dilation: ")
# print(Kernel('dilation'))

# print("Opening: ")
# print(Kernel('opening'))

# print("Closing: ")
# print(Kernel('closing'))


def Filter(img, filter):
    if filter == 'closing':
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, Kernel('closing'), iterations=2)
    if filter == 'opening':
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, Kernel('opening'), iterations=2)
    if filter == 'dilation':
        return cv2.dilate(img, Kernel('dilation'), iterations=2)
    if filter == 'combine':
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, Kernel('closing'), iterations=2)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, Kernel('opening'), iterations=2)
        dilation = cv2.dilate(opening, Kernel('dilation'), iterations=2)
        return dilation


def Subtractor(algorithm_type):
    if algorithm_type == 'KNN':
        return cv2.createBackgroundSubtractorKNN()
    if algorithm_type == 'GMG':
        return cv2.bgsegm.createBackgroundSubtractorGMG()
    if algorithm_type == 'CNT':
        return cv2.bgsegm.createBackgroundSubtractorCNT()
    if algorithm_type == 'MOG':
        return cv2.bgsegm.createBackgroundSubtractorMOG()
    if algorithm_type == 'MOG2':
        return cv2.createBackgroundSubtractorMOG2()
    print('Erro - Insira uma nova informação')
    sys.exit(1)


##----
w_min = 40  # largura minima do retangulo
h_min = 40  # altura minima do retangulo
offset = 2  # Erro permitido entre pixel
linha_ROI = 620  # Posição da linha de contagem. Quando o centroide do carro passar a linha, conta um carro
carros = 0

'''
Como o centróide é um ponto, resume a informação de todo o retângulo em volta do carro e diminui o tamanho a ser analisado ao passar pela linha de detecção. Isso facilita que o carro não seja contado com duplicidade.
Os retângulos em volta dos carros podem se sobrepor e dificultar a identificação. Ao se utilizar um único ponto, há uma separação melhor de um carro para outro.
'''
def centroide(x, y, w, h):
    """
    :param x: x do objeto
    :param y: y do objeto
    :param w: largura do objeto
    :param h: altura do objeto
    :return: tupla que contém as coordenadas do centro de um objeto
    """
    x1 = w // 2
    y1 = h // 2
    cx = x + x1
    cy = y + y1
    return cx, cy


detec = []
def set_info(detec):
    global carros
    for (x, y) in detec:
        if (linha_ROI + offset) > y > (linha_ROI - offset):
            carros += 1
            cv2.line(frame, (25, linha_ROI), (1200, linha_ROI), (0, 127, 255), 3)
            detec.remove((x, y))
            print("Carros detectados até o momento: " + str(carros))

def show_info(frame, mask):
    text = f'Carros: {carros}'
    cv2.putText(frame, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Video Original", frame)
    # cv2.imshow("Detectar", mask)


cap = cv2.VideoCapture(VIDEO)
background_subtractor = Subtractor(algorithm_type)


while True:

    ok, frame = cap.read() # Pega cada frame do vídeo

    if not ok:
        break

    mask = background_subtractor.apply(frame)
    mask = Filter(mask, 'combine')

    contorno, img = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (25, linha_ROI), (1200, linha_ROI), (255, 127, 0), 3)
    for (i, c) in enumerate(contorno):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contorno = (w >= w_min) and (h >= h_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        centro = centroide(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame, centro, 4, (0, 0, 255), -1)

    set_info(detec)
    show_info(frame, mask)


    if cv2.waitKey(1) == 27: #ESC
        break

cv2.destroyAllWindows()
cap.release()