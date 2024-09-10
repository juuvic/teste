from flask import Flask, request, jsonify  
import re
from datetime import datetime
from email_validator import validate_email, EmailNotValidError 

app = Flask(__name__)

def clean_data(data): 
    cleaned_data = []
    for user in data.get("usuarios", []):
        # Limpando ID
        try:
            user['id'] = int(user['id'])
        except (ValueError, TypeError):
            user['id'] = None
        
        # Limpando nome
        user['nome'] = user['nome'].strip() if user['nome'] else None
        
        # Limpando idade
        try:
            user['idade'] = int(user['idade'])
            if user['idade'] < 0: user['idade'] = None
        except (ValueError, TypeError):
            user['idade'] = None
        
        # Validando email usando email_validator
        try:
            valid = validate_email(user['email'])
            user['email'] = valid.email  # Captura o email validado
        except EmailNotValidError:
            user['email'] = None
        
        # Limpando telefone
        phone = re.sub(r'\D', '', user.get('telefone', ''))
        user['telefone'] = phone if len(phone) == 11 else None
        
        # Validando data de cadastro
        try:
            user['data_cadastro'] = datetime.strptime(user['data_cadastro'], '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            user['data_cadastro'] = None
        
        # Convertendo "ativo" para booleano
        user['ativo'] = user['ativo'] in ['yes', 'Y', 'true', '1', 'sim', 1]
        
        # Limpando salário
        try:
            user['salario'] = float(user['salario'])
        except (ValueError, TypeError):
            user['salario'] = None
        
        cleaned_data.append(user)
    
    return {"usuarios": cleaned_data}

@app.route('/limpar', methods=['POST'])
def limpar_dados():
    data = request.get_json()
    cleaned_data = clean_data(data)
    return jsonify(cleaned_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
