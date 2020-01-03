#IMPORTAREA LIBRARIILOR NECESARE
import numpy as np
import cv2
import socket
import sys
import os
import string

# CREAZA UN SOCKET TCP/IP
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# CONECTAREA LA SOCKET-UL CU ADRESA SI PORTUL SERVARULUI
host = 'localhost'
port = 5001

con.connect((host, port))

myCord = {}
count = 0

imgcap = cv2.VideoCapture("http://localhost:5000")
imgcap.set(3,320) # LATIMEA IMAGINI
imgcap.set(4,240) # LUNGIMEA IMAGINI

count = 0

if imgcap.isOpened():

    while(True):
        ret, frame = imgcap.read()
        
        #FILTRU BLUR GAUSSIAN
        color_blur = cv2.GaussianBlur(frame, (3, 3), 0)
        
        #CONVERTIREA CULORILOR DIN BGR LA HSV
        hsc_color = cv2.cvtColor(color_blur, cv2.COLOR_BGR2HSV)
        
        #INTERVALU DE CULORI CAUTAT
        lowcolor= np.array([140, 84, 141])
        highercolor = np.array([186, 255, 255])
        
        #OBTINEREA CULORILOR DIN INTERVAL
        color_range = cv2.inRange(hsc_color, lowcolor, highercolor)
        rs_color = cv2.bitwise_and(color_blur,color_blur, mask=color_range )
        color_gray = cv2.cvtColor(rs_color, cv2.COLOR_BGR2GRAY)
        
        #FILTRU PENTRU DETECTAREA MARGINILOR
        edge_filter = cv2.Canny(color_gray, 100, 500)
        color_gray = cv2.GaussianBlur(color_gray, (5, 5), 0)
        edge_filter = cv2.GaussianBlur(edge_filter, (5, 5), 0)
        
        #FILTRU DE DETECTAREA FORMELOR CIRCULARE
        rows = edge_filter.shape[0]
        rows = int(rows / 8)
        cercuri = cv2.HoughCircles(color_gray, cv2.HOUGH_GRADIENT, 1, rows, param1=10, param2=20, minRadius=10, maxRadius=50)
        cir_cen = []
        
        #VERIFICAREA IMAGINI DACA CONTINE UN CERC COLORAT
        if cercuri is not None:
            cercuri = np.uint16(np.around(cercuri))
            for i in cercuri[0,:]:
                center = (i[0], i[1])
                
                #DESENAREA UNUI CERC CU ACEEASI RAZA CA CERCUT DETECTAT
                cv2.circle(frame,center,i[2],(0, 0, 255),1)

                #TRIMITEREA CORDONATELOR CERCULUI CATRE SERVAR
                if count == 5:
                    count = 0
                    message = str(str(center[0]) + " " + str(center[1]))
                    message = message.encode()
                    con.sendall(message)
                    print(center)
                count += 1

                radius = i[2]
        
        #AFISAREA IMAGINI PROCESATE
        cv2.imshow('Detectare Cerc', frame)
        cv2.imshow('Filtru de Culoare', color_gray)
        cv2.imshow('Filtru de Margini', edge_filter)
        
        #ASTEPTAREA UNU BUTON PENTRU OPRIREA PROCESULUI
        tasta = cv2.waitKey(5) & 0xFF
        if tasta == 27:
            break
    
    #ELIBERAREA MEMORIEI FOLOSITE DE PROGRAM DUPA TERMINAREA PROCESULUI
    cam.release()
    con.close()
    cv2.destroyAllWindows()
else:
   print('Fara imagine')
