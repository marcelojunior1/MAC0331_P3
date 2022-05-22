#!/usr/bin/env python

from geocomp.common.segment import Segment
from geocomp.common.point import *
from geocomp.rn import RN
import math

# ------------------------------------------------------------------------
# Constantes
SEGM = 0
ESQ = 1
RAIO = 2
THETA = 3
X = 1
Y = 2


# TODO: Remover repetição de elementos em seg_visiveis

# ------------------------------------------------------------------------
# Inicio do algoritmo

def Svp(l):
    print()
    # Registra o ponto
    origem = l[0]
    del l[0]
    seg_visiveis = []  # Lista de segmentos visiveis
    arvore = RN()  # Inicia a arvore de segmentos
    # Insere os eventos na fila
    fila, seg_eixo, seg_eixo_info = para_coordenadas_polares(l, origem)
    mergesort(0, len(fila), fila, l)  # Ordena os eventos

    print("Eixo:", seg_eixo)

    # Insere os segmentos do eixo
    for i in range(len(seg_eixo)):
        arvore.put_op(seg_eixo_info[i][0], seg_eixo[i])

    for i in range(len(fila)):
        print(fila[i])

    for i in range(len(l)):
        print(i, l[i])

    for i in range(len(fila)):
        print(fila[i][SEGM], "---------------")

        control.sleep()
        lSeg = fila[i][SEGM]
        fEsq = fila[i][ESQ]
        fRaio = fila[i][RAIO]

        if not fEsq and seg_eixo.count(lSeg) == 0:
            arvore.put_op(fRaio, lSeg)

        # Linha de varredura
        if fEsq:
            segmento = Segment(origem, l[lSeg].init)
        else:
            segmento = Segment(origem, l[lSeg].to)
        linha = control.plot_segment(segmento.init.x, segmento.init.y, segmento.to.x, segmento.to.y, "blue", 1)

        control.sleep()

        if fEsq:
            l[lSeg].hilight("red")
        else:
            l[lSeg].hilight("white")

        control.plot_delete(linha)

        # Define o menor da arvore
        min = arvore.fmin_op()
        k = min[0]
        print("MIN", min)

        if len(min) > 1:
            for i in range(1, len(min)):
                theta_1 = math.atan2(l[k].to.y - origem.y, l[k].to.x - origem.x)
                theta_2 = math.atan2(l[min[i]].to.y - origem.y, l[min[i]].to.x - origem.x)
                if theta_2 > theta_1:
                    k = min[i]

        if k != -1:
            seg_visiveis.append(k)

        # arvore.print_tree_op()
        # print(seg_visiveis)

        if fEsq or seg_eixo.count(lSeg) != 0:
            arvore.remove_op(fRaio, lSeg)

        for i in range(len(seg_visiveis)):
            l[seg_visiveis[i]].hilight("green")


# ------------------------------------------------------------------------
# Converte os pontos de uma lista de segmentos para coordenadas polares e os
# organiza em uma lista de pontos.

def para_coordenadas_polares(l, origem):
    fila = []
    tam_l = len(l)
    seg_eixo = []
    seg_eixo_info = []

    for i in range(tam_l):
        p1 = l[i].init
        p2 = l[i].to
        xc = origem.x
        yc = origem.y
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y

        r1 = (x1 - xc) ** 2 + (y1 - yc) ** 2
        r2 = (x2 - xc) ** 2 + (y2 - yc) ** 2

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

        # Detecta se o segmento intersecta o eixo X
        if abs(theta_1 - theta_2) > math.pi and not (theta_1 == 0 or theta_2 == 0):
            seg_eixo.append(i)
            seg_eixo_info.append([raio])

        # Define se o ponto no eixo X e 0 ou 2PI
        if abs(theta_1 - theta_2) > math.pi and (theta_1 == 0 or theta_2 == 0):
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

    return fila, seg_eixo, seg_eixo_info


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
            seg_1 = w[i][SEGM]
            seg_2 = w[j][SEGM]

            if esq_1 != esq_2:
                if seg_1 == seg_2:
                    if not esq_1:
                        cond = True
                    else:
                        cond = False
                else:
                    if raio_1 > raio_2:
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
