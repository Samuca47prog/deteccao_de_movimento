'''
O algoritmo que aprendemos detecta pontos onde tem ou não movimento e preserva aqueles que estão fixos e sem movimentação para criar o fundo do local. 
Por conta disso, é interessante que a câmera esteja fixa e sem movimentação para que o plano de fundo - que é imóvel - permaneça sem movimento.
'''

import numpy as np
import cv2

nome_video = "Peixes.mp4"
VIDEO = "C:/Users/samue/OneDrive/Documentos/Programming/Alura/deteccao_de_movimento/videos/" + nome_video

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

# Mostra e salva o frame médio obtido
cv2.imshow('Median Frame', medianFrame)
cv2.waitKey(0)
cv2.imwrite('imagens\median_frame_' + nome_video + '.jpg', medianFrame)