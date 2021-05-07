import os
import time

from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from flask_mysqldb import MySQL
from models.models import Usuario, Pet
from dao import PetDao, UsuarioDao

app = Flask(__name__)
app.secret_key = 'projeto_cest'

mysql = MySQL(app)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password"
app.config['MYSQL_DB'] = "petshop"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)
pet_dao = PetDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('lista')))
    return render_template('lista.html', titulo='PETSHOWPPER!', pets=lista)


@app.route("/lista")
def lista():
    return render_template('lista.html', titulo='Sistema Petshop!')


@app.route("/cadastropet")
def cadastros():
    return render_template('cadastropet.html', titulo='Pets cadastrados')


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Cadastrar novo Pet')


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    raca = request.form['raca']
    porte = request.form['porte']
    dono = request.form['dono']
    pet = Pet(nome, raca, porte, dono)
    pet = pet_dao.salvar(pet)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{pet.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    pet = pet_dao.buscar_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Pet', pet=pet
                           , capa_pet=nome_imagem or 'capa_padrao.jpg')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(message=usuario.nome + " logado com sucesso!")
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash(message="Não Logado. Por favor, verifique suas credenciais ou entre em contato com o suporte.")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.route('/cadastropet')
def cadastrapet():
    return render_template('cadastropet.html', titulo='Pets cadastrados no sistema', pets=lista)


if __name__ == '__main__':
    app.run(debug=True)
