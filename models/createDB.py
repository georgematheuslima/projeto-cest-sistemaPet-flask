import MySQLdb

conn = MySQLdb.connect(user='root',
                       database='petshop',
                       passwd='password',
                       host='localhost',
                       port=3306)

#conn.cursor().execute("DROP DATABASE IF EXISTS `petshop`;")                     # CASO DÊ ERRO RELACIONADO A DATABASE EXISTS
# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `petshop`;")
#conn.commit()


criar_tabelas = '''CREATE DATABASE `petshop` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
    USE `petshop`;
    CREATE TABLE `pet` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `raca` varchar(40) NOT NULL,
      `porte` varchar(20) NOT NULL,
      `dono` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) NOT NULL,
      `nome` varchar(20) NOT NULL,
      `senha` varchar(8) NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;'''

conn.cursor().execute(criar_tabelas)

cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO petshop.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('george', 'George Matheus', '123'),
            ('admin', 'Administrador', 'teste'),

      ])

cursor.execute('select * from petshop.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])


cursor.executemany(
      'INSERT INTO petshop.pet (nome, raca, porte, dono) VALUES (%s, %s, %s, %s)',
      [
            ('Tobias Bob', 'Poodle', 'pequeno', 'George'),
            ('Rex', 'RND', 'medio', 'Bruno'),
            ('Duda', 'Poodle', 'pequeno', 'Andrea'),

      ])

cursor.execute('select * from petshop.pet')
print(' -------------  Pets:  -------------')
for pet in cursor.fetchall():
    print(pet[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()