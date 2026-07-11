from random import randint

class NPC:
    def __init__(self, nome, destino, origem, genero, idade=randint(18,80)):
        self.nome = nome
        self.destino = destino
        self.origem = origem
        self.genero = genero
        self.backstory = ''
        self.idade = idade

    def __repr__(self):
        return f"{self.nome} ({self.origem.nome}->{self.destino.nome})"