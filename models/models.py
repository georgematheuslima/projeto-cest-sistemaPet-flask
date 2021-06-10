
class Pet:
    def __init__(self,nome, raca, porte, dono, id=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.porte = porte
        self.dono = dono


class Usuario:
    def __init__(self, nome, login, senha, id=None):
        self.id = id
        self.nome = nome
        self.login = login
        self.senha = senha


class Funcionario:
    def __init__(self, nome, cpf, nascimento, telefone, email, cargo, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.telefone = telefone
        self.email = email
        self.cargo = cargo
