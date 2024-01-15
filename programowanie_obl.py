import numpy as np
from itertools import combinations
from typing import List, Callable

#1. 
#miary ilościowe
def euclidean_dist(x, y):
    x = np.array(x)
    y = np.array(y)
    return np.sqrt(np.sum((x - y)**2))
result_euclidean = euclidean_dist(12, 10)
print(result_euclidean)
    #miara manhattan
def manhattan_dist(x, y):
    return np.sum(np.abs(x - y))
result_manhattan = manhattan_dist(12, 10)
print(result_manhattan)
#miary jakościowe
    #miara hamminga
def hamming_dist(x, y):
    dif_count = 0
    if len(x) != len(y):
        print("Strings must be of equal length.")
        return -1
    for i, j in zip(x, y):
        dif_count += 1 if i != j else 0
    return dif_count
assert hamming_dist('1010', '1010') == 0
assert hamming_dist('1010', '1011') == 1
assert hamming_dist('1', '10100') == -1
str1 = '0769653'
str2 = '1110011'
result_hamming = hamming_dist(str1, str2)
print(result_hamming)
    #miara jaccarda

from typing import Set
def jaccard_dist(set1: Set, set2: Set) -> int:
    intersect = set1 & set2
    union = set1 | set2
    common_elements = len(intersect)
    all_uniqe = len(union)
    return 1 - common_elements / all_uniqe

assert jaccard_dist({"A", "B", "C", "D", "D"}, {"A", "B", "C", "D", "D"}) == 0.0
assert jaccard_dist({"A", "B", "C", "D", "E"}, {"F", "G", "H", "I", "J"}) == 1.0


set1 = ["A", "B", "C", "D", "E"]
set2 = ["F", "D", "E", "H", "I"]

result_jaccard = jaccard_dist(set(set1), set(set2))
print(f"Jaccard Distance: {result_jaccard}")
#2
#grupowanie hierarchiczne metodami aglomeracyjnymi(czyli takimi, gdzie pojedyncze obiekty grupuję w jedną grupę skupiającą je wszystkie)

#average linkage hierarchical - 
    #Znaleźć najmniejszą odległość między punktami i stworzyć z nich klaster
    #wyliczyć na nowo odległości ze zaktualizowaną macierzą - odległośc stworzona grupa i reszta punktów
    #powtórz
def linkage_method(points: List, dist: Callable = euclidean_dist):
    dist_cache = {}
    for p1, p2 in combinations(points, 2):
        dist_cache[p1, p2] = dist(p1, p2)
    
    # odswiezanie odleglosci (zastepowanie kolejnych elementow grupami i usrednianie dystansow)
    # dzialamy tak dlugo az wszystko zostanie zgrupowane w 1 'super-grupe'
    while len(dist_cache) > 1 :
        # znajdujemy najblizsze sobie elementy (nowa grupa)
        # workaround, bo min() przestal dzialac na zlozonych kluczach
        closest_group = list(dist_cache.keys())[0]
        for key, item in dist_cache.items():
            if item < dist_cache[closest_group]:
                closest_group = key

        # tworzymy nowa macierz odleglosci (dist_cache), zaczynamy od tmp, ktorym ja zastapimy
        tmp = {}
        for key, item in dist_cache.items():
            # przepisujemy odleglosci, ktore nie ulegaja zmianie
            if key[0] not in closest_group and key[1] not in closest_group:
                tmp[key] = item

        # dla wszystkich obiektow (obiekt moze byc punktem lub grupa) wyznaczamy odleglosc do nowopowstalej grupy
        for p in set([item for items in dist_cache.keys() for item in items]):
            if p in closest_group:
                continue

            # odleglosci do obu skladowych closest_group, sprawdzamy obie kombinacje kluczy (kolejnosc elementow w kluczu ma znacznie)
            c1, c2 = closest_group
            d1 = dist_cache[p, c1] if (p, c1) in dist_cache else dist_cache[c1, p]
            d2 = dist_cache[p, c2] if (p, c2) in dist_cache else dist_cache[c2, p]
            # zapisanie nowej odleglosci
            tmp[p, closest_group] = 0.5 * (d1 + d2)
        # nadpisujemy macierz odleglosci dla nowego przebiegu petli
        dist_cache = tmp
    # koniec petli
    # macierz odleglosci zbudowana, ma 1 klucz
        
    
cluster = linkage_method([(0.4, 0.53), (0.22, 0.38), (0.35,0.32), (0.26, 0.19), (0.08, 0.41), (0.45, 0.3)])
print("complete linkage method:")
print(cluster)

#complete linkage hierarchical - odległość między najdalszymi elementami - metoda najdalszego sąsiada
#znajdź najwiejszą odległosć między punktami i stwórz klaster