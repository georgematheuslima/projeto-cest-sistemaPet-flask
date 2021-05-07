
class Pet:
    def __init__(self,nome, raca, porte, dono, id=None):
        self.nome = nome
        self.raca = raca
        self.porte = porte
        self.dono = dono
        self._id = id


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
