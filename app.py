from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg in ["oi", "menu", "início"]:
        msg.body(
            "👋 Olá! Escolha uma opção digitando o número:\n"
            "1️⃣ Ver produtos\n"
            "2️⃣ Falar com atendente\n"
            "3️⃣ Sair"
        )
    elif incoming_msg in ["1", "produtos"]:
        msg.body(
            "🍕 Temos os seguintes produtos:\n"
            "1. Pizza\n2. Sushi\n3. Hamburguer\n\n"
            "Digite o número do produto para saber mais."
        )
    elif incoming_msg in ["2", "atendente"]:
        msg.body("💬 Um atendente entrará em contato com você em instantes.")
    elif incoming_msg in ["3", "sair"]:
        msg.body("👋 Obrigado por conversar. Até mais!")
    else:
        msg.body("🤔 Desculpe, não entendi. Digite *menu* para ver as opções.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
