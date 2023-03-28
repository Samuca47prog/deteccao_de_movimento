import cv2
import sys

nome_video = "Ponte.mp4"
VIDEO = "C:/Users/samue/OneDrive/Documentos/Programming/Alura/deteccao_de_movimento/videos/" + nome_video

# Define os tipos de algoritmos
algorithm_types = ['KNN', 'GMG', 'CNT', 'MOG', 'MOG2']
algorithm_type = algorithm_types[0]


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
# background_subtractor = Subtractor(algorithm_type)
background_subtractor = []
for i, a in enumerate(algorithm_types): #gera um ID para cada um dos algoritmos
    print(i, a)
    background_subtractor.append(Subtractor(a))


# e1 = cv2.getTickCount()

# Aplica o algoritmo escolhido no video
def main():
    while (cap.isOpened):
        ok, frame = cap.read()

        if not ok:
            print('Frames acabaram!')
            break

        frame = cv2.resize(frame, (0, 0), fx=0.35, fy=0.35)

        # mask = background_subtractor.apply(frame)
        # cv2.imshow('Frame', frame)
        # cv2.imshow('Mask', mask)


        knn = background_subtractor[0].apply(frame)
        gmg = background_subtractor[1].apply(frame)
        cnt = background_subtractor[2].apply(frame)
        mog = background_subtractor[3].apply(frame)
        mog2 = background_subtractor[4].apply(frame)

        cv2.imshow('Original', frame)
        cv2.imshow('KNN', knn)
        cv2.imshow('GMG', gmg)
        cv2.imshow('CNT', cnt)
        cv2.imshow('MOG', mog)
        cv2.imshow('MOG2', mog2)


        if cv2.waitKey(1) & 0xFF == ord("c"):
            break

        
        # e2 = cv2.getTickCount()

        # t = (e2 -e1) / cv2.getTickFrequency()
        # print(t)

main()



## KNN - 28.9843742
## GMG - 
## CNT - 
## MOG - 
## MOG 2 - 