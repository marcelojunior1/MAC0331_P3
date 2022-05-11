#!/usr/bin/env python


from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.point import *
from geocomp.rn import RN
import time

import math

# ------------------------------------------------------------------------
# Constantes
SEGM = 0
ESQ = 1
RAIO = 2
THETA = 3
X = 1
Y = 2


# ------------------------------------------------------------------------
# Inicio do algoritmo

def Svp(l):
    print()
    fila = para_coordenadas_polares(l)
    mergesort(0, len(fila), fila, X)
    arvore = RN()

    origem = Point(0, 0)

    for i in range(len(fila)):
        print(fila[i])

    for i in range(len(fila)):
        control.sleep()
        segmento = None
        lSeg = fila[i][SEGM]
        fEsq = fila[i][ESQ]
        fTheta = fila[i][THETA]
        fRaio = fila[i][RAIO]

        A = None
        B = None

        print(lSeg, fRaio)

        if fEsq:
            segmento = Segment(origem, l[lSeg].init)
            A, B = arvore.max_min_no(fRaio)
            # arvore.remove_op(fRaio)
        else:
            segmento = Segment(origem, l[lSeg].to)
            arvore.put_op(fRaio, lSeg)
            A, B = arvore.max_min_no(fRaio)

        linha = control.plot_segment(segmento.init.x, segmento.init.y, segmento.to.x, segmento.to.y, "blue", 1)

        if fEsq:
            l[lSeg].hilight("red")
        else:
            l[lSeg].hilight("white")

        control.sleep()

        l[lSeg].hilight("purple")

        if A != -1:
            l[A].hilight("yellow")
        if B != -1:
            l[B].hilight("yellow")

        control.sleep()

        if A != -1:
            l[A].hilight("white")
        if B != -1:
            l[B].hilight("white")

        if fEsq:
            l[lSeg].hilight("red")
        else:
            l[lSeg].hilight("white")

        control.plot_delete(linha)

    arvore.print_tree_op()


# ------------------------------------------------------------------------
# Converte os pontos de uma lista de segmentos para coordenadas polares e os
# organiza em uma lista de pontos.

# TODO: Função alterada para raios iguais; Ponto é sempre a origem

def para_coordenadas_polares(l):
    fila = []
    tam_l = len(l)

    for i in range(tam_l):
        p1 = l[i].init
        p2 = l[i].to
        x1 = p1.x
        x2 = p2.x
        y1 = p1.y
        y2 = p2.y
        r1 = x1**2 + y1**2
        r2 = x2**2 + y2**2
        theta_1 = math.atan(y1 / x1)
        theta_2 = math.atan(y2 / x2)

        raio = r1 if r1 < r2 else r2

        if theta_1 < theta_2 or (theta_1 == theta_2 and r1 < r2):
            fila.append([i, False, raio, theta_1])
            fila.append([i, True, raio, theta_2])
            l[i] = Segment(l[i].to, l[i].init)
        else:
            if theta_1 > theta_2 or (theta_1 == theta_2 and r1 > r2):
                fila.append([i, True, raio, theta_1])
                fila.append([i, False, raio, theta_2])
            else:
                print("Empate!")

    return fila


# -------------------------------------------------------------------
# Ordena a fila pelo valor do angulo (em radianos)

def mergesort(p, r, fila, eixo):
    if p < (r - 1):
        q = math.floor((p + r) / 2)

        mergesort(p, q, fila, eixo)
        mergesort(q, r, fila, eixo)

        intercala(p, q, r, fila, eixo)


def intercala(p, q, r, fila, eixo):
    w = [None for i in range((r - p))]

    for i in range(p, q):
        w[i - p] = fila[i]
    for j in range(q, r):
        w[r - p + q - j - 1] = fila[j]

    i = 0
    j = r - p - 1

    for k in range(p, r):

        cond = (w[i][THETA] <= w[j][THETA])

        if cond:
            fila[k] = w[i]
            i += 1
        else:
            fila[k] = w[j]
            j -= 1
