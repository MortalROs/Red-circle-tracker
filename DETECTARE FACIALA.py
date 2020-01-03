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
i = 0

#LOCATIA FISIERULUI DE UNDE SE PREIA MODELUL DE RECUNOSTERE AL FETEI
font = cv2.FONT_HERSHEY_SIMPLEX
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture("http://localhost:5000/")
cap.set(3,640) # LATIMEA IMAGINI
cap.set(4,480) # LUNGIMEA IMAGINI

if __name__ == '__main__':
    import sys, getopt

    while True:
        ret, frame = cap.read()

        #APLICAREA UNUI FILTRU ALB-NEGRU
        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #APLICAREA FILTRULUI PENTRU DETECTAREA FETELOR
        fete = faceCascade.detectMultiScale(
            gri,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )

        #PENTRU FIECARE FATA DETECTAT SE VA DESENA UN DREPTUNGHI ALBASTRU IN JURUL EI
        for (x,y,w,h) in fete:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
            X = int(x+(w/2))
            Y = int(y+(h/2))
            fata_gru = gri[y:y+h, x:x+w]
            fata_color = frame[y:y+h, x:x+w]
            print(X,Y)
            
            #TRIMITEREA CORDONATELOR FETEI CATRE SERVAR
            if count == 5:
                count = 0
                message = str(str(X) + " " + str(Y))
                message = message.encode()
                con.sendall(message)
            count += 1

        #AFISAREA IMAGINI PROCESATE
        cv2.imshow('Detectare fete',frame)

        #ASTEPTAREA UNU BUTON PENTRU OPRIREA PROCESULUI
        k = cv2.waitKey(30) & 0xff
        if k == 27: 
            break
            
    #ELIBERAREA MEMORIEI FOLOSITE DE PROGRAM DUPA TERMINAREA PROCESULUI        
    cam.release()
    con.close()

cap.release()
cv2.destroyAllWindows()
