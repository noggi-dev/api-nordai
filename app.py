from flask import Flask, render_template
from database import criar_tabela
from routes.routes import produtos_bp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# cria tabela ao iniciar
criar_tabela()

# registra o blueprint
app.register_blueprint(produtos_bp)

if __name__ == '__main__':
    app.run(debug=True)