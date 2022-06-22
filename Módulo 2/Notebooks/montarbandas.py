def lista_combinacoes(lista: list) -> list:
    ''' Recebe uma lista de listas e retorna todas os arranjos de escolhas de um elemento de cada lista.
    Exemplos: lista_combinacoes([[1, 2], [3, 4, 5]]) --> [[1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
    '''
    if len(lista) == 0:
        return [[]]
    combinacoes = [[]]
    for i in range(len(lista)):
        combinacoes = [y + [x] for x in lista[i] for y in combinacoes]
    # retira as listas com elementos repetidos
    arranjo =[i for i in combinacoes if len(set(i)) == len(lista)]
    return arranjo
lista_combinacoes([[1, 2], [1, 4, 5], [2, 7]])