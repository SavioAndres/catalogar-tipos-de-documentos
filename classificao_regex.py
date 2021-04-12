import re
import difflib
import os
from unicodedata import normalize
import pathlib

PATH = 'R:\\GERDEPE\\DOCUMENTOS DIGITALIZADOS SEFAZ\\Servidores'

TYPES = [
    "ABONO DE FALTAS",
    "ABONO DE PERMANENCIA",
    "AFASTAMENTO DO CARGO",
    "AFASTAMENTO PARA CONCORRER AO PLEITO ELEITORAL",
    "AFASTAMENTO PARA MANDATO SINDICAL",
    "AFASTAMENTO SEM JUSTIFICATIVA",
    "APOSENTADORIA",
    "APOSENTADORIA POR INVALIDEZ",
    "AVERBACAO DE TEMPO DE SERVICO",
    "CONCESSAO DE FINATE",
    "CONCESSAO DE LICENCA-PREMIO",
    "DIARIAS",
    "FERIAS",
    "GOZO DE LICENCA-PREMIO",
    "INDENIZACAO DE LICENCA-PREMIO",
    "INDENIZACAO DE FERIAS E 13º SALARIO",
    "INDENIZACAO OUTRAS",
    "LICENCA ADOCAO",
    "LICENCA PARA ACOMPANHAMENTO DO CONJUGE",
    "LICENCA MEDICA",
    "LICENCA PARA ACOMPANHAR PESSOA DA FAMILIA",
    "LICENCA PARA EXERCICIO DE MANDATO ELETIVO",
    "LICENCA PARA TRATO DE INTERESSE PARTICULAR",
    "LICENCA PATERNIDADE",
    "MAJORACAO DE LICENCA-PREMIO",
    "OUTROS",
    "PORTARIA CONCESSAO DE LICENCA-PREMIO",
    "PORTARIA CONCESSAO DE LICENCA MEDICA",
    "PORTARIA CUMPRIMENTO",
    "PORTARIA DESIGNACAO",
    "PORTARIA DISPENSA",
    "PORTARIA LOTAR",
    "PORTARIA REMOCAO",
    "PORTARIA OUTRAS",
    "PROGRESSAO POR TITULACAO",
    "INCORPORACAO DE FUNCAO",
]

def count_tipos(list: list):
    for _type in TYPES:
        print(_type + ':', list.count(_type))
    print('Total:', len(list))

def __normalize(word):
    word = normalize('NFKD', word[:-4]).encode('ASCII', 'ignore').decode('ASCII').upper()
    return re.sub(r'[\d\.]+', '', word)

list_undefined = list()

# Pegar provável tipo baseado em uma string
def likely_type(_type, p):
    name = _type
    _type = __normalize(_type)
    likely = difflib.get_close_matches(_type, TYPES, n=1, cutoff=0)
    score = difflib.SequenceMatcher(None, _type, likely[0]).ratio()
    #print(score)
    if score >= 0.3:
        return likely[0]
    else:
        _, file_extension = os.path.splitext(name)
        if file_extension != '.db':
            list_undefined.append(os.path.join(p, name) + '\n')
        return None

ll = list()
for p, _, f in os.walk(os.path.abspath(PATH)):
    for fi in f:
        diry = pathlib.Path(p).name
        if diry.lower() != 'arquivo':
            dd = likely_type(fi, p)
            ll.append(dd)
            print(dd, '>>>>>>', os.path.join(p, fi))

count_tipos(ll)

arquivo = open("C:\\Users\\sasraraujo\\Desktop\log-teste.txt", "a")
arquivo.writelines(list_undefined)