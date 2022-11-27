import sys
import os
import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import main

def test_unit1__root_content():
    assert main.generate_root_content() == (open('html/header_content.html', encoding='utf-8').read() + open('html/root_content.html', encoding='utf-8').read() + open('html/bottom_content.html', encoding='utf-8').read())

def test_unit2__error_message():
    message = "test message"
    response = (open('html/header_content.html', encoding='utf-8').read() +
                '<body>\n' +
                '    <center><h2>ERRO</h2></center>\n' +
                '    <font color="#CC0000" size=3>\n' +
                '        &nbsp;' + message + '\n' +
                '    </font><br><br><hr><br>\n' +
                open('html/bottom_content.html', encoding='utf-8').read())
    assert main.generate_error_content(message) == response

def test_unit3__info_message():
    message = "test message"
    response = (open('html/header_content.html', encoding='utf-8').read() +
            '<body>\n' +
            '    <center><h1>INFO</h1></center>\n' +
            '    <font size=3>\n' +
            '        &nbsp;' + message + '\n' +
            '    </font><br><br><hr><br>\n' +
            open('html/bottom_content.html', encoding='utf-8').read())
    assert main.generate_message_content(message) == response

def test_unit4__password_length():
    pontuacao = '@#$%()[]<>'
    password = main.generate_new_password(pontuacao)
    assert len(password) >=8 and len(password) <= 16
