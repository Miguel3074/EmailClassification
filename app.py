import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, jsonify
from groq import Groq
from PyPDF2 import PdfReader 

# Inicializa o Flask
app = Flask(__name__)

# Manager de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Configurações da API do AI
client = Groq(api_key="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")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

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
        prompt = f"Escreva uma resposta profissional para o seguinte email: {email_content}, envie somente a resposta no formato para email"
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

    email_text = request.form.get('email')
    file = request.files.get('file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                email_text = f.read()
        elif filename.lower().endswith('.pdf'):
            email_text = extract_text_from_pdf(file_path)

    if not email_text:
        return jsonify({'error': 'Nenhum conteúdo de email encontrado.'}), 400

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