import json
import os.path
import sys


def obter_dados() -> list:
    '''
    Essa função carrega os dados dos produtos e retorna uma lista de dicionários, onde cada dicionário representa um produto com sua 'ID', 'CATEGORIA', 'PREÇO'.
    '''
    with open(os.path.join(sys.path[0], 'dados.json'), 'r') as arq:
        dados = json.loads(arq.read())
    return dados


def listar_categorias(dados: list) -> list:
    '''
    Cria uma lista com as categorias dos dados.
    '''
    categorias_set = set([])
    for i in dados:
        categorias_set.add(i['categoria'])
    categorias = sorted(list(categorias_set))
    return categorias


def escolher_categoria(dados: list) -> str:
    '''
    Fazer e validar o input da escolha de uma categoria, devolve a string 9 caso, por algum motivo, o usuário deseja voltar ao menu sem digitar a categoria.
    '''
    categoria = input('Digite a categoria que desejada: ').replace(
        ' ', '_').lower()
    voltar_menu = True
    while categoria not in listar_categorias(dados) and voltar_menu:
        categoria = input(
            'Esta categoria não existe, por favor digite uma categoria válida ou digite 9 para voltar ao menu anterior.\n')
        if categoria == '9':
            voltar_menu = False
    return categoria


def listar_por_categoria(dados: list, categoria: str) -> list:
    '''
    Devolve uma lista com dados de uma determinada categoria.
    '''
    produtos_list = []
    if categoria in listar_categorias(dados):
        for i in dados:
            if i['categoria'] == categoria:
                produtos_list.append(i)
    else:
        print('Categoria não encontrada!')
    return produtos_list


def produto_mais_caro(dados: list, categoria: str) -> dict:
    '''
    Devolve o dado de valor mais caro de uma determinada categoria. 
    '''
    return sorted(listar_por_categoria(dados, categoria), key=lambda x: float(x['preco']))[-1]


def produto_mais_barato(dados: list, categoria: str) -> dict:
    '''
    Devolve o dado de valor mais barato de uma determinada categoria. 
    '''
    return sorted(listar_por_categoria(dados, categoria), key=lambda x: float(x['preco']))[0]


def mais_caro(dados: list) -> dict:
    '''
    Devolve o dado de valor mais caro. 
    '''
    return sorted(dados, key=lambda x: float(x['preco']))[-1]


def mais_barato(dados: list) -> dict:
    '''
    Devolve o dado de valor mais barato. 
    '''
    return sorted(dados, key=lambda x: float(x['preco']))[0]


def top_10_caros(dados: list) -> list:
    '''
    Devolve uma lista com os 10 dados mais caros. 
    '''
    return sorted(dados, key=lambda x: float(x['preco']))[-10:]


def top_10_baratos(dados: list) -> list:
    '''
    Devolve uma lista com os 10 dados mais baratos. 
    '''
    return sorted(dados, key=lambda x: float(x['preco']))[:10]


