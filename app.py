from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# Variáveis de ambiente configuradas no Render
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")  # Ex: whatsapp:+12028398609

client = Client(account_sid, auth_token)


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower().strip()
    from_number = request.values.get("From")
    user_name = request.values.get("ProfileName", "")

    # Opções do menu
    if incoming_msg in ["oi", "olá", "inicio", "início"]:
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=(
                f"Oi, {user_name}! Tudo bem? 😊\n\n"
                "Escolha uma das opções abaixo e responda com o número:\n"
                "1️⃣ Saber mais sobre a Juntai\n"
                "2️⃣ Reservar uma mesa"
            )
        )

    elif incoming_msg == "1":
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=(
                "Aqui é a Julia! Sua inscrição na Juntai foi aprovada 🎉\n\n"
                "Agora é oficial: você está prestes a viver uma noite especial, com pessoas incríveis, "
                "boa comida e conexões autênticas 🍽️✨\n\n"
                "Tudo acontece em um ambiente cuidadosamente pensado, com pessoas que combinam com você.\n\n"
                "Digite *2* para reservar sua mesa."
            )
        )

    elif incoming_msg == "2":
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=(
                "Nossos jantares acontecem todas as quartas, com grupos de 5 desconhecidos que têm tudo pra se dar bem.\n\n"
                "A mágica acontece com a nossa inteligência artificial, que cruza os interesses de cada pessoa "
                "e monta mesas com sintonia real 🍷✨\n\n"
                "👉 *Clique no link para reservar:* https://juntai.app/"
            )
        )

    else:
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body="Não entendi 😅\n\nDigite *oi* para começar."
        )

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
