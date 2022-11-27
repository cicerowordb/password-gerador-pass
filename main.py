#!/bin/usr/python3
""" GERAR: Facade to password catalogs.
    apt install python3 python3-pip
    pip3 install flask requests mysql-connector-python
    apt install pylint #para checagem de estilo
    pip3 install pytest #para testes unitários
"""

import os
import string
import json
from random import choice, randint
import requests
from flask import Flask
from mysql.connector import errorcode
import mysql.connector

# Section with objects/variables definitions
app = Flask(__name__,
            static_url_path='/static-files',
            static_folder='static-files')

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

# Section with utils functions
def generate_root_content():
    """ Function to render root page """
    response = (open('html/header_content.html', encoding='utf-8').read() +
                open('html/root_content.html', encoding='utf-8').read() +
                open('html/bottom_content.html', encoding='utf-8').read())
    return response

def generate_error_content(message):
    """ Function to render error """
    response = (open('html/header_content.html', encoding='utf-8').read() +
                '<body>\n' +
                '    <center><h2>ERRO</h2></center>\n' +
                '    <font color="#CC0000" size=3>\n' +
                '        &nbsp;' + message + '\n' +
                '    </font><br><br><hr><br>\n' +
                open('html/bottom_content.html', encoding='utf-8').read())
    return response

def generate_message_content(message):
    """ Function to render other messages """
    response = (open('html/header_content.html', encoding='utf-8').read() +
                '<body>\n' +
                '    <center><h1>INFO</h1></center>\n' +
                '    <font size=3>\n' +
                '        &nbsp;' + message + '\n' +
                '    </font><br><br><hr><br>\n' +
                open('html/bottom_content.html', encoding='utf-8').read())
    return response

def generate_list_content(list_registers):
    """ Function to render a list """
    lines = ""
    for item in list_registers:
        line = open('html/list_line_template.html', encoding='utf-8').read()
        line = line.replace("%%NUMBER%%", str(item[0]))
        line = line.replace("%%SERVICE%%", item[1])
        line = line.replace("%%USER%%", item[2])
        line = line.replace("%%PASSWORD%%", item[3])
        lines += line
    response = (open('html/header_content.html', encoding='utf-8').read() +
                open('html/list_top_content.html', encoding='utf-8').read() +
                lines +
                open('html/list_bottom_content.html', encoding='utf-8').read() +
                open('html/bottom_content.html', encoding='utf-8').read())
    return response

def generate_new_password(symbols) -> str:
    """ Function to generate a new password
        Thanks to https://www.pythonforbeginners.com/code-snippets-source-code/
        script-password-generator/
    """
    characters = string.ascii_letters + string.digits + symbols
    password = "".join(choice(characters) for x in range(randint(8, 16)))
    print("Senha calculada")
    return password

def insert_into_database(user, servico, password):
    """ Server function inserir_no_banco """
    config = {
        'host':database_host,
        'user':mysql_user,
        'password':mysql_password,
        'database':mysql_database
    }
    result = [False, "ERRO!", 500]
    try:
        conn = mysql.connector.connect(**config)
        print("Conexao bem sucedida")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ERRO: Nome ou senha do banco incorretas (permissao).")
            result = [False, "ERRO: Nome ou senha do banco incorretas (permissao).", 501]
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("ERRO: Banco não existe no servidor consultado.")
            result = [False, "ERRO: Banco nao existe no servidor consultado.", 502]
        else:
            print("ERRO: não identificado no codigo.")
            print(err)
            result = [False, "ERRO: não identificado no codigo.<br>"+str(err), 503]
    else:
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE dados_logon (id SERIAL PRIMARY KEY, \
                servico VARCHAR(80), user VARCHAR(80), password VARCHAR(80));")
        except mysql.connector.Error as err:
            if err.errno == 1050:
                print("AVISO: Tabela já existe.")
            else:
                print("ERRO: não identificado no código")
                result = [False, "ERRO: não identificado no código.", 504]
                print(err)
        print("Executando insert")
        cursor.execute("INSERT INTO dados_logon (servico, user, password) \
                        VALUES (%s, %s, %s);", (servico, user, password))
        print("Commint no banco")
        conn.commit()
        result = [True, "Dados inseridos com sucesso!", 200]
        cursor.close()
        print("Dados inseridos")
        conn.close()
    return result

# Section with Flask routes
@app.route('/')
def root_server():
    """ Server Root """
    return generate_root_content(), 200

@app.route('/gerar/<service>/<user>')
def gerar(service='', user=''):
    """" Server function gerar """
    if service == '' or user == '':
        message = 'Parâmetros incorretos.'
        return generate_error_content(message), 400
    else:
        password = generate_new_password(pontuacao)
        print("Inserindo no banco")
        database_output = insert_into_database(user, service, password)
        if database_output[0]:
            print("Finalizado procedimento de inserir no banco.")
            return generate_list_content([['---', service, user, password]]), 200
        else:
            print("Erro ao inserir no banco.")
            return generate_error_content(database_output[1]), database_output[2]

@app.route('/listar')
def listar():
    """ Server function listar """
    req_listar = requests.get(f'http://{container_listar}:'
                              f'{listar_pass_port}/listar', timeout=4)
    response_list = json.loads(req_listar.text)
    if response_list[0]:
        return generate_list_content(response_list[1]), response_list[2]
    else:
        return generate_error_content(str(response_list[1])), response_list[2]

@app.route('/atualizar/<servico>/<user>/<password>')
def atualizar(servico='', user='', password=''):
    """ Server function  atualizar """
    if servico == '' or user == '' or password == '':
        print('Parâmetros incorretos.')
        message = 'Parâmetros incorretos.'
        return generate_error_content(message), 400
    else:
        req_atualizar = requests.get(f'http://{container_atualizar}:'
                                     f'{atualizar_pass_port}/atualizar/{servico}'
                                     f'/{user}/{password}', timeout=4)
        response_list = json.loads(req_atualizar.text)
        if response_list[0]:
            return generate_message_content(response_list[1]), response_list[2]
        else:
            return generate_error_content(str(response_list[1])), response_list[2]


# Section with Flask initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=gerador_pass_port, debug=False)
