from flask import Flask, jsonify, request
import numpy as np
from quantum import QRegister, H, I, U
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def is_constant(f, n):
    q = QRegister(n + 1, '0' * n + '1')
    q.apply(H ** (n + 1))
    q.apply(U(f, n))
    q.apply(H ** n @ I)

    return q.measure()[:~0] == '0' * n

def f1(x):
    return x

def f2(x):
    return 1

def f3(x, y):
    return x ^ y

#A PARTIR DAQUI NÃO FUNCIONA O CUSTOM, POIS PARA SER DINÂMICO PRECISA DE UTILIZAR O SPREAD
#GERANDO UM VALOR DE ARGUMENTOS (??) ASSIM NÃO DÁ PARA UTILIZAR A FUNÇÃO VERIFICA CONSTANCIA QUE 
#PEDE UM VALOR FIXO

# MESMO PASSANDO UMA LIST PARA VALORES, A FUNÇÃO SEMPRE RETORNARÁ BALANCEADA, POIS DEPENDERA DO VALOR 
# QUE O USER INFORMAR E NÃO DA CONSTANCIA DA FUNÇÃO EM SÍ
def custom(operacoes, **valores):
    return 0

def gerarParametrosFuncao(valores):
    print(valores)
    return verificaConstancia(custom, 2)
#____________________________________________________________________________________

def verificaConstancia(funcao, numero):
    if is_constant(funcao, numero):
        resp = 'constante'
    else:
        resp = 'balanceada'
    return resp


@app.route('/deutch', methods=["POST", "GET"])
def deutch():
    resp = 'funcao nao encontrada'
    if request.args.get('funcao') == "funcao 1":
        resp = verificaConstancia(f1, 1)
    if request.args.get('funcao') == "funcao 2":
        resp = verificaConstancia(f2, 1)
    if request.args.get('funcao') == "funcao 3":
        resp = verificaConstancia(f3, 2)    
    if request.args.get('funcao') == "custom":    
        content = request.get_json(force=True)
        resp = gerarParametrosFuncao(content["dataEnviar"])

    return {'result': resp, 'funcao': request.args.get('funcao')}

if __name__ == '__main__':
    app.run(port = '5002')
