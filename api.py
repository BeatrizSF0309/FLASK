from flask import Flask, request
from openai import OpenAI


app = Flask(__name__)

VERSION = "v0.0.1"

OPENAI_API_KEY = "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"
OPENAI_ORGANIZATION = "org-Ltwu7N4fgS3VStuVDoFJ0WVF"


def conversation(message):
    client = OpenAI(api_key=OPENAI_API_KEY,
                    organization=OPENAI_ORGANIZATION)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um bot que conversa com o usuário para chegar em um breve diagnóstico sobre sua condição mental."},
                  {"role": "user", "content": message}])

    return completion.choices[0].message.content


def trace_error(type_error, message):
    return {type_error: message}


@app.route('/chat', methods=['POST'])
def get_chat_conversation():
    """
    Requisição: {"message": "Olá, chatbot!"}
    :return: {"chatbot_message": "Olá, usuário!"}
    """
    if request.method == 'POST':
        request_data = request.get_json()
        try:
            message = request_data['message']
            return {"chatbot_message": conversation(str(message))}
        except:
            return trace_error("error", "Mensagem não encontrada! Certifique-se de que esteja utilizando o campo "
                                        "'message'")
    else:
        return trace_error("error", "Método POST requerido.")


@app.route('/version', methods=['GET'])
def version():
    return {"version": VERSION}


if __name__ == '__main__':
    app.run(debug=True)
