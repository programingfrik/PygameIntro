#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import pygame
import math

pygame.init()
pygame.mixer.init()


# los colores del juego
color_fondo = (0,0,0)
color_paleta = (255, 255, 255)
color_bolita = (255, 255, 255)
color_puntaje = (255, 255, 255)
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
factor_aumento = 1.5

distancia_paleta_I = 50
distancia_paleta_D = 730
limite_superior = 50
limite_inferior = 590

# estados
JUEGO_CORRIENDO = 0
JUEGO_CERRANDO = 1

estado_juego = JUEGO_CORRIENDO

ESTADO_ESPERANDO = 0
ESTADO_LISTO = 1

estado_I = ESTADO_ESPERANDO
estado_D = ESTADO_ESPERANDO
texto_visible = True
ganador_visible = False

en_movimiento_I = False
en_movimiento_D = False

# otras
texto_ganador = ""

puntaje_I = 0
puntaje_D = 0
maximo_puntaje = 5

PUNTAJE_I = 0
PUNTAJE_D = 1
quien_seguido = 0
puntaje_seguido = 3
cont_seguido = 0

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turbo Pong!")

reloj = pygame.time.Clock()
letras_puntaje = pygame.font.SysFont("default", 50)

sonido_A = pygame.mixer.Sound("fist.ogg")
sonido_B = pygame.mixer.Sound("club.ogg")
sonido_toasty = pygame.mixer.Sound("toasty.ogg")
pygame.mixer.music.load("speeditup.ogg")
pygame.mixer.music.play(-1)

pablo_toasty = pygame.image.load("pablo_toasty.png")

inicio_cont = 15
cont = inicio_cont

