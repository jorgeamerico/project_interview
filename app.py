#!/usr/local/bin/python3

import redis
from flask import Flask, request, json, Response, render_template

app = Flask(__name__)
things = redis.Redis(host = 'localhost', port = 6379, db=0, charset="utf-8", decode_responses=True)

#LISTA O QUE TA EM MEMORIA NO INDEX
@app.route('/')
def index():
    list=things.lrange('queue', 0, -1)                                  #LISTAGEM
    return render_template("index.html", list=list)

@app.route('/api/queue/pop', methods=["POST"])
def popQueue():
    if things.llen('queue') > 0:                                        #VALIDA SE HA FILA
        msg=things.lindex('queue', 0)                                   #PRIMEIRA COISA DA FILA
        things.lpop('queue')                                            #REMOVE COISA 0

        dados = {
            'status'  : '200',
            'message' :  msg + ' REMOVED'                               #TXT TRATADO
        }
        js = json.dumps(dados)
        resp = Response(js, status=200, mimetype='application/json')
    else:                                                               #NAO HAVENDO FILA
        dados = {
            'message' : 'SEM COISAS NA FILA',
            'status'  : 500
        }
        js = json.dumps(dados)                                          #GERA MSG
        resp = Response(js, status=500, mimetype='application/json')    #TRATA MSG

    return resp                                                         #ESCREVE MSG

@app.route('/api/queue/push', methods=["POST"])
def pushQueue():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json()
        val = content['thing']                                          #VARIAVEL PARA ADICAO
        things.rpush('queue', val)                                      #ADICAO A FILA

        dados = {
            'OK '  : val + ' ADD'
        }
        js = json.dumps(dados)

        resp = Response(js, status=200, mimetype='application/json')
    else:
        dados = {                                                       #NAO CONSEGUI TRATAR ERROS
        'status'  : '404',
        'message' : 'FALHA DE SINTAXE'
        }
        js = json.dumps(dados)

        resp = Response(js, status=404, mimetype='application/json')
    return resp

@app.route('/api/queue/count', methods=["GET"])
def countQueue():
    count=things.llen('queue')                                          #CONTA COISAS
    dados = {
            'TOTAL DE COISAS: ' : count
    }
    js = json.dumps(dados)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

#LIMPA MEMORIA DE COISAS
@app.route('/clear')
def clear():
    length=things.llen('queue')                                         #TAMANHO DA FILA
    if length>0:                                                        #VALIDA SE TEM FILA
        for i in range(length):
            things.blpop('queue')                                       #ESTOURO
    list=things.lrange('queue', 0, -1)
    return render_template("index.html", list=list)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)