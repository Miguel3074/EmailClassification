from flask import Flask, request, render_template, jsonify
from groq import Groq

# Inicializa o Flask
app = Flask(__name__)

# Configurações da API do AI
client = Groq(api_key="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")

def classify_email(email_content):
    prompt = f"Analise o seguinte email e classifique-o como 'Produtivo' ou 'Improdutivo'.\n\nEmail: {email_content}\n\nClassificação:"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a classificar emails como produtivos ou improdutivos e deve responder SOMENTE `produtivo` ou `improdutivo`."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    return response.choices[0].message.content

def generate_response(classification, email_content):
    if classification == 'Produtivo':
        prompt = f"Escreva uma resposta profissional para o seguinte email: {email_content}"
    else:
        prompt = "Obrigado pelo contato. Esta mensagem não requer ação imediata."

    response = client.chat.completions.create(
        messages=[ 
            {"role": "system", "content": "Você é um assistente que ajuda a classificar emails como produtivos ou improdutivos."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    email_text = request.form['email'] 

    classification = classify_email(email_text)
    category = 'Produtivo' if classification == 'produtivo' else 'Improdutivo'

    response = generate_response(category, email_text)

    return jsonify({
        'category': category,
        'response': response
    })

# Flask
if __name__ == '__main__':
    app.run(debug=False)