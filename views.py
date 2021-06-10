import os
import time
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models.models import Pet, Funcionario
from helpers import deleta_arquivo, recupera_imagem
from projeto.dao.petDao import PetDao
from projeto.dao.usuarioDao import UsuarioDao
from projeto.dao.funcionarioDao import FuncionarioDao
from app import db, app

pet_dao = PetDao(db)
usuario_dao = UsuarioDao(db)
funcionario_dao = FuncionarioDao(db)

# ================================ LOGIN/LOGOUT =========================


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


# ================================ AUTENTICAÇÃO =========================


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(message=usuario.nome + " logado com sucesso!")
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        elif usuario.senha != request.form['senha']:
            flash(message=usuario.nome + " senha incorreta, tente novamente.")
            return redirect(url_for('login'))
    else:
        flash(message="Não Logado. Por favor, verifique suas credenciais ou entre em contato com o suporte.")
        return redirect(url_for('login'))



# ================================ PET ===================================
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('lista')))
    return render_template('lista.html', titulo='PETSHOWPPER!')


@app.route("/lista")
def lista():
        return render_template('lista.html', titulo='Sistema Petshop')


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo_pet.html', titulo='Cadastrar novo Pet')


@app.route('/criarpet', methods=['POST'])
def criarpet():
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
    return redirect(url_for('cadastrapet'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    pet = pet_dao.buscar_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Pet', pet=pet
                           , capa_pet=nome_imagem or 'capa_padrao.jpg')


@app.route('/deletar/<int:id>')
def deletar(id):
    pet_dao.deletar(id)
    flash('Pet foi removido com sucesso!')
    return redirect(url_for('cadastrapet'))


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    raca = request.form['raca']
    porte = request.form['porte']
    dono = request.form['dono']
    pet = Pet(nome, raca, porte, dono, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(pet.id)
    arquivo.save(f'{upload_path}/capa{pet.id}-{timestamp}.jpg')
    pet_dao.salvar(pet)
    return redirect(url_for('cadastrapet'))


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo


@app.route('/cadastrapet')
def cadastrapet():
    lista = pet_dao.listar()
    return render_template('cadastropet.html', titulo='Pets cadastrados', pets=lista)



@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


#========================== USUARIOS =======================

@app.route('/cadastrausuario')
def cadastrausuario():
    lista = usuario_dao.listar()
    return render_template('listausuario.html', titulo='Usuários cadastrados no sistema', usuarios=lista)



#========================= FUNCIONARIOS ====================



@app.route('/novofuncionario')
def novofuncionario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('cadastra_funcionario.html', titulo='Petsystem Cadastro de Funcionários')


@app.route('/cadastrofuncionario')
def cadastrofuncionario():
    lista = funcionario_dao.listar()
    return render_template('lista_funcionarios.html', titulo='Petsystem Cadastro de Funcionários', funcionarios = lista)


@app.route('/deletarfuncionario/<int:id>')
def deletarFuncionario(id):
    funcionario_dao.deletar(id)
    flash('Funcionário foi removido com sucesso!')
    return redirect(url_for('cadastrofuncionario'))


@app.route('/criarfuncionario', methods=['POST', ])
def criarfuncionario():
    nome = request.form['nome']
    cpf = request.form['cpf']
    nascimento = request.form['nascimento']
    telefone = request.form['telefone']
    email = request.form['email']
    cargo = request.form['cargo']
    funcionario = Funcionario(nome, cpf, nascimento, telefone, email, cargo)
    funcionario = funcionario_dao.salvar(funcionario)
    return redirect(url_for('cadastrofuncionario'))