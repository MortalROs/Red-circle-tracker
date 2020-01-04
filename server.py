#IMPORTAREA LIBRARIILOR NECESARE
import socket
import sys
import os
import time
import random
import PID
import work

#SETAREA VARIABILELOR NECESARE PID
targetX = 120
targetY = 160
Px = 0.5
Ix = 0.2
Dx = 0.05
Py = 0.3
Iy = 0.1
Dy = 0.03
#INITIALIZAREA PID-ULUI
pidX = PID.PID(Px, Ix, Dx)
pidX.SetPoint = targetX
pidX.setSampleTime(1)
pidY = PID.PID(Py, Iy, Dy)
pidY.SetPoint = targetY
pidY.setSampleTime(1)

#CREAREA UNUI SOCKET TCP/IP
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#SETAREA SI PORNIREA SERVARULUI
host = '0.0.0.0'
port = 5001
#print('starting up on ', server_address)
con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
con.bind((host, port))


#ASTEPRAREA UNUI SOCKET DISPONIBIL
con.listen(1)

while True:
    #ASTEPTAREA UNEI CONEXIUNI DE LA CLIENT
    print('Astept o conexiune')
    print("")
    connection, client_address = con.accept()
    try:
        print(str(client_address[0]) + " conectat!")
        print("Astept date de la client!")
        print()
       #PRIMIREA DATELOR TRIMISE DE CLIENT
        while True:
            date = connection.recv(255)
            date = date.decode()
            if date:
                dat = str.split(str(date))
                cordX = int(dat[0])
                cordY = int(dat[1])

		#REINITIALIZAREA VALORILOR PENTRU PID
                pidX.update(cordX)
                pidY.update(cordY)

                targetX = pidX.output
                targetX = max(min( int(targetX), 100 ), -100)
                targetY = pidY.output
                targetY = max(min( int(targetY), 100 ), -100)

       #AFISAREA CORDONATELOR PRIMITE
                print("X= " + str(targetX))
                print("y= " + str(targetY))
                print("------------------")

	   #ACTIONAREA MOTOARELOR
                work.motor(targetY, targetX)
            else:
                break
    finally:
        #INCHIDEREA CONEXIUNI CU CLIENTUL
        connection.close()
