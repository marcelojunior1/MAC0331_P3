#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from random import randint
import random

PRETO = 0
VERMELHO = 1

CONTROLE = False
IMPRIMIR = 0


class RN:
    def __init__(self):
        self.raiz = None

    class No:

        def __init__(self, chave, cor, item):
            self.item = item
            self.chave = chave
            self.cor = cor
            self.esq = None
            self.dir = None
            self.pai = None
            self.N = 0

    # Rotinas auxiliares ------------------------------------------------------------------------

    def size(self, x: No):
        if x == None:
            return 0
        else:
            return x.N

    def eFolha(self, no: No):
        return no.esq is None and no.dir is None

    def filhosPretos(self, no: No):
        if no is None:
            return True

        if (no.esq is None) and (no.dir is None):
            return True

        if (no.esq is not None) and (no.dir is not None):
            return (no.esq.cor is PRETO) and (no.dir.cor is PRETO)

        if no.esq is not None:
            return no.esq.cor is PRETO

        return no.dir.cor is PRETO

    def filhosVermelhos(self, no: No):
        if (no.esq is not None) and (no.dir is not None):
            return (no.esq.cor is VERMELHO) and (no.dir.cor is VERMELHO)
        return False

    def get(self, raizArv: No, chave):
        if raizArv is None:
            return None

        i = chave - raizArv.chave

        if i < 0:
            return self.get(raizArv.esq, chave)
        else:
            if i > 0:
                return self.get(raizArv.dir, chave)
            else:
                return raizArv

    def fmax(self, no: No):
        if no.dir is None:
            return no
        else:
            return self.fmax(no.dir)

    def fmin_op(self):

        if self.raiz is None:
            return -1

        no = self.fmin(self.raiz)

        if no is None:
            return -1
        else:
            return no.item

    def fmin(self, no: No):
        if no.esq is None:
            return no
        return self.fmin(no.esq)

    def max_min_no(self, chave):
        predecessor = -1
        sucessor = -1

        no = self.get(self.raiz, chave)

        if no is None:
            print("Erro ao encontrar a chave! : ", chave)
            return predecessor, sucessor

        if no == self.raiz:
            A = None
            B = None
            if no.esq is not None:
                A = self.fmax(no.esq)
            if no.dir is not None:
                B = self.fmin(no.dir)
            if A is not None:
                predecessor = A.item
                # predecessor = A.chave
            if B is not None:
                sucessor = B.item
                #sucessor = B.chave

            return sucessor, predecessor

        # Encontra o sucessor
        if no.dir is not None:
            tmp = self.fmin(no.dir)
            sucessor = tmp.item
        else:
            pai = no.pai
            filho = no
            while pai is not None and (filho == pai.dir):
                filho = pai

                if pai.pai is not None:
                    pai = pai.pai
                else:
                    break
            sucessor = pai.item

        # Encontra o predecessor
        if no.esq is not None:
            tmp = self.fmax(no.esq)
            predecessor = tmp.item
        else:
            pai = no.pai
            filho = no
            while pai is not None and (filho == pai.esq):
                filho = pai
                if pai.pai is not None:
                    pai = pai.pai
                else:
                    break
            predecessor = pai.item

        return sucessor, predecessor

    # Insercao ---------------------------------------------------------------------------------

    def put_op(self, chave, item):
        self.raiz = self.put(self.raiz, chave, item)

    def put(self, raiz_arv, chave, item):
        # TESTE
        global IMPRIMIR

        if raiz_arv is None:
            raiz_arv = self.No(chave, PRETO, item)
            raiz_arv.N = 1
            raiz_arv.pai = None
            return raiz_arv

        p = raiz_arv
        achou = False
        direito = False

        # Procura onde o no sera inserido
        while not achou:
            if (chave < p.chave) and (p.esq is not None):
                p = p.esq
            else:
                if (chave < p.chave) and (p.esq is None):
                    achou = True
                else:
                    if (chave > p.chave) and (p.dir is not None):
                        p = p.dir
                    else:
                        if (chave > p.chave) and (p.dir is None):
                            direito = True
                            achou = True
                        else:
                            if chave == p.chave:
                                p.item = item
                                return raiz_arv

        # Insere o no
        novo = RN.No(chave, VERMELHO, item)
        novo.pai = p
        if direito:
            p.dir = novo
        else:
            p.esq = novo

        filho = novo

        while p is not None:

            if p.cor == PRETO:

                if p.esq is not None:
                    p.esq.N = 1 + self.size(p.esq.esq) + self.size(p.esq.dir)
                if p.dir is not None:
                    p.dir.N = 1 + self.size(p.dir.esq) + self.size(p.dir.dir)
                p.N = 1 + self.size(p.esq) + self.size(p.dir)
                break

            avo = p.pai

            if avo is None:
                if p.esq is not None:
                    p.esq.N = 1 + self.size(p.esq.esq) + self.size(p.esq.dir)
                if p.dir is not None:
                    p.dir.N = 1 + self.size(p.dir.esq) + self.size(p.dir.dir)
                p.N = 1 + self.size(p.esq) + self.size(p.dir)

                p.cor = PRETO
                break

            tio = None

            if (avo.esq is not None) and (avo.esq is not p):
                tio = avo.esq
            else:
                if (avo.dir is not None) and (avo.dir is not p):
                    tio = avo.dir

            if (tio is not None) and (tio.cor is VERMELHO):
                avo.cor = VERMELHO
                p.cor = PRETO
                tio.cor = PRETO

                if avo.pai is None:
                    avo.cor = PRETO
                    return avo

                if p.esq is not None:
                    p.esq.N = 1 + self.size(p.esq.esq) + self.size(p.esq.dir)
                if p.dir is not None:
                    p.dir.N = 1 + self.size(p.dir.esq) + self.size(p.dir.dir)
                p.N = 1 + self.size(p.esq) + self.size(p.dir)

                p = avo.pai
                filho = avo
            else:
                # Casos

                if (p is avo.esq) and (filho is p.dir):

                    # Rodar para a esquerda
                    p.dir = filho.esq
                    if filho.esq is not None:
                        filho.esq.pai = p
                    filho.esq = p
                    p.pai = filho
                    filho.pai = avo
                    avo.esq = filho

                    p = filho
                    filho = filho.esq

                    continue
                else:
                    if (p is avo.esq) and (filho is p.esq):

                        # Roda para direita
                        avo.esq = p.dir
                        if p.dir is not None:
                            p.dir.pai = avo
                        p.dir = avo
                        p.pai = avo.pai

                        if avo.pai is not None:
                            if avo.pai.dir is avo:
                                avo.pai.dir = p
                            else:
                                avo.pai.esq = p

                        avo.pai = p
                        p.cor = PRETO
                        avo.cor = VERMELHO

                        if avo is raiz_arv:
                            raiz_arv = p

                        continue
                    else:
                        if (p is avo.dir) and (filho is p.dir):
                            # Roda para esquerda
                            avo.dir = p.esq
                            if p.esq is not None:
                                p.esq.pai = avo
                            p.esq = avo
                            p.pai = avo.pai

                            if avo.pai is not None:
                                if avo.pai.esq is avo:
                                    avo.pai.esq = p
                                else:
                                    avo.pai.dir = p

                            avo.pai = p

                            p.cor = PRETO
                            avo.cor = VERMELHO

                            if avo is raiz_arv:
                                raiz_arv = p

                            continue
                        else:
                            if (p is avo.dir) and (filho is p.esq):
                                # Rodar para a direita
                                p.esq = filho.dir
                                if filho.dir is not None:
                                    filho.dir.pai = p
                                filho.dir = p
                                p.pai = filho
                                filho.pai = avo
                                avo.dir = filho

                                p = filho
                                filho = filho.dir

                                continue

                if p.esq is not None:
                    p.esq.N = 1 + self.size(p.esq.esq) + self.size(p.esq.dir)
                if p.dir is not None:
                    p.dir.N = 1 + self.size(p.dir.esq) + self.size(p.dir.dir)
                p.N = 1 + self.size(p.esq) + self.size(p.dir)

                filho = p
                p = p.pai

        return raiz_arv

    # Remocao ----------------------------------------------------------------------------------
    
    def remove_op(self, chave):
        # TESTE
        global CONTROLE
        if chave == 50:
            CONTROLE = True

        self.raiz = self.remove(self.raiz, chave)

    def checar(self, no: No):
        while no is not self.raiz:

            # Definindo variaveis
            filhoDir = (no.pai.dir is no)
            pai = no.pai
            irmao = None
            if filhoDir:
                irmao = no.pai.esq
            else:
                irmao = no.pai.dir
            avo = pai.pai

            # TESTE
            if irmao is None:
                print("Erro - Irmao null")
                exit(1)

            # Irmao preto com filhos pretos ou nulos
            if (irmao.cor is PRETO) and (self.filhosPretos(irmao)):
                irmao.cor = VERMELHO

                if pai.cor is PRETO:
                    no = no.pai
                    continue
                else:
                    pai.cor = PRETO
                    break

            # Irmao vermelho com filhos pretos ou nulos
            if (irmao.cor is VERMELHO) and (self.filhosPretos(irmao)):

                # Troca a cor
                corAux = pai.cor
                pai.cor = irmao.cor
                irmao.cor = corAux

                # Rotaciona
                if filhoDir:
                    # Direita
                    pai.esq = irmao.dir
                    irmao.dir.pai = pai
                    irmao.dir = pai
                    pai.pai = irmao
                else:
                    # Esquerda
                    pai.dir = irmao.esq
                    irmao.esq.pai = pai
                    irmao.esq = pai
                    pai.pai = irmao

                irmao.pai = avo

                if avo is None:
                    self.raiz = irmao
                    continue
                else:
                    if avo.dir is pai:
                        avo.dir = irmao
                    else:
                        avo.esq = irmao


                if filhoDir:
                    no = pai.dir
                else:
                    no = pai.esq

                continue

            # Filhos de cada cor
            if (irmao.cor is PRETO) and (not self.filhosVermelhos(irmao)):

                # Subrinho mais longe
                if (filhoDir and (irmao.esq is not None) and irmao.esq.cor == VERMELHO) or ((not filhoDir) and (irmao.dir is not None) and (irmao.dir.cor == VERMELHO)):

                    corAux = irmao.cor
                    irmao.cor = irmao.pai.cor
                    irmao.pai.cor = corAux

                    #Rotaciona
                    if (filhoDir):

                        # Direita
                        pai.esq = irmao.dir
                        if irmao.dir is not None:
                            irmao.dir.pai = pai
                        irmao.pai = pai.pai

                        if pai.pai is not None:
                            if pai.pai.dir is pai:
                                pai.pai.dir = irmao
                            else:
                                pai.pai.esq = irmao
                        else:
                            self.raiz = irmao

                        pai.pai = irmao
                        irmao.dir = pai

                        irmao.esq.cor = PRETO
                    else:
                        # Esquerda
                        pai.dir = irmao.esq
                        if irmao.esq is not None:
                            irmao.esq.pai = pai
                        irmao.pai = pai.pai

                        if pai.pai is not None:
                            if pai.pai.dir is pai:
                                pai.pai.dir = irmao
                            else:
                                pai.pai.esq = irmao
                        else:
                            self.raiz = irmao

                        pai.pai = irmao
                        irmao.esq = pai

                        irmao.dir.cor = PRETO

                    break

                # Subrinho mais perto
                if (filhoDir and (irmao.dir is not None) and irmao.dir.cor == VERMELHO) or (not filhoDir and (irmao.esq is not None) and irmao.esq.cor == VERMELHO):

                    # Encontra o filho vermelho
                    filho_v = None
                    if (irmao.dir is not None) and (irmao.dir.cor == VERMELHO):
                        filho_v = irmao.dir
                    else:
                        filho_v = irmao.esq

                    # Troca a cor filho vermelho - irmao
                    corAux = irmao.cor
                    irmao.cor = filho_v.cor
                    filho_v.cor = corAux

                    # Rotaciona
                    if filhoDir:
                        # Esquerda
                        filho_v.pai = irmao.pai
                        irmao.pai.esq = filho_v

                        irmao.dir = filho_v.esq
                        filho_v.esq = irmao
                        irmao.pai = filho_v

                        if irmao.dir is not None:
                            irmao.dir.pai = irmao
                    else:
                        # Direita
                        filho_v.pai = irmao.pai
                        irmao.pai.dir = filho_v

                        irmao.esq = filho_v.dir
                        filho_v.dir = irmao
                        irmao.pai = filho_v

                        if irmao.esq is not None:
                            irmao.esq.pai = irmao

                    continue

            if self.filhosVermelhos(irmao):

                corAux = irmao.cor
                irmao.cor = pai.cor
                pai.cor = corAux

                if filhoDir:
                    pai.esq = irmao.dir
                    pai.esq.pai = pai
                    irmao.dir = pai
                    pai.pai = irmao
                    irmao.esq.cor = PRETO
                else:
                    pai.dir = irmao.esq
                    pai.dir.pai = pai
                    irmao.esq = pai
                    pai.pai = irmao
                    irmao.dir.cor = PRETO

                irmao.pai = avo

                if avo is None:
                    self.raiz = irmao
                    break
                else:
                    if avo.dir is pai:
                        avo.dir = irmao
                    else:
                        avo.esq = irmao
                break

            print("Erro: Loop Chegou até o fiinal")
            arvore.print_tree_op()
            print(no.chave)
            exit(9)

        self.raiz.cor = PRETO
        return self.raiz

    def remove(self, raizArv: No, chave):
        no = self.get(raizArv, chave)

        if no is None:
            return self.raiz

        filhoDir = False

        if no is not self.raiz:
            filhoDir = (no.pai.dir is no)

        # E folha
        if self.eFolha(no):
            # Folha e vermelha
            if no.cor is VERMELHO:
                if no.pai.esq is no:
                    no.pai.esq = None
                else:
                    no.pai.dir = None

                no = None
                return self.raiz

            # Folha e preta
            pai = no.pai
            irmao = None

            if filhoDir is True:
                if no.pai is None:
                    irmao = None
                else:
                    irmao = no.pai.esq
            else:
                if no.pai is None:
                    irmao = None
                else:
                    irmao = no.pai.dir

            if pai is None:
                avo = None
            else:
                if pai.pai is None:
                    avo = None
                else:
                    avo = pai.pai

            tmp = no
            aux = self.checar(no)

            if pai is not None:
                if pai.dir == tmp:
                    no.pai.dir = None
                else:
                    no.pai.esq = None

            if (no is self.raiz) and (no.dir is None) and (no.esq is None):
                return None

            return self.raiz

        # Nao e folha
        if no.esq is not None:
            # Copia o max e remove
            maximo = self.fmax(no.esq)
            no.chave = maximo.chave
            no.item = maximo.item
            aux = self.remove(no.esq, maximo.chave)
        else:
            # Copia do min e remove
            minimo = self.fmin(no.dir)
            no.chave = minimo.chave
            no.item = minimo.item
            aux = self.remove(no.dir, minimo.chave)

        return self.raiz

    # Impressao e verificacao ----------------------------------------------------------------------

    def print_tree_op(self):

        if self.raiz is None:
            print("Arvore Vazia")
        else:
            self.print_tree(self.raiz)

    def print_tree(self, raiz_arv: No):
        if raiz_arv.esq is not None:
            self.print_tree(raiz_arv.esq)
            print("\"", raiz_arv.chave, raiz_arv.cor, "\"", "->",
                  "\"", raiz_arv.esq.chave, raiz_arv.esq.cor, "\"")

        if raiz_arv.dir is not None:
            self.print_tree(raiz_arv.dir)
            print("\"", raiz_arv.chave, raiz_arv.cor, "\"", "->",
                  "\"", raiz_arv.dir.chave, raiz_arv.dir.cor, "\"")

        if raiz_arv.esq is None and raiz_arv.dir is None:
            print("\"", raiz_arv.chave, raiz_arv.cor, "\"")

    def balanceada_op(self):
        preto = 0
        no = self.raiz

        while no is not None:
            if no.cor is not VERMELHO:
                preto += 1
            no = no.esq
        return self.balanceada(self.raiz, preto)

    def balanceada(self, no: No, preto):
        if no is None:
            return (preto == 0)
        if no.cor is not VERMELHO:
            preto -= 1
        return (self.balanceada(no.esq, preto)) and (self.balanceada(no.dir, preto))

    def verificar_pai(self, no: No):
        if no is not None and no.pai is not None:
            print("\"", no.chave, no.cor, "\"", "->",
                  "\"", no.pai.chave, no.pai.cor, "\"")

        if no is not None:
            self.verificar_pai(no.esq)
            self.verificar_pai(no.dir)

    def verificar_pai_op(self):
        self.verificar_pai(self.raiz)


# TESTE

if __name__ == '__main__':


    for a in range(1, 1000):
        arvore = RN()
        numeros = []

        numeros.clear()
        for i in range(1, 100):
            x = randint(0, 1000)
            arvore.put_op(x)
            print(x)
            numeros.append(x)

            if arvore.balanceada_op() is False:
                print("Erro 1")
                print(numeros)
                exit()

        arvore.print_tree_op()
        tam = len(numeros)

        for i in range(1, 100):
            #print("Original")
            #arvore.print_tree_op()

            k = random.choices(numeros, k=1)

            arvore.remove_op(k[0])

            cond = arvore.balanceada_op()

            if cond is not True:
                print("Erro 2")
                print("Resultado: ", cond)
                print(numeros, k)
                arvore.print_tree_op()
                exit()

            numeros.remove(k[0])
            tam -=1

            print("Removido: ", k)

        arvore.print_tree_op()
        print("K: ", a)
        if tam != 0:
            arvore.print_tree_op()
            print("Erro tam", tam)
            exit(9)
        del arvore