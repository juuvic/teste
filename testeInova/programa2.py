from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://user:password@db:1433/usuariosdb?driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(15))
    endereco = db.Column(db.String(200))
    data_cadastro = db.Column(db.String(10))
    ativo = db.Column(db.Boolean)
    salario = db.Column(db.Float)

    def __init__(self, id, nome, idade, email, telefone, endereco, data_cadastro, ativo, salario):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.data_cadastro = data_cadastro
        self.ativo = ativo
        self.salario = salario

@app.route('/json.txt', methods=['POST'])
def salvar_dados():
    data = request.get_json()
    for user in data.get("usuarios", []):
        usuario = Usuario(
            id=user.get('id'),
            nome=user.get('nome'),
            idade=user.get('idade'),
            email=user.get('email'),
            telefone=user.get('telefone'),
            endereco=user.get('endereco'),
            data_cadastro=user.get('data_cadastro'),
            ativo=user.get('ativo'),
            salario=user.get('salario')
        )
        db.session.add(usuario)
    db.session.commit()
    return jsonify({"message": "Dados salvos com sucesso!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
