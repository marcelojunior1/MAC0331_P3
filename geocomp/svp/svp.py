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
    origem = Point(1, 1)
    # Garante a ordem dos pontos em cada segmento
    # filter_segments(l)
    # Insere os eventos na fila
    fila = para_coordenadas_polares(l, origem)
    # Ordena os eventos
    mergesort(0, len(fila), fila, l)
    # Inicia a arvore de segmentos
    arvore = RN()

    pts_visiveis = []

    for i in range(len(fila)):
        print(fila[i])

    for i in range(len(l)):
        print(i, l[i])

    for i in range(len(fila)):
        print(fila[i][SEGM], "---------------")

        control.sleep()
        segmento = None
        lSeg = fila[i][SEGM]
        fEsq = fila[i][ESQ]
        fTheta = fila[i][THETA]
        fRaio = fila[i][RAIO]
        A = None
        B = None

        if fEsq:
            segmento = Segment(origem, l[lSeg].init)
            arvore.remove_op(fRaio, lSeg)
        else:
            segmento = Segment(origem, l[lSeg].to)
            arvore.put_op(fRaio, lSeg)

        linha = control.plot_segment(segmento.init.x, segmento.init.y, segmento.to.x, segmento.to.y, "blue", 1)

        if fEsq:
            l[lSeg].hilight("red")
        else:
            l[lSeg].hilight("white")

        control.sleep()

        if fEsq:
            l[lSeg].hilight("red")
        else:
            l[lSeg].hilight("white")

        control.plot_delete(linha)

        if not (i > len(fila)-2 and not fEsq):
            min = arvore.fmin_op()

            for i in range(1):
                k = min[i]
                if k != -1:
                    pts_visiveis.append(k)

        #arvore.print_tree_op()

        # print("----------------------------")

        for i in range(len(pts_visiveis)):
            l[pts_visiveis[i]].hilight("green")


# ------------------------------------------------------------------------
# Converte os pontos de uma lista de segmentos para coordenadas polares e os
# organiza em uma lista de pontos.

def para_coordenadas_polares(l, origem):
    fila = []
    tam_l = len(l)

    for i in range(tam_l):
        p1 = l[i].init
        p2 = l[i].to
        x1 = p1.x
        x2 = p2.x
        xc = origem.x
        yc = origem.y
        y1 = p1.y
        y2 = p2.y
        r1 = (x1) ** 2 + (y1) ** 2
        r2 = (x2) ** 2 + (y2) ** 2

        xt1 = abs(x1 - xc)
        yt1 = abs(y1 - yc)
        xt2 = abs(x2 - xc)
        yt2 = abs(y2 - yc)

        if x1 < xc:
            xt1 *= -1
        if y1 < yc:
            yt1 *= -1
        if x2 < xc:
            xt2 *= -1
        if y2 < yc:
            yt2 *= -1

        theta_1 = math.atan2(yt1, xt1)
        theta_2 = math.atan2(yt2, xt2)

        if theta_1 < 0:
            theta_1 = math.pi + theta_1 + math.pi
        if theta_2 < 0:
            theta_2 = math.pi + theta_2 + math.pi

        raio = r1 if r1 < r2 else r2

        if abs(theta_1 - theta_2) > math.pi:
            if theta_1 <= math.pi:
                theta_1 += 2 * math.pi
            else:
                theta_2 += 2 * math.pi

        if theta_1 < theta_2 or (theta_1 == theta_2 and r1 < r2):
            fila.append([i, False, raio, theta_1])
            fila.append([i, True, raio, theta_2])
            l[i] = Segment(l[i].to, l[i].init)
        else:
            if theta_1 > theta_2 or (theta_1 == theta_2 and r1 > r2):
                fila.append([i, True, raio, theta_1])
                fila.append([i, False, raio, theta_2])
            else:
                fila.append([i, False, raio, theta_1])
                fila.append([i, True, raio, theta_2])
                l[i] = Segment(l[i].to, l[i].init)

    return fila


# -------------------------------------------------------------------
# Garante que o ponto de 'inicio' de um segmento é menor em X do que
# o ponto 'final'.

def filter_segments(l):
    for i in range(len(l)):
        if (l[i].init.x > l[i].to.x):
            l[i].init, l[i].to = l[i].to, l[i].init
        elif (l[i].init.x == l[i].to.x):
            if (l[i].init.y > l[i].to.y):
                l[i].init, l[i].to = l[i].to, l[i].init


# -------------------------------------------------------------------
# Ordena a fila pelo valor do angulo (em radianos)

def mergesort(p, r, fila, l):
    if p < (r - 1):
        q = math.floor((p + r) / 2)

        mergesort(p, q, fila, l)
        mergesort(q, r, fila, l)
        intercala(p, q, r, fila, l)


def intercala(p, q, r, fila, l):
    w = [None for i in range((r - p))]

    for i in range(p, q):
        w[i - p] = fila[i]
    for j in range(q, r):
        w[r - p + q - j - 1] = fila[j]

    i = 0
    j = r - p - 1

    for k in range(p, r):

        theta_1 = w[i][THETA]
        theta_2 = w[j][THETA]

        cond = (theta_1 < theta_2)

        if theta_1 == theta_2:
            esq_1 = w[i][ESQ]
            esq_2 = w[j][ESQ]
            raio_1 = w[i][RAIO]
            raio_2 = w[j][RAIO]

            if esq_1 != esq_2:
                if not esq_1:
                    cond = True
                else:
                    cond = False
            else:
                if esq_1 and esq_2:
                    if raio_1 > raio_2:
                        cond = True
                    else:
                        cond = False

                if not esq_1 and not esq_2:
                    if raio_1 < raio_2:
                        cond = True
                    else:
                        cond = False

        if cond:
            fila[k] = w[i]
            i += 1
        else:
            fila[k] = w[j]
            j -= 1
