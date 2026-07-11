# Seção para teste a partir da root:
#//////////////////////////////////////////////////////////////////////////////////
""" import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) """
#//////////////////////////////////////////////////////////////////////////////////

import random
from Sistemas.NPC_names.listaNomesNPC import nomes, sobrenomes
from Classes.NPC import NPC

def gerarNome():
    randomNum = random.randint(0,99)
    if randomNum%2 == 0: # analisando a lista de nomes, existe o padrão dos nomes de índice par serem masculinos e ímpares femininos
        genero = 'M'
    else:
        genero = 'F'
    return (f"{nomes[randomNum]} {random.choice(sobrenomes)}", genero)

def criarNpcs(estacoes, quantidade):
    npcs = []
    for i in range(quantidade):
        random_gerado = gerarNome()
        nome_completo = random_gerado[0]
        genero = random_gerado[1]
        origem = random.choice(estacoes)
        destino = random.choice(estacoes)
        while destino == origem:
            destino = random.choice(estacoes)
        npc = NPC(nome_completo, destino, origem, genero)
        origem.fila.append(npc)
        npcs.append(npc)
    return npcs