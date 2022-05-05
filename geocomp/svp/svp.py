#!/usr/bin/env python


from geocomp.common.segment import Segment
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.point import *
from geocomp.rn import RN

import math

SEGM = 0
ESQ = 1
RAIO = 2
THETA = 3
X = 1
Y = 0

# ------------------------------------------------------------------------
# Inicio do algoritmo
def Svp(l):
    print()
    filter_segments(l)
    fila = para_coordenadas_polares(l)
    mergesort(0, len(fila), fila, X)

    origem = Point(0, 0)

    for i in range(len(fila)):
        print(fila[i])

# ------------------------------------------------------------------------
#

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
        r_1 = (x2 - y1) ** 2
        r_2 = (x2 - y2) ** 2
        theta_1 = math.atan(y1 / x1)
        theta_2 = math.atan(y2 / x2)
        fila.append([i, True, r_1, theta_1])
        fila.append([i, False, r_2, theta_2])
    return fila


# ------------------------------------------------------------------------
# Ajusta o segmento de forma que o  primeiro ponto
# seja o de menor coordenada

def filter_segments(l):
    for i in range(len(l)):
        if (l[i].init.x > l[i].to.x):
            l[i].init, l[i].to = l[i].to, l[i].init
        elif (l[i].init.x == l[i].to.x):
            if (l[i].init.y > l[i].to.y):
                l[i].init, l[i].to = l[i].to, l[i].init


# -------------------------------------------------------------------
# Ordena a fila pela coordenada X

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
        cond = False

        # Organizacao por X
        if eixo == X:
            p1 = fila[i]
            p2 = fila[j]

            cond = (p1[THETA] <= p2[THETA])

            if p1[ESQ] == p2[ESQ]:
                if not p1[ESQ]:
                    cond = True
                else:
                    cond = False
        else:
            print("Implementar se necessario")

        if cond:
            fila[k] = w[i]
            i += 1
        else:
            fila[k] = w[j]
            j -= 1
