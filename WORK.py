import sys
import time
from time import sleep
import cmath
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def motor(xx, yy):
    #MOTOR CAMERA
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(32, GPIO.OUT)
    #MOTOR ARBORE
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
	
	Setarea valorilor PWM folosite de motoare

    DoSteep = xx*-1
    aa = GPIO.PWM(12, 500)
    aa.start(0) 
    ar = GPIO.PWM(32, 500)
    ar.start(0) 
    DoSteep2 = yy*-1
    ba = GPIO.PWM(11, 500)
    ba.start(0) 
    br = GPIO.PWM(13, 500)
    br.start(0)

    if DoSteep2>4:
        GPIO.output(11, 1)
	ba.ChangeDutyCycle(abs(DoSteep2) / 1.2)
        GPIO.output(13, 0)
	br.ChangeDutyCycle(0)
	sleep(0.015)

    if DoSteep>4:
        GPIO.output(12, 1)
	aa.ChangeDutyCycle(abs(DoSteep) / 1.2)

        GPIO.output(32, 0)
	ar.ChangeDutyCycle(0)
	sleep(0.02)

    if DoSteep<-4:
        GPIO.output(12, 0)
	aa.ChangeDutyCycle(0)
        GPIO.output(32, 1)
        ar.ChangeDutyCycle(abs(DoSteep) / 1.2)
	sleep(0.02)
        
    if DoSteep2<-4:
        GPIO.output(11, 0)
	ba.ChangeDutyCycle(0)
        GPIO.output(13, 1)
	br.ChangeDutyCycle(abs(DoSteep2) / 1.2)
	#br.ChangeDutyCycle(50)
	sleep(0.015)

GPIO.cleanup()
