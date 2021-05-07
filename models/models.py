
class Pet:
    def __init__(self,nome, raca, porte, dono, id=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.porte = porte
        self.dono = dono



class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
