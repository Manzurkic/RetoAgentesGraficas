from flask import Flask
from flask import request
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def fun():
    if request.method == 'GET':
        print('GET: http://localhost:8080/')
        return "Hola caca"

    if request.method == 'POST':
        print('POST: http://localhost:8080/')
        json = request.json
        print(json)
        return json


puerto = 8080

try:
    print(f'Servidor en línea en el {puerto}')
    serve(app, port=puerto)


except Exception as e:
    print(e)
