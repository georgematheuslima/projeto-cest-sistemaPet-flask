from models.models import Pet, Usuario

SQL_DELETA_PET = 'delete from pet where id = %s'
SQL_PET_POR_ID = 'SELECT id, nome, raca, porte, dono  from pet where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_PET = 'UPDATE pet SET nome=%s, raca=%s, porte=%s, dono=%s, where id = %s'
SQL_BUSCA_PETS = 'SELECT id, nome, raca, porte, dono from pet'
SQL_CRIA_PET = 'INSERT into pet (nome, raca, porte, dono) values (%s, %s, %s, %s)'


class PetDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, pet):
        cursor = self.__db.connection.cursor()

        if pet.id:
            cursor.execute(SQL_ATUALIZA_PET, (pet.nome, pet.raca, pet.porte, pet.dono, pet.id))
        else:
            cursor.execute(SQL_CRIA_PET, (pet.nome, pet.raca, pet.porte, pet.dono))
            pet.id = cursor.lastrowid
        self.__db.connection.commit()
        return pet

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_PETS)
        pets = traduz_pet(cursor.fetchall())
        return pets

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PET_POR_ID, (id,))
        tupla = cursor.fetchall()
        return Pet(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_PET, (id,))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_pet(pets):
    def cria_pet_com_tupla(tupla):
        return Pet(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])

    return list(map(cria_pet_com_tupla, pets))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
