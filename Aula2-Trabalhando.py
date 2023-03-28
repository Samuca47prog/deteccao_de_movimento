'''
O algoritmo que aprendemos detecta pontos onde tem ou não movimento e preserva aqueles que estão fixos e sem movimentação para criar o fundo do local. 
Por conta disso, é interessante que a câmera esteja fixa e sem movimentação para que o plano de fundo - que é imóvel - permaneça sem movimento.
'''

import numpy as np
import cv2

from time import sleep

nome_video = "Rua.mp4"
VIDEO = "C:/Users/samue/OneDrive/Documentos/Programming/Alura/deteccao_de_movimento/videos/" + nome_video

delay = 10

cap = cv2.VideoCapture(VIDEO)
hasFrame, frame = cap.read()

# captura 72 frames aleatórios (24FPS em 3s)
framesIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=72)

# junta todos os frames em uma lista
frames = []
for fid in framesIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    hasFrame, frame = cap.read()
    frames.append(frame)

# Calcula o frame médio entre todos os capturados
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

# Salva a imagem
cv2.imwrite('imagens\median_frame_aula2' + nome_video + '.jpg', medianFrame)



#---- Aula 2



# Passando a imagem média dos frames para escala de cinza
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Cinza', grayMedianFrame)
# cv2.waitKey(0)
cv2.imwrite('imagens\median_frame__aula2cinza.jpg', medianFrame)


# Converte todo o vídeo para preto e branco
# while (True):
#     hasFrame, frame = cap.read()

#     if not hasFrame:
#         print('Acabou os frames')
#         break

#     frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     cv2.imshow('Frames em Cinza', frameGray)

#     if cv2.waitKey(1) & 0xFF == ord('c'):
#         break

# cap.release()


# aplica a mascara de pixel preto ou branco com OTSU para identificar os carros no vídeo
while (True):
    tempo = float(1/delay)
    sleep(tempo)

    hasFrame, frame = cap.read()

    if not hasFrame:
        print('Acabou os frames')
        break

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    dframe = cv2.absdiff(frameGray, grayMedianFrame)
    th, dframe = cv2.threshold(dframe, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow('Frames em Cinza', dframe)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cap.release()

