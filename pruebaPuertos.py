#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print "Error importando RPi.GPIO! Probablemente se deba a falta de permisos!"
    sys.exit(1)

cont = 0
rep = 5
try:
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setwarnings(False)

    for c in range(26):
        GPIO.setup(entrada, GPIO.OUT, GPIO.LOW)

        print ("probando %i ...\n" % (c))

        cont = 0
        while cont < rep:
            GPIO.output(c, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(c, GPIO.HIGH)
            time.sleep(0.2)
            cont += 1
finally:
    GPIO.cleanup()