inicio_toasty = 30
toasty_cont = 0
while (estado_juego == JUEGO_CORRIENDO):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            estado_juego = JUEGO_CERRANDO

    # leyendo el teclado
    estados_teclas = pygame.key.get_pressed()

    en_movimiento_I = False
    if (estados_teclas[pygame.K_LSHIFT] and (posicion_paleta_I > limite_superior)):
        posicion_paleta_I -= 10
        en_movimiento_I = True
        
    if (estados_teclas[pygame.K_LCTRL] and (posicion_paleta_I < (limite_inferior - tamano_paleta[1]))):
        posicion_paleta_I += 10
        en_movimiento_I = True        

    if (estados_teclas[pygame.K_TAB]):
        estado_I = ESTADO_LISTO

    en_movimiento_D = False
    if (estados_teclas[pygame.K_UP] and (posicion_paleta_D > limite_superior)):
        posicion_paleta_D -= 10
        en_movimiento_D = True
        
    if (estados_teclas[pygame.K_DOWN] and (posicion_paleta_D < (limite_inferior - tamano_paleta[1]))):
        posicion_paleta_D += 10
        en_movimiento_D = True

    if estados_teclas[pygame.K_BACKSPACE]:
        estado_D = ESTADO_LISTO

    if estados_teclas[pygame.K_ESCAPE]:
        estado_juego = JUEGO_CERRANDO

    if (estados_teclas[pygame.K_6] and (toasty_cont == 0)):
        sonido_toasty.play()
        toasty_cont = inicio_toasty
        vector_bolita = (int(vector_bolita[0] * 3), vector_bolita[1])
    
    # reaccionando
    if ((estado_I == ESTADO_LISTO) and (estado_D == ESTADO_LISTO)):
        posicion_bolita = (posicion_bolita[0] + vector_bolita[0], posicion_bolita[1] + vector_bolita[1])
    
    if ((posicion_bolita[1] < limite_superior)
        or (posicion_bolita[1] > (limite_inferior - tamano_bolita[1]))):
        vector_bolita = (vector_bolita[0],-vector_bolita[1])
        posicion_bolita = (posicion_bolita[0], posicion_bolita[1] + vector_bolita[1])
        sonido_A.play()
        
    if (((posicion_bolita[0] < (distancia_paleta_I + tamano_paleta[0]))
         and ((posicion_bolita[1] + tamano_bolita[1]) > posicion_paleta_I)
         and (posicion_bolita[1] < (posicion_paleta_I + tamano_paleta[1])))
        or (((posicion_bolita[0] + tamano_bolita[0]) > distancia_paleta_D)
            and ((posicion_bolita[1] + tamano_bolita[1]) > posicion_paleta_D)
            and (posicion_bolita[1] < (posicion_paleta_D + tamano_paleta[1])))):
        if (((posicion_bolita[0] < (distancia_paleta_I + tamano_paleta[0]))
            and (en_movimiento_I))
            or (((posicion_bolita[0] + tamano_bolita[0]) > distancia_paleta_D)
                and (en_movimiento_D))):
            vector_bolita = (int(vector_bolita[0] * factor_aumento), vector_bolita[1])
            
        vector_bolita = (-vector_bolita[0], vector_bolita[1])
        posicion_bolita = (posicion_bolita[0] + vector_bolita[0], posicion_bolita[1])
        sonido_B.play()

    if ((posicion_bolita[0] > distancia_paleta_D) or ((posicion_bolita[0] + tamano_bolita[0]) < distancia_paleta_I)):
        if (posicion_bolita[0] > distancia_paleta_D):
            puntaje_I += 1
            vector_inicial = (math.fabs(vector_inicial[0]), vector_inicial[1])
            if (quien_seguido == PUNTAJE_D):
                quien_seguido = PUNTAJE_I
                cont_seguido = 0
            cont_seguido += 1
        elif ((posicion_bolita[0] + tamano_bolita[0]) < distancia_paleta_I):
            puntaje_D += 1
            vector_inicial = (-math.fabs(vector_inicial[0]), vector_inicial[1])
            if (quien_seguido == PUNTAJE_I):
                quien_seguido = PUNTAJE_D
                cont_seguido = 0
            cont_seguido += 1

        vector_bolita = vector_inicial
        posicion_bolita = posicion_inicial
        posicion_paleta_I = posicion_paleta_inicial
        posicion_paleta_D = posicion_paleta_inicial
        estado_I = ESTADO_ESPERANDO
        estado_D = ESTADO_ESPERANDO
        ganador_visible = False

        if (cont_seguido == puntaje_seguido):
            cont_seguido = 0
            sonido_toasty.play()
            toasty_cont = inicio_toasty
            
        if ((puntaje_I >= maximo_puntaje) or (puntaje_D >= maximo_puntaje)):
            if (puntaje_I >= maximo_puntaje):
                texto_ganador = "<- GANO"
            elif (puntaje_D >= maximo_puntaje):
                texto_ganador = "GANO ->"
                
            ganador_visible = True
            puntaje_I = 0
            puntaje_D = 0
            cont_seguido = 0
            
    # la parte de dibujadera
    pantalla.fill(color_fondo)

    pygame.draw.rect(pantalla, color_limite, pygame.Rect(distancia_paleta_I, (limite_superior - 10), (distancia_paleta_D - distancia_paleta_I + tamano_paleta[0]), 5))

    pygame.draw.rect(pantalla, color_limite, pygame.Rect(distancia_paleta_I, (limite_inferior + 5), (distancia_paleta_D - distancia_paleta_I + tamano_paleta[0]), 5))

    pygame.draw.rect(pantalla, color_paleta, pygame.Rect(distancia_paleta_I, posicion_paleta_I, tamano_paleta[0], tamano_paleta[1]))

    pygame.draw.rect(pantalla, color_paleta, pygame.Rect(distancia_paleta_D, posicion_paleta_D, tamano_paleta[0], tamano_paleta[1]))

    pygame.draw.rect(pantalla, color_bolita, pygame.Rect(posicion_bolita, tamano_bolita))

    img_temp = letras_puntaje.render(str(puntaje_I), False, color_puntaje)
    pantalla.blit(img_temp, (80,5))

    img_temp = letras_puntaje.render(str(puntaje_D), False, color_puntaje)
    pantalla.blit(img_temp, (700,5))

    img_temp = letras_puntaje.render("TURBO PONG", False, color_puntaje)
    pantalla.blit(img_temp, (290,5))

    cont -= 1
    if (cont <= 0):
        cont = inicio_cont
        texto_visible = not texto_visible
    
    if (((estado_I == ESTADO_ESPERANDO) or (estado_D == ESTADO_ESPERANDO)) and (texto_visible)):
        img_temp = letras_puntaje.render("PRESIONA START", False, color_puntaje)
        pantalla.blit(img_temp, (250, 200))
        
        if (ganador_visible):
            img_temp = letras_puntaje.render(texto_ganador, False, color_puntaje)
            pantalla.blit(img_temp, (330, 400))

    if (toasty_cont > 0):
        pantalla.blit(pablo_toasty, (656 + (math.fabs(toasty_cont - (inicio_toasty / 2)) * 10), 300))
        toasty_cont -= 1
    
    pygame.display.flip()
    reloj.tick(30)

pygame.mixer.quit()
pygame.display.quit()
