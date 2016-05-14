#Wrapper code for interfacing with GPIO
#Author: Mehmet Akbulut
#MIT License

import RPi.GPIO as GPIO

#RPi numbering for GPIO. Alternative: GPIO.BCM for CPU numbering
GPIO.setmode(GPIO.BOARD)
freq=100
pwm = {}

def setpin(pin,mode):
    '''Sets pin to INPUT or OUTPUT mode'''
    if mode=="INPUT":
        GPIO.setup(pin, GPIO.IN)
        return 0
    elif mode=="OUTPUT":
        GPIO.setup(pin, GPIO.OUT)
        return 1
    else:
        return -1

def setPWM(pin):
    '''Create PWM object to control pin outputs'''
    pwm[pin]=GPIO.PWM(pin,freq)
    pwm[pin].start(0)

def read(pin):
    '''Returns the pin value'''
    return GPIO.input(pin)

def write(pin,value):
    '''Writes to the pin'''
    if value==1:
        return GPIO.output(pin,GPIO.HIGH)
    else:
        return GPIO.output(pin,GPIO.LOW)

def writePWM(pin,percentage):
    '''Control PWM pin outputs'''
    if percentage >= 0 and percentage <= 1:
        #print("pwm at "+str(percentage*100))
        pwm[pin].ChangeDutyCycle(percentage*100)
    else:
        #print("pwm off")
        pass
