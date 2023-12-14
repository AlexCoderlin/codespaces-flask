# app.py
from flask import Flask, render_template, request, Response
import requests
from io import BytesIO
from gzip import GzipFile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/youtube-proxy', methods=['POST'])
def youtube_proxy():
    youtube_url = request.form.get('url')
    
    # Descarga el video de YouTube
    response = requests.get(youtube_url, stream=True)
    
    # Comprime el contenido
    compressed_content = compress_content(response.content)
    
    # Configura la respuesta con el contenido comprimido
    compressed_response = Response(compressed_content)
    compressed_response.headers['Content-Type'] = 'video/mp4'
    compressed_response.headers['Content-Encoding'] = 'gzip'
    
    return compressed_response

def compress_content(content):
    buffer = BytesIO()
    with GzipFile(fileobj=buffer, mode='wb') as f:
        f.write(content)
    return buffer.getvalue()

if __name__ == '__main__':
    app.run(debug=True)
