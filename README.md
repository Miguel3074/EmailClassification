# Email Refiner

Este projeto oferece uma solução inteligente para classificar e responder a emails, utilizando a integração com a API do Groq e a extração de texto de arquivos `.txt` ou `.pdf`. A aplicação utiliza o Flask para o back-end e permite que o usuário envie conteúdo de email ou arquivos para análise, e, dependendo da classificação, sugira uma resposta automatizada.

## Funcionalidades

- **Classificação de emails**: A aplicação classifica os emails como "Produtivo" ou "Improdutivo" com base no seu conteúdo.
- **Respostas automáticas**: A partir da classificação, a aplicação sugere uma resposta apropriada para um email produtivo ou envia uma mensagem de agradecimento caso seja improdutivo.
- **Suporte a arquivos**: O usuário pode enviar arquivos `.txt` ou `.pdf` contendo o conteúdo do email.
- **Integração com API de IA**: Utiliza a API do Groq para análise e resposta.

## Tecnologias Usadas

- **Python 3.x**
- **Flask**: Framework web utilizado para o back-end.
- **Groq API**: API de IA para classificação e geração de respostas.
- **PyPDF2**: Biblioteca para extração de texto de arquivos PDF.
- **Werkzeug**: Utilizado para a segurança no envio de arquivos.
- **HTML/CSS**: Estrutura e estilização do front-end.

## Requisitos

- Python 3.x
- Instalar as dependências:

# Como Rodar o Projeto

## Clone o repositório:

### git clone https://github.com/seuusuario/email-refiner.git
### cd email-refiner

## Instale as dependências:

### pip install -r requirements.txt

## Execute a aplicação:

### python app.py

## Acesse a aplicação no navegador através de http://127.0.0.1:5000.