from projeto.models.models import Usuario

# USUARIO
SQL_DELETA_USUARIO = 'delete from usuario where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, login, senha from usuario where id = %s'
SQL_USUARIO_POR_LOGIN = 'SELECT login  from usuario where id = %s'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET nome=%s, login=%s,senha=%s, where id = %s'
SQL_BUSCA_USUARIO = 'SELECT id, nome, login from usuario'
SQL_CRIA_USUARIO = 'INSERT into usuario (id, nome, senha) values (%s, %s, %s)'


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def busca_por_login(self, login):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_LOGIN, (login,))
        dados = cursor.fetchone()
        login = traduz_usuario(dados) if dados else None
        return login

    def salva(self, usuario):
        cursor = self.__db.connection.cursor()

        if usuario.id:
            cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.nome, usuario.senha, usuario.id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario.nome, usuario.login, usuario.senha))
            usuario.id = cursor.lastrowid
        self.__db.connection.commit()
        return usuario

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIO)
        usuarios = traduz_usuario(cursor.fetchall())
        return usuarios



def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])
