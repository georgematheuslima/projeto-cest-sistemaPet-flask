from projeto.models.models import Funcionario

# FUNCIONARIO
SQL_DELETA_FUNCIONARIO = 'delete from funcionario where id = %s'
SQL_FUNCIONARIO_POR_ID = 'SELECT id, nome, cpf, nascimento, telefone, email, cargo from funcionario where id = %s'
SQL_ATUALIZA_FUNCIONARIO = 'UPDATE funcionario SET nome=%s, cpf=%s, nascimento=%s, telefone=%s, email=%s, cargo=%s, ' \
                           'where id =%s'
SQL_BUSCA_FUNCIONARIOS = 'SELECT id, nome, cpf, nascimento, telefone, email, cargo from funcionario'
SQL_CRIA_FUNCIONARIO = 'INSERT into funcionario ( nome, cpf, nascimento, telefone, email, cargo) ' \
                       'values ( %s, %s, %s, %s, %s, %s)'


class FuncionarioDao:
    def __init__(self, db):
        self.__db = db

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_FUNCIONARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        funcionario = traduz_funcionario(dados) if dados else None
        return funcionario

    def salvar(self, funcionario):
        cursor = self.__db.connection.cursor()

        if funcionario.id:
            cursor.execute(SQL_ATUALIZA_FUNCIONARIO, (funcionario.nome, funcionario.cpf, funcionario.nascimento,
                                                      funcionario.telefone, funcionario.email, funcionario.cargo))
        else:
            cursor.execute(SQL_CRIA_FUNCIONARIO, (funcionario.nome, funcionario.cpf, funcionario.nascimento,
                                                funcionario.telefone, funcionario.email, funcionario.cargo))
            funcionario.id = cursor.lastrowid
        self.__db.connection.commit()
        return funcionario

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_FUNCIONARIO, (id,))
        self.__db.connection.commit()

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_FUNCIONARIOS)
        funcionarios = traduz_funcionario(cursor.fetchall())
        return funcionarios


def traduz_funcionario(funcionarios):
    def cria_funcionario_com_tupla(tupla):
        return Funcionario(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], id=tupla[0])

    return list(map(cria_funcionario_com_tupla,  funcionarios))