from flask import Flask, jsonify, request, render_template_string
import random, json, os

app = Flask(__name__)

FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'animais.json')
TOKEN_ADM = '13245'
SENHA_ADM = '13245'

def carregar_animais():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_animais(lista):
    try:
        with open(FILE_PATH, 'w') as f:
            json.dump(lista, f)
        return True
    except:
        return False

animais = carregar_animais()

@app.route('/')
def home():
    return """
    <html><head><title>API de Animais</title></head>
    <body style="font-family:sans-serif;text-align:center;padding:20px">
        <h1>🐾 API de Animais</h1>
        <p><a href='/animais'>🔁 Animal aleatório</a></p>
        <p><a href='/lista'>📋 Lista completa</a></p>
        <p><a href='/admin'>🔐 Painel Admin</a></p>
    </body></html>
    """

@app.route('/animais')
def animal_aleatorio():
    if not animais:
        return jsonify({"erro": "Nenhum animal disponível"}), 404
    return jsonify({"animal": random.choice(animais)})

@app.route('/lista')
def listar():
    if not animais:
        return jsonify({"erro": "Nenhum animal disponível"}), 404
    formatado = "\n".join(f"- {a}" for a in animais)
    return render_template_string("""
        <h2>Lista de animais</h2>
        <textarea rows='10' cols='40'>{{formatado}}</textarea><br><br>
        <button onclick='copy()'>📋 Copiar</button>
        <script>
            function copy() {
                navigator.clipboard.writeText(document.querySelector('textarea').value);
                alert('Lista copiada!');
            }
        </script>
    """, formatado=formatado)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        token = request.form.get('token')
        senha = request.form.get('senha')
        if token != TOKEN_ADM or senha != SENHA_ADM:
            return "<h3>🚫 Acesso negado</h3>", 403

        novo = request.form.get('novo')
        if novo:
            animais.append(novo)
            salvar_animais(animais)
        return "<h3>✅ Animal adicionado</h3><a href='/admin'>Voltar</a>"

    return '''
    <form method='POST'>
        <h2>Login do Admin</h2>
        Token: <input name='token'><br>
        Senha: <input name='senha' type='password'><br><br>
        Adicionar Animal: <input name='novo'><br>
        <button type='submit'>Salvar</button>
    </form>
    '''