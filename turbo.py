#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import pygame
import math

pygame.init()


# los colores del juego
color_fondo = (0,0,0)
color_paleta = (255, 255, 255)
color_bolita = (255, 255, 255)
color_limite = (255, 255, 255)

# tamanos coordenadas
tamano_paleta = (20, 120)
tamano_bolita = (20, 20)

posicion_paleta_inicial = 240
posicion_paleta_I = posicion_paleta_inicial
posicion_paleta_D = posicion_paleta_inicial

posicion_inicial = (400,300)
posicion_bolita = posicion_inicial

vector_inicial = (10,10)
vector_bolita = vector_inicial

distancia_paleta_I = 50
distancia_paleta_D = 730
limite_superior = 50
limite_inferior = 590

# estados
JUEGO_CORRIENDO = 0
JUEGO_CERRANDO = 1

estado_juego = JUEGO_CORRIENDO

# otras

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turbo Pong!")

reloj = pygame.time.Clock()

while (estado_juego == JUEGO_CORRIENDO):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            estado_juego = JUEGO_CERRANDO

    # leyendo el teclado
    estados_teclas = pygame.key.get_pressed()

    if (estados_teclas[pygame.K_LSHIFT] and (posicion_paleta_I > limite_superior)):
        posicion_paleta_I -= 10
        
    if (estados_teclas[pygame.K_LCTRL] and (posicion_paleta_I < (limite_inferior - tamano_paleta[1]))):
        posicion_paleta_I += 10

    if (estados_teclas[pygame.K_UP] and (posicion_paleta_D > limite_superior)):
        posicion_paleta_D -= 10
        
    if (estados_teclas[pygame.K_DOWN] and (posicion_paleta_D < (limite_inferior - tamano_paleta[1]))):
        posicion_paleta_D += 10

    if estados_teclas[pygame.K_ESCAPE]:
        estado_juego = JUEGO_CERRANDO
    
    # reaccionando
    posicion_bolita = (posicion_bolita[0] + vector_bolita[0], posicion_bolita[1] + vector_bolita[1])
    
    if ((posicion_bolita[1] < limite_superior)
        or (posicion_bolita[1] > (limite_inferior - tamano_bolita[1]))):
        vector_bolita = (vector_bolita[0],-vector_bolita[1])
        posicion_bolita = (posicion_bolita[0], posicion_bolita[1] + vector_bolita[1])
        
    if (((posicion_bolita[0] < (distancia_paleta_I + tamano_paleta[0]))
         and ((posicion_bolita[1] + tamano_bolita[1]) > posicion_paleta_I)
         and (posicion_bolita[1] < (posicion_paleta_I + tamano_paleta[1])))
        or (((posicion_bolita[0] + tamano_bolita[0]) > distancia_paleta_D)
            and ((posicion_bolita[1] + tamano_bolita[1]) > posicion_paleta_D)
            and (posicion_bolita[1] < (posicion_paleta_D + tamano_paleta[1])))):           
        vector_bolita = (-vector_bolita[0], vector_bolita[1])
        posicion_bolita = (posicion_bolita[0] + vector_bolita[0], posicion_bolita[1])

    if ((posicion_bolita[0] > distancia_paleta_D) or ((posicion_bolita[0] + tamano_bolita[0]) < distancia_paleta_I)):
        posicion_bolita = posicion_inicial
        posicion_paleta_I = posicion_paleta_inicial
        posicion_paleta_D = posicion_paleta_inicial
    
    # la parte de dibujadera
    pantalla.fill(color_fondo)

    pygame.draw.rect(pantalla, color_limite, pygame.Rect(distancia_paleta_I, (limite_superior - 10), (distancia_paleta_D - distancia_paleta_I + tamano_paleta[0]), 5))

    pygame.draw.rect(pantalla, color_limite, pygame.Rect(distancia_paleta_I, (limite_inferior + 5), (distancia_paleta_D - distancia_paleta_I + tamano_paleta[0]), 5))

    pygame.draw.rect(pantalla, color_paleta, pygame.Rect(distancia_paleta_I, posicion_paleta_I, tamano_paleta[0], tamano_paleta[1]))

    pygame.draw.rect(pantalla, color_paleta, pygame.Rect(distancia_paleta_D, posicion_paleta_D, tamano_paleta[0], tamano_paleta[1]))

    pygame.draw.rect(pantalla, color_bolita, pygame.Rect(posicion_bolita, tamano_bolita))
        
    pygame.display.flip()
    reloj.tick(30)

pygame.display.quit()
