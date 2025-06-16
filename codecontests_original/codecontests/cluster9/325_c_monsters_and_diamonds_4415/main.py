#!/usr/bin/env python3

import sys, heapq

_BLANCO, _GRIS, _NEGRO = 0, 1, 2
_OO = int(1e18)


class Regla:
    def __init__(self, id, diamantes, deMonstruo, monstruos):
        self.id = id
        self.diamantes = diamantes
        self.deMonstruo = deMonstruo
        self.monstruos = monstruos

    def clonar(self):
        return Regla(self.id, self.diamantes, self.deMonstruo, self.monstruos[:])


def esUnaMalaRegla(r, d):
    for m in r.monstruos:
        if d[m] == _OO:
            return True

    return False


def dfsVisit(u, color, reglas, diamMax, d):
    color[u] = _GRIS

    for r in reglas[u]:
        if esUnaMalaRegla(r, d):
            continue

        sumaMax = r.diamantes

        for v in r.monstruos:
            if color[v] == _BLANCO:
                dfsVisit(v, color, reglas, diamMax, d)

                if diamMax[v] > 0:
                    sumaMax += diamMax[v]

            elif color[v] == _GRIS:
                diamMax[v] = -2

            elif color[v] == _NEGRO:
                sumaMax += diamMax[v]

            if diamMax[v] == -2:
                diamMax[u] = -2
                color[u] = _NEGRO
                return

        diamMax[u] = max(diamMax[u], sumaMax)

    color[u] = _NEGRO


def dfs(reglas, d):
    n = len(reglas)
    color, diamMax = [], []

    for i in range(n):
        color.append(_BLANCO)
        diamMax.append(0)

    for u in range(n):
        if color[u] == _BLANCO:
            dfsVisit(u, color, reglas, diamMax, d)

    return diamMax


def dijkstra(reglas, s, m, perteneceA):
    n = len(reglas)
    d = []
    Q, visto = [], []
    k, sumaMin = [0] * m, []
            
    for u in range(n):
        d.append(_OO)
        visto.append(False)

        for r in reglas[u]:
            sumaMin.append(0)
            k[r.id] = len(r.monstruos)

    d[s] = 0
    Q.append((0, s))
    heapq.heapify(Q)

    while len(Q) != 0:
        u = heapq.heappop(Q)[1]

        if visto[u]:
            continue

        visto[u] = True

        for p in perteneceA[u]:
            r = reglas[p[0]][p[1]]
            ocurrencias = p[2]

            k[r.id] -= ocurrencias
            sumaMin[r.id] += d[u] * ocurrencias

            if k[r.id] == 0 and d[r.deMonstruo] > sumaMin[r.id] + r.diamantes:
                d[r.deMonstruo] = sumaMin[r.id] + r.diamantes;
                heapq.heappush(Q, (d[r.deMonstruo], r.deMonstruo))

    return d


def anyadirVerticeFicticio(reglas, perteneceA):
    n = len(reglas)
    nuevasReglas = []

    perteneceA.append([])  # pertenencia del vertice ficticio

    for u in range(n):
        nuevasReglas.append([])

        for r in reglas[u]:
            nuevasReglas[u].append(r.clonar())

            if len(r.monstruos) == 0:
                nuevasReglas[u][-1].monstruos.append(n)  # anyadiendo vertice ficticio
                perteneceA[n].append((u, len(nuevasReglas[u]) - 1, 1))

    nuevasReglas.append([])  # reglas del vertice ficticio

    return nuevasReglas


def resolver(reglas, m, perteneceA):
    n = len(reglas)

    reglasConVertFicticio = anyadirVerticeFicticio(reglas, perteneceA)
    d = dijkstra(reglasConVertFicticio, n, m, perteneceA)
    diamMax = dfs(reglas, d)

    UPPER = 314000000

    for u in range(n):
        if d[u] < _OO:
            sys.stdout.write("%d %d" % (min(d[u], UPPER), min(diamMax[u], UPPER)))

        else:
            sys.stdout.write("-1 -1")

        sys.stdout.write("\n")


def leer_enteros():
    return [int(cad) for cad in sys.stdin.readline().split()]


if __name__ == "__main__":
    m, n = leer_enteros()

    ocurr, perteneceA, reglas = [], [], []

    for i in range(n):
        ocurr.append(0)
        perteneceA.append([])
        reglas.append([])

    for i in range(m):
        enteros = leer_enteros()
        mi = enteros[0] - 1

        r = Regla(i, 0, mi, [])

        for x in enteros[2:]:
            x -= 1

            if x >= 0:
                ocurr[x] += 1
                r.monstruos.append(x)

            else:
                r.diamantes += 1

        for mons in r.monstruos:
            if ocurr[mons] != 0:
                perteneceA[mons].append((mi, len(reglas[mi]), ocurr[mons]))

            ocurr[mons] = 0

        reglas[mi].append(r)

    resolver(reglas, m, perteneceA)