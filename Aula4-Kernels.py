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


cap = cv2.VideoCapture(VIDEO)
background_subtractor = Subtractor(algorithm_type)


# Aplica o algoritmo escolhido no video
def main():
    while (cap.isOpened):
        ok, frame = cap.read()

        if not ok:
            print('Frames acabaram!')
            break

        frame = cv2.resize(frame, (0, 0), fx=0.35, fy=0.35)

        mask = background_subtractor.apply(frame)
        mask_Filter = Filter(mask, 'combine')

        # mostra os pixels da imagem original que possuem pixel branco na máscara
        cars_after_mask = cv2.bitwise_and(frame, frame, mask=mask_Filter)

        # cv2.imshow('Frame', frame)
        # cv2.imshow('Mask', mask)
        # cv2.imshow('Mask with Filter', mask_Filter)
        # cv2.imshow('Cars', cars_after_mask)



        mask_Filter_dilation = Filter(mask, 'dilation')
        mask_Filter_closing = Filter(mask, 'closing')
        mask_Filter_opening = Filter(mask, 'opening')
        mask_Filter_combine = Filter(mask, 'combine')

        cv2.imshow('Original', frame)
        cv2.imshow('Dilation', mask_Filter_dilation)
        cv2.imshow('Closing', mask_Filter_closing)
        cv2.imshow('Opening', mask_Filter_opening)
        cv2.imshow('Combine', mask_Filter_combine)



        if cv2.waitKey(1) & 0xFF == ord("c"):
            break

main()