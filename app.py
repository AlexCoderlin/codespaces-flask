from flask import Flask, request, render_template, Response
import requests
from bs4 import BeautifulSoup
import zlib

app = Flask(__name__)

def compress(content):
    return zlib.compress(content.encode('utf-8'), level=zlib.Z_BEST_COMPRESSION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy', methods=['POST'])
def proxy():
    url = request.form['url']

    # Realiza la solicitud a la URL proporcionada
    response = requests.get(url)

    # Comprueba si la respuesta ya está comprimida
    if 'Content-Encoding' in response.headers and 'gzip' in response.headers['Content-Encoding']:
        return Response(response.content, content_type=response.headers['Content-Type'])

    # Comprime el contenido de la página
    compressed_content = compress(response.text)

    # Renderiza la página utilizando BeautifulSoup para optimizarla
    soup = BeautifulSoup(response.text, 'html.parser')

    # Puedes aplicar diversas optimizaciones aquí según tus necesidades

    optimized_content = str(soup)

    # Devuelve la página comprimida y optimizada al cliente
    return Response(compressed_content, content_type='text/html; charset=utf-8', headers={'Content-Encoding': 'gzip'})

if __name__ == '__main__':
    app.run(debug=True)