def imprimir_dados_tabela(dados: list) -> None:
    '''
    Imprime os dados no formato de uma tabela.
    '''
    col_1 = max(
        len(sorted(dados, key=lambda x: len(x['id']))[-1]['id']), len('ID'))
    col_2 = max(len(sorted(dados, key=lambda x: len(
        x['categoria']))[-1]['categoria']), len('CATEGORIA'))
    col_3 = max(len(sorted(dados, key=lambda x: len(
        x['preco']))[-1]['preco']) + 3, len('PRECO'))
    espacos_col_1_esq_titulo = (col_1 - len('id'))//2
    espacos_col_1_dir_titulo = col_1 - len('id') - espacos_col_1_esq_titulo + 1
    espacos_col_2_esq_titulo = (col_2 - len('categoria'))//2
    espacos_col_2_dir_titulo = col_2 - \
        len('categoria') - espacos_col_2_esq_titulo
    espacos_col_3_esq_titulo = (col_3 - len('preco'))//2
    espacos_col_3_dir_titulo = col_3 - len('preco') - espacos_col_3_esq_titulo
    print('+' + '-'*(col_1 + col_2 + col_3 + 15) + '+')
    print('|', ' '*espacos_col_1_esq_titulo, 'ID', ' '*espacos_col_1_dir_titulo, '|', ' '*espacos_col_2_esq_titulo,
          'CATEGORIA', ' '*espacos_col_2_dir_titulo, '|', ' '*espacos_col_3_esq_titulo, 'PREÇO', ' '*espacos_col_3_dir_titulo, '|')
    print('+' + '-'*(col_1 + col_2 + col_3 + 15) + '+')
    for i in dados:
        espacos_col_1_esq = (col_1 - len(i['id']))//2
        espacos_col_1_dir = col_1 - len(i['id']) - espacos_col_1_esq
        espacos_col_2_esq = (col_2 - len(i['categoria']))//2
        espacos_col_2_dir = col_2 - len(i['categoria']) - espacos_col_2_esq
        espacos_col_3_esq = (col_3 - (len(i['preco'])+3))//2
        espacos_col_3_dir = col_3 - len(i['preco']) - 3 - espacos_col_3_esq
        print('|', ' '*espacos_col_1_esq, i['id'], ' '*espacos_col_1_dir, ' '*(col_1 - len(i['id'])), '|', ' '*espacos_col_2_esq, i['categoria'].replace(
            '_', ' ').capitalize(), ' '*espacos_col_2_dir, '|', ' '*espacos_col_3_esq, 'R$ ' + i['preco'].replace('.', ','), ' '*espacos_col_3_dir, '|')
        print('+' + '-'*(col_1 + col_2 + col_3 + 15) + '+')


def menu(dados: list) -> None:
    '''
    Inicializa o menu principal com as iterações e consultas em dados.
    '''
    rodar_menu = True
    opcoes = ('0', '1', '2', '3', '4', '5', '6')
    while rodar_menu:
        opcao = input('As opções são:\n'
                      '1. Listar categorias\n'
                      '2. Listar produtos de uma categoria\n'
                      '3. Produto mais caro por categoria\n'
                      '4. Produto mais barato por categoria\n'
                      '5. Top 10 produtos mais caros\n'
                      '6. Top 10 produtos mais baratos\n'
                      '0. Sair\n'
                      'Digite um número para prosseguir: ')
        if opcao not in opcoes:
            print('Opção inválida!')
        else:
            if opcao == '1':
                print('As categorias são: \n')
                comp_linha = 0
                for i in range(len(listar_categorias(dados)) - 1):
                    if comp_linha < 50:
                        print(listar_categorias(dados)[i].replace(
                            '_', ' ').capitalize(), end=', ')
                        comp_linha += len(listar_categorias(dados)[i])
                    else:
                        print(listar_categorias(dados)[i].replace(
                            '_', ' ').capitalize() + ',')
                        comp_linha = 0
                print(listar_categorias(dados)
                      [-1].replace('_', ' ').capitalize()+'.')
            elif opcao == '2':
                categoria = escolher_categoria(dados)
                if categoria == '9':
                    pass
                else:
                    imprimir_dados_tabela(
                        listar_por_categoria(dados, categoria))
            elif opcao == '3':
                categoria = escolher_categoria(dados)
                if categoria == '9':
                    pass
                else:
                    mais_caro = produto_mais_caro(dados, categoria)
                    imprimir_dados_tabela([mais_caro])
            elif opcao == '4':
                categoria = escolher_categoria(dados)
                if categoria == '9':
                    pass
                else:
                    mais_barato = produto_mais_barato(dados, categoria)
                    imprimir_dados_tabela([mais_barato])
            elif opcao == '5':
                imprimir_dados_tabela(top_10_caros(dados))
            elif opcao == '6':
                imprimir_dados_tabela(top_10_baratos(dados))
            elif opcao == '0':
                rodar_menu = False
    else:
        print('Muito obrigado, espero tê-lo ajudado!')


dados = obter_dados()
menu(dados)
