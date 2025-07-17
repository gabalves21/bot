from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg in ["oi", "menu", "início"]:
        msg.body("Olá! Escolha uma opção:")
        msg_buttons = msg.button_response()
        msg_buttons.button("Ver produtos", "produtos")
        msg_buttons.button("Falar com atendente", "atendente")
        msg_buttons.button("Sair", "sair")
    elif incoming_msg == "produtos":
        msg.body("Temos os seguintes produtos:\n1. Pizza\n2. Sushi\n3. Hamburguer\n\nDigite o número do produto para saber mais.")
    elif incoming_msg == "atendente":
        msg.body("Um atendente entrará em contato com você em instantes.")
    elif incoming_msg == "sair":
        msg.body("Obrigado por conversar. Até mais!")
    else:
        msg.body("Desculpe, não entendi. Digite *menu* para ver as opções.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
