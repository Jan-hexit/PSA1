# -*- coding: utf-8 -*-
import operator
def maxCycleTreeIndependentSet(T, w):
    """
    Najtežja neodvisna množica
    v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
    kjer ima tabela tež w dimenzije k×n (k >= 2).

    Vrne par (c, s), kjer je c teža najdene neodvisne množice,
    s pa je seznam vozlišč v neodvisni množici,
    torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
    """
    n = len(T)
    assert all(len(r) == n for r in w), \
        "Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
    assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), \
        "Podani graf ni neusmerjen!"
    k = len(w)
    slovar=dict()
    slovar2=dict()
    assert k >= 2, "k mora biti vsaj 2!"
    if n == 0:
        return (0, [])
    def drevo(T,w,V,vozlisce,obiskani):
        obiskani1=obiskani.copy() #zapomnemo si vozlisča ki smo jih že obiskali
        obiskani1.append(vozlisce)
        mozni_sosedi=[]
        for sosed in T[vozlisce]:#preverimo v katere sosede lahko gremo
            if sosed not in obiskani1:
                mozni_sosedi.append(sosed)
        cikel=[i for i in range(k)]
        for v in V:#izločimo vozlišča ki so v knofliktu s množico V izbrano v prejšnem vozlišču
            del cikel[cikel.index(v)]
        H=memorizacija2(cikel)#naredimo vse neodvisne množice
        maxmnozica, maximum = max(enumerate(sum(w[element][vozlisce] for element in M)+sum(memorizacija1(M,sosed,obiskani1)[0] for sosed in mozni_sosedi) for M in H), key=operator.itemgetter(1)) #izračunamo max vsote trenutne množice + sosedov
        izbrani=mnozica(H[maxmnozica],vozlisce)
        for sosed in mozni_sosedi: #zapomnemo si vozlišča ki smo jih izbrali prej
            izbrani+=memorizacija1(H[maxmnozica],sosed,obiskani1)[1]
        return [maximum,izbrani]
    def neodvisna_mn(A):
        if len(A)!=0:
            mnozica=[[A[0]]]
            for j in range(1,len(A)):#izbremo element in ga dodamo vsem kompatibilnim množicam
                pmn=[]
                for M in mnozica: #dodamo element kompatibilnim množicam
                    if A[j]==0 and (1 in M or k-1 in M): pass
                    elif A[j]==(k-1) and (0 in M or k-2 in M):pass
                    elif (A[j]+1) in M or (A[j]-1) in M: pass
                    else:
                        element=M.copy()
                        pmn+=[element+[A[j]]]
                mnozica+=pmn
            mnozica+=memorizacija2(A[1:])#rekurzivno dodamo še preostale množice ki ne vsebujejo A[0]
            return mnozica
        else:
            return [[]]
    def mnozica(G,vozlisce):#iz mnozice in vozlišča naredimo pare
        A=[]
        for a in G:
            A.append((a,vozlisce))
        return A
    def memorizacija1(V,sosed,obiskani1): #memorizacija za funkcijo drevo
        A=frozenset(V)
        B=frozenset(obiskani1)
        index=(A,sosed,B)
        if index in slovar:
            return slovar[index]
        else:
            slovar[index]=drevo(T,w,V,sosed,obiskani1)
            return slovar[index]
    def memorizacija2(A): #memorizacija za funkcijo neodvisna_mn
        B=frozenset(A)
        if B in slovar2:
            return slovar2[B]
        else:
            slovar2[B]=neodvisna_mn(A)
            return slovar2[B]
    return drevo(T,w,[],T[0][0],[])
    