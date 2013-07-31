#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Esta es la organización de un 7-segmentos.
#
#   3 0   1 2
#   | | | | |
#   ---------
#   |  ---1 |
#   | |0  |2|
#   | |   | |
#   |  ---3 |
#   | |4  | |
#   | | 5 |6|
#   |  ---o7|
#   ---------
#   | | | | |
#   4 5 G 6 7
#


import sys
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print "Error importando RPi.GPIO! Probablemente se deba a falta de permisos!"
    sys.exit(1)


def ponerDigito(disp, digito):
    cont = 0
    while (cont < 8):
        GPIO.output(disp[cont], numeros[digito][cont])
        cont += 1

def ponerValor(valor, base, disps):
    cont = 0
    digito = 0
    while (valor > 0) and (cont < len(disps)):
        digito = valor % base
        valor = valor / base
        ponerDigito(disps[cont], digito)
        cont += 1

numeros = {0: [1, 1, 1, 0, 1, 1, 1, 0]\
           ,1 : [0, 0, 1, 0, 0, 0, 1, 0]\
           ,2 : [0, 1, 1, 1, 1, 1, 0, 0]\
           ,3 : [0, 1, 1, 1, 0, 1, 1, 0]\
           ,4 : [1, 0, 1, 1, 0, 0, 1, 0]\
           ,5 : [1, 1, 0, 1, 0, 1, 1, 0]\
           ,6 : [1, 1, 0, 1, 1, 1, 1, 0]\
           ,7 : [0, 1, 1, 0, 0, 0, 1, 0]\
           ,8 : [1, 1, 1, 1, 1, 1, 1, 0]\
           ,9 : [1, 1, 1, 1, 0, 1, 1, 0]\
           ,10 : [1, 1, 1, 1, 1, 0, 1, 0]\
           ,11 : [1, 0, 0, 1, 1, 1, 1, 0]\
           ,12 : [1, 1, 0, 1, 1, 1, 0, 0]\
           ,13 : [0, 0, 1, 1, 1, 1, 1, 0]\
           ,14 : [1, 1, 0, 1, 1, 1, 0, 0]\
           ,15 : [1, 1, 1, 1, 1, 0, 0, 0]}

disp = [[2, 3, 4, 14, 15, 17, 18, 27]\
        ,[22, 23, 24, 10, 9, 25, 11, 8]]

valor = 0

base = 10

entrada = 7

estado = 0
estadoa = 0

try:
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)
    
    GPIO.setup(entrada, GPIO.IN)
    
    for d in disp:
        for c in d:
            GPIO.setup(c, GPIO.OUT, 0)
    
    while True:
        estadoa = estado
        estado = GPIO.input(entrada)

        # tratando de detectar un flanco comparando el estado anterior
        # de la entrada con el estado actual.
#        if (estadoa == 1) and (estado == 0):
#            valor += 1

        ponerValor(valor, base, disp)
        valor += 1
        time.sleep(0.5)

finally:
    GPIO.cleanup()


