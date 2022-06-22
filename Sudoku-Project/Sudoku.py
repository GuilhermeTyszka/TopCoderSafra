def lista_combinacoes(lista):
    if len(lista) == 0:
        return [[]]
    combinacoes = []
    for i in lista[0]:
        resto_lista = lista[1:]
        resto_lista_combinada = lista_combinacoes(resto_lista)
        for j in resto_lista_combinada:
            combinacoes.append([i,*j])
    return combinacoes