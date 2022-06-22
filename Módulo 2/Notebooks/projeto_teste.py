import json

class EmailInvalido(Exception):
    def __init__(self, email, mensagem='Formato do email inválido.'):
        self.email = email
        self.message = mensagem
        super().__init__(self.message)

class EmailJaCadastrado(Exception):
    def __init__(self, email, mensagem='Email já cadastrado.'):
        self.email = email
        self.message = mensagem
        super().__init__(self.message)

class SemGenero(Exception):
    def __init__(self, mensagem='Deve-se cadastrar ao menos um gênero musical.'):
        self.message = mensagem
        super().__init__(self.message)

class SemInstrumento(Exception):
    def __init__(self, mensagem='Deve-se cadastrar ao menos um instrumento musical.'):
        self.message = mensagem
        super().__init__(self.message)

class NomeInvalido(Exception):
    def __init__(self, mensagem='Nome digitado é inválido.'):
        self.message = mensagem
        super().__init__(self.message)

class AbrirArquivo(Exception):
    def __init__(self, mensagem='Não foi possível abrir o arquivo.'):
        self.message = mensagem
        super().__init__(self.message)

class SalvarArquivo(Exception):
    def __init__(self, mensagem='Não foi possível salvar o arquivo..'):
        self.message = mensagem
        super().__init__(self.message)

def abrir_base() -> list:
    try:
        with open('musicos.json', 'r', encoding = 'utf-8') as arquivo:
            base = json.loads(arquivo.read())
            return base
    except:
        raise AbrirArquivo()

def salvar_base(base: list) -> None:
    try:
        with open('musicos.json', 'w', encoding = 'utf-8') as arquivo:
            arquivo.write(json.dumps(base, indent=4))
    except:
        raise SalvarArquivo()


def imprimir(dados: list) -> None:
    if dados == []:
        print('Não foram encontrados resultados!')
    else:
        for i in dados:
            print(f'NOME: {i["nome"].title()}\nEMAIL: {i["email"]}\nGÊNEROS: {", ".join(i["generos"]).capitalize()}\nINSTRUMENTOS: {", ".join(i["instrumentos"]).capitalize()}\n')

def verifica_email(email: str) -> None:
    caracteres_validos = 'abcdefghijklmnopqrstuvwxyz@_.'
    if email.count('@') != 1: raise EmailInvalido(email)
    for i in email:
        if i not in caracteres_validos: raise EmailInvalido(email)


def obter_info(dados = None, cadastrar = False, busca = False, modificar = False, **kwargs) -> dict:
    nome = input('Digite o nome: ').strip().lower() if not modificar else kwargs['nome']
    if not nome.replace(' ', '').isalpha() and not busca: raise NomeInvalido('O formato do nome é inválido!') 
    email = input('Digite o email: ').strip().lower() if not modificar else kwargs['email']
    if cadastrar:
        verifica_email(email)
        for em in dados:
            if email != em['email']:
                continue
            raise EmailJaCadastrado(email)
    generos = []
    usuario_input_genero = input('Digite um gênero musical: ').strip().lower() 
    if usuario_input_genero == '' and cadastrar:  raise SemGenero()
    generos.append(usuario_input_genero)
    while usuario_input_genero and not busca:
        usuario_input_genero = input('Digite outro gênero musical, caso não haja mais estilos apenas pressione ENTER: ').strip().lower()
        if usuario_input_genero != '': generos.append(usuario_input_genero)
    instrumentos = []
    usuario_input_inst = input('Digite um instrumento musical: ').strip().lower()
    if usuario_input_inst == '' and cadastrar:  raise SemInstrumento()
    instrumentos.append(usuario_input_inst)
    while usuario_input_inst and not busca:
        usuario_input_inst = input('Digite outro instrumento musical, caso não haja mais instrumentos apenas pressione ENTER: ').strip().lower()
        if usuario_input_inst != '': instrumentos.append(usuario_input_inst)
    return {'nome': nome, 'email': email, 'generos': generos, 'instrumentos': instrumentos}


def cadastra_usuario() -> None:
    base_musicos = abrir_base()
    novo_usuario = obter_info(cadastrar = True, dados = base_musicos)
    print('Por favor, confirme os dados que você digitou: ')
    imprimir([novo_usuario])
    confirmacao = input('Você deseja adicionar este usuário na base de dados? (S/N)').lower().strip()
    while confirmacao != 's' and confirmacao != 'n':
        confirmacao = input('Desculpe, não entendi! Você deseja adicionar este usuário na base de dados? (S/N)').lower().strip()
    if confirmacao == 's':
        base_musicos.append(novo_usuario)
        salvar_base(base_musicos)
        print('\nUsuário cadastrado com sucesso!\n')
    else:
        print('\nO usuário não foi cadastrado!\n')


def comparando_info(info: dict, cadastro: dict, todas_info: bool) -> bool:
    ''' Recebe dois dicionários e compara se os dois dicionários possuem as mesmas informações.
    todas_info: se True devolve True se todos os valores do dicionário coincidem. Se False, devolve
    True se pelo menos um valor coincide.
    '''
    resposta = True
    if info['nome']: 
        if info['nome'] == cadastro['nome']:
            if not todas_info:
                return True
        else: 
            resposta = False
    if info['email']: 
        if info['email'] == cadastro['email']:
            if not todas_info:
                return True
        else: 
            resposta = False
    if info['generos'][0] != '':
        if info['generos'][0] in cadastro['generos']: 
            if not todas_info:
                return True
        else: 
            resposta = False
    if info['instrumentos'][0] != '':
        if info['instrumentos'][0] in cadastro['instrumentos']:         
            if not todas_info:
                return True
        else: 
            resposta = False
    return resposta
        

def buscar_musicos() -> None:
    base_musicos = abrir_base()
    print('\nInsira as informações que deseja inserir na busca. DEIXE EM BRANCO as outras.\n')
    info = obter_info(busca = True)
    regra_busca = input('Os resultados devem conter TODAS as informações dadas? (S/N)').lower().strip()
    while regra_busca != 's' and regra_busca != 'n':
        regra_busca = input('Desculpe, não entendi! Os resultados devem conter TODAS as informações dadas? (S/N)').lower().strip()
    todas_info = True if regra_busca == 's' else False
    resultado_busca = [cadastro for cadastro in base_musicos if comparando_info(info, cadastro, todas_info)]
    if len(resultado_busca) == 0:
        print('Não foram encontrados resultados com os dados inseridos.\n')
    else:
        print('Os seguintes resultados foram encontrados: \n')
        imprimir(resultado_busca)

def modificar_musicos() -> None:
    base_musicos = abrir_base()
    email_input = input('Digite o email do músico que deseja modificar: ').lower().strip()
    i = 0
    while i < len(base_musicos):
        if base_musicos[i]['email'] == email_input:
            num_cadastro = i
            break
        i += 1
    else: 
        return print('Usuário não encontrado na base de músicos.\n'
                    'Você foi redirecionado ao menu.\n')
    print(f'Digite as novas informações sobre gêneros musicais e instrumentos do usuário {base_musicos[num_cadastro]["nome"].title()},\nregistrado com o email {email_input}: \n')
    base_musicos[num_cadastro] = obter_info(modificar = True, email = email_input, nome = base_musicos[num_cadastro]["nome"])
    salvar_base(base_musicos)
    print('\n Usuário modificado com sucesso!\n')


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
    arranjo = [i for i in combinacoes if len(set(i)) == len(lista)]
    return arranjo


def imprimir_bandas(bandas_filtradas: list, instrumentos: list) -> None:
    bandas= [[j + ' - ' + k for j, k in zip(i, instrumentos)] for i in bandas_filtradas]
    bandas_unicos = [] # eliminando o caso de repetições com bandas com dois (ou mais) instrumentos iguais
    for i in bandas:
        if set(i) not in bandas_unicos:
            bandas_unicos.append(set(i))
    print(f'Foram encontradas {len(bandas_unicos)} opções de bandas: \n')
    for i, elemento in enumerate(bandas_unicos):
        print(f'{i + 1}ª opção de banda:\n')
        print('| ', end = '')
        for j in elemento:
            print(j, end = ' | ')
        print('\n')
        print('-'* 100)

def montar_bandas() -> None:
    base_musicos = abrir_base()
    genero = input('Digite o genero musical da banda que deseja montar: ').lower().strip()
    num_integrantes = int(input('Digite o número de integrantes da banda: '))
    instrumentos = [input(f'Digite o instrumento do {i + 1}º membro da banda.').lower().strip() for i in range(num_integrantes)]
    # monta uma lista de listas onde a primeira lista contém os emails de toca o primeiro instrumento, a segunda lista 
    # os emails de que toca o segundo instrumento e assim por diante
    musicos_instrumentos = [[j['email'] for j in base_musicos if i in j['instrumentos'] and genero in j['generos']] for i in instrumentos]
    # criando todas as combinações de bandas, incluindo as com mesmo email e mais de um instrumento
    bandas = lista_combinacoes(musicos_instrumentos)
    # inserindo o instrumento ao lado de cada email, até aqui o instrumento era notado na ordem do membro da banda
    imprimir_bandas(bandas, instrumentos)


def selecionar_opcao() -> str:
    opcoes = ('0', '1', '2', '3', '4')
    print('Selecione a opção desejada: \n'
        '1.\tCadastrar músico\n'
        '2.\tBuscar músicos\n'
        '3.\tModificar músico\n'
        '4.\tMontar bandas\n'
        '0.\tSair\n')
    opcao = input()
    while opcao not in opcoes:
        opcao = input('Por favor, digite uma opção válida: ')
    return opcao


def menu() -> None:
    print('Bem vindo!\n')
    opcoes_dict = { 
        '1': cadastra_usuario,
        '2': buscar_musicos,
        '3': modificar_musicos,
        '4': montar_bandas
    } 
    opcao = '_'
    while opcao != '0':
        opcao = selecionar_opcao()
        if opcao == '0': 
            print('Programa encerrado!')
            continue
        try:
            opcoes_dict[opcao]()
        except EmailInvalido as excecao:
            print(f'O email {excecao.email} não é considerado um email válido!\n'
                    'Você foi direcionado ao menu.\n')
        except EmailJaCadastrado as excecao:
            print(f'O email {excecao.email} digitado já está!\n'
                    'Você foi direcionado ao menu.\n')
        except SemGenero:
            print('Deve-se adicionar pelo menos um gênero musical.\n'
                    'Você foi direcionado ao menu.\n')
        except SemInstrumento:
            print('Deve-se adicionar pelo menos um instrumento musical.\n'
                    'Você foi direcionado ao menu.\n')
        except NomeInvalido:
            print('O nome digitado é inválido.\n'
                    'Você foi direcionado ao menu.\n')
        except ValueError:
            print('O valor digitado deveria ser um número inteiro.\n'
                    'Você foi direcionado ao menu.\n')
        except AbrirArquivo:
            print('Ocorreu um erro ao acessar a base de dados.\n'
                    'Você foi direcionado ao menu.\n')
        except SalvarArquivo:
            print('Ocorreu um erro ao salvar a base de dados.\n'
                    'Você foi direcionado ao menu.\n')
        except:
            print('Ocorreu um erro desconhecido.\n'
                    'Você foi direcionado ao menu.\n')

menu()