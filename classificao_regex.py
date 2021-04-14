import re
import difflib
import os
from unicodedata import normalize
import pathlib

# Caminho do diretório explorado
PATH = 'C:\\Users\\savio\\Desktop\\Base Exploratoria'
# Score de quanto um tipo é semelhante ao tipo real
score = 0.7
# Lista com os cominhos dos arquivos resultados
list_result = list()
list_result.append('tipo,score,caminho,nome\n')
# Lista de tipos encontrados
list_types_found = list()
# Lista de nomes não definidos na imagem
list_undefined = list()
# Lista de tipos que não entrou por perissão do score e que pode ser falha
list_possible_failure_not_enter = list()
# Lista de tipos que entrou por perissão do score, mas que pode ser falha
list_possible_failure_enter = list()

# Tipos permitidos
TYPES = [
    "ABONO FALTAS",
    "ABONO PERMANENCIA",
    "AFASTAMENTO DO CARGO",
    "AFASTAMENTO PARA CONCORRER AO PLEITO ELEITORAL",
    "AFASTAMENTO PARA MANDATO SINDICAL",
    "AFASTAMENTO SEM JUSTIFICATIVA",
    "APOSENTADORIA",
    "APOSENTADORIA POR INVALIDEZ",
    "AVERBACAO TEMPO SERVICO",
    "CONCESSAO FINATE",
    "CONCESSAO LICENCA PREMIO",
    "DIARIAS",
    "FERIAS",
    "GOZO LICENCA PREMIO",
    "INDENIZACAO LICENCA PREMIO",
    "INDENIZACAO FERIAS E 13º SALARIO",
    "INDENIZACAO OUTRAS",
    "LICENCA ADOCAO",
    "LICENCA PARA ACOMPANHAMENTO DO CONJUGE",
    "LICENCA MEDICA",
    "LICENCA PARA ACOMPANHAR PESSOA DA FAMILIA",
    "LICENCA PARA EXERCICIO MANDATO ELETIVO",
    "LICENCA PARA TRATO INTERESSE PARTICULAR",
    "LICENCA PATERNIDADE",
    "MAJORACAO LICENCA PREMIO",
    "OUTROS",
    "PORTARIA CONCESSAO LICENCA PREMIO",
    "PORTARIA CONCESSAO LICENCA MEDICA",
    "PORTARIA CUMPRIMENTO",
    "PORTARIA DESIGNACAO",
    "PORTARIA DISPENSA",
    "PORTARIA LOTAR",
    "PORTARIA REMOCAO",
    "PORTARIA OUTRAS",
    "PROGRESSAO POR TITULACAO",
    "INCORPORACAO FUNCAO",
]

# Nomalizando e extraíndo texto importante do nome da imagem
def __normalize(word: str):
    word = normalize('NFKD', word[:-4]).encode('ASCII', 'ignore').decode('ASCII').upper()
    word = re.sub(r'[\d()\.]+', '', word)
    word = re.sub(r'[-]+', ' ', word)
    list_word = [w for w in word.split() if not w in 'DE']
    return ' '.join(list_word)

# Pegar provável tipo baseado em uma string
def __likely_type(path: str, name_file: str):
    _type = __normalize(name_file)
    likely = difflib.get_close_matches(_type, TYPES, n=1, cutoff=0)
    _score = difflib.SequenceMatcher(None, _type, likely[0]).ratio()
    if _score >= score:
        if _score <= score + 0.2:
            text = str(_score) + ' > ' + likely[0] + ' > - ' + os.path.join(path, name_file) + '\n'
            list_possible_failure_enter.append(text)
        return likely[0], _score
    else:
        _, file_extension = os.path.splitext(name_file)
        if file_extension != '.db':
            if _score >= score - 0.2:
                text = str(_score) + ' > ' + likely[0] + ' > - ' + os.path.join(path, name_file) + '\n'
                list_possible_failure_not_enter.append(text)
            list_undefined.append(os.path.join(path, name_file) + '\n')
        return None, _score

# Def para salvar informações em arquivo
def __save_file(_list: list, name: str):
    f = open(name, 'w', encoding='utf8')
    f.writelines(_list)

# Buscar tipo por página
def search_by_type_on_pages():
    for path, _, name_file in os.walk(os.path.abspath(PATH)):
        for _name_file in name_file:
            if pathlib.Path(path).name.lower() != 'arquivo':
                l_type, _score = __likely_type(path, _name_file)
                list_types_found.append(l_type)
                list_result.append('{0},{1},{2},{3}\n'.format(l_type, str(_score), path, _name_file))
                print(l_type, '>>>', str(_score), '>>>', os.path.join(path, _name_file))

# Contar quantidade de tipos encontrados
def count_types():
    for _type in TYPES:
        print(_type + ':', list_types_found.count(_type))
    print('Total:', len(list_types_found))

# Salvar resultado da categorização
def save_result(name: str):
    __save_file(list_result, name)

# Salvar log dos tipos não definidos
def save_not_named(name: str):
    __save_file(list_undefined, name)

# Possível falha que não entrou
def possible_failure_not_enter(name: str):
    __save_file(list_possible_failure_not_enter, name)

# Possível falha que entrou
def possible_failure_enter(name: str):
    __save_file(list_possible_failure_enter, name)


######### Execução #########
search_by_type_on_pages()
count_types()
save_result('C:\\Users\\savio\\Desktop\\resultado2.txt')
save_not_named('C:\\Users\\savio\\Desktop\\log-teste.txt')
#possible_failure_not_enter('C:\\Users\\savio\\Desktop\\possible_failure_not_enter.txt')
#possible_failure_enter('C:\\Users\\savio\\Desktop\\possible_failure_enter.txt')