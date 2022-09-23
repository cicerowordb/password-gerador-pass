#!/bin/usr/python3
""" GERAR: Facade para o serviço de catálogo de senhas.
apt install python3 python3-pip
pip3 install flask requests mysql-connector-python """

import os
import string
from random import choice, randint
import requests
from flask import Flask
from mysql.connector import errorcode
import mysql.connector

app = Flask(__name__)

container_atualizar = os.getenv('CONTAINER_ATUALIZAR')
container_listar = os.getenv('CONTAINER_LISTAR')
gerador_pass_port = os.getenv('GERADOR_PASS_PORT')
atualizar_pass_port = os.getenv('ATUALIZAR_PASS_PORT')
listar_pass_port = os.getenv('LISTAR_PASS_PORT')
database_host = os.getenv('DATABASE_HOST')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')
pontuacao = os.getenv('PONTUACAO') #'@#$%()[]<>'

output1 = '''<h1>USO:</h1>
<b>/</b> = esta página<br>
<b>/gerar/<servico>/<user></b> = gera uma nova senha para o usuário/serviço<br>
<b>/atualizar/<servico>/<user>/<senha></b> = atualiza uma senha para usuario/servico manualmente<br>
<b>/listar</b> = lista todos os serviços usuários e senhas
'''
output2 = '''<h1>ERRO:</h1>
Algum parâmetro não foi informado corretamente<br><br>'''

output3 = '''<h1>OK:</h1>
Função executada corretamente corretamente<br><br>
<b>User: </b> %%user%%<br>
<b>Serviço: </b> %%servico%%<br>
<b>Password: </b> %%password%%<br>
'''

@app.route('/')
def root_server():
    """ Server Root """
    return output1, 200

@app.route('/gerar/<servico>/<user>')
def gerar(servico='', user=''):
    """" Server function gerar """
    if servico == '' or user == '':
        return output2, 400
    else:
        characters = string.ascii_letters + string.digits + pontuacao
        password = "".join(choice(characters) for x in range(randint(8, 16)))
        print("Senha calculada")
        ## Thanks to https://www.pythonforbeginners.com/code-snippets-
        ## source-code/script-password-generator/
        saida = output3.replace('%%user%%', user)
        saida = saida.replace('%%servico%%', servico)
        saida = saida.replace('%%password%%', password)
        print("Inserindo no banco")
        saida2 = inserir_no_banco(user, servico, password)
        print("Finalizado procedimento de inserir no banco")
        return saida + '<br><br>Resultado do banco: ' + saida2, 200

def inserir_no_banco(user, servico, password):
    """ Server function inserir_no_banco """
    config = {
        'host':database_host,
        'user':mysql_user,
        'password':mysql_password,
        'database':mysql_database
    }
    result = "ERRO"
    try:
        conn = mysql.connector.connect(**config)
        print("Conexao bem sucedida")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERRO: Nome ou senha do banco incorretas (permissao)")
            result = "ERRO: Nome ou senha do banco incorretas (permissao)\n"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERRO: Banco não existe no servidor consultado")
            result = "ERRO: Banco nao existe no servidor consultado\n"
        else:
            print("ERRO: não identificado no codigo\n")
            print(err)
            result = "ERRO: não identificado no codigo\n"
    else:
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE dados_logon (id SERIAL PRIMARY KEY, \
                servico VARCHAR(80), user VARCHAR(80), password VARCHAR(80));")
        except mysql.connector.Error as err:
            if err.errno == 1050:
                print("AVISO: Tabela já existe")
            else:
                print("ERRO: não identificado no código:")
                result = "ERRO: não identificado no código\n"
                print(err)
        print("Executando insert")
        cursor.execute("INSERT INTO dados_logon (servico, user, password) \
                  VALUES (%s, %s, %s);", (servico, user, password))
        print("Commint no banco")
        conn.commit()
        result = "Dados inseridos com sucesso!\n"
        cursor.close()
        print("Dados inseridos")
        conn.close()
    return result

@app.route('/listar')
def listar():
    """ Server function listar """
    req_listar = requests.get('http://' + container_listar + ':' \
                               + listar_pass_port + '/listar')
    return req_listar.text, req_listar.status_code

@app.route('/atualizar/<servico>/<user>/<password>')
def atualizar(servico='', user='', password=''):
    """ Server function  atualizar """
    if servico == '' or user == '' or password == '':
        print("Erro: algum parâmetro faltando")
        return output2, 400
    else:
        req_atualizar = requests.get('http://' + container_atualizar + ':' \
                                      + atualizar_pass_port + '/atualizar/' + servico \
                                      + '/' + user + '/' + password)
        return req_atualizar.text, req_atualizar.status_code

app.run(host='0.0.0.0', port=gerador_pass_port, debug=False)
