from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    user_name = request.values.get("ProfileName", "tudo bem")  # nome da pessoa no WhatsApp
    resp = MessagingResponse()

    if incoming_msg in ["oi", "olá", "início"]:
        msg = resp.message(f"Oi, {user_name}! Tudo bem? 😊")
        return str(resp)

    elif incoming_msg == "1":
        msg = resp.message()
        msg.body(
            "Aqui é a Julia! Sua inscrição na Juntai foi aprovada 🎉\n\n"
            "Agora é oficial: você está prestes a viver uma noite especial, com pessoas incríveis, boa comida e conexões autênticas 🍽️✨\n\n"
            "Tudo acontece em um ambiente cuidadosamente pensado, com pessoas que combinam com você."
        )
        return str(resp)

    elif incoming_msg == "2":
        msg = resp.message()
        msg.body(
            "Nossos jantares acontecem todas as quartas, com grupos de 5 desconhecidos que têm tudo pra se dar bem.\n\n"
            "A mágica acontece com a nossa inteligência artificial, que cruza os interesses de cada pessoa e monta mesas com sintonia real 🍷✨\n\n"
            "Ah, e o restaurante? É um lugar surpresa. A gente só revela o endereço um dia antes do jantar.\n\n"
            "Você gostaria de participar?"
        )
        msg_buttons = msg.button_response()
        msg_buttons.button("Sim, reservar mesa!", "reservar")
        return str(resp)

    elif incoming_msg == "reservar":
        msg = resp.message()
        msg.body(
            "Pra garantir essa experiência, a gente trabalha com vagas limitadas: são só 60 por mês por cidade.\n\n"
            "Pra participar, é só reservar sua mesa. Mas não deixa pra depois, porque elas podem acabar a qualquer momento ⏳🍽️\n\n"
            "Temos 3 tipos de plano:\n"
            "🔸 Plano Único: 1 mês, sem renovação automática\n"
            "🔸 Plano Mensal: renovação mensal\n"
            "🔸 Plano Trimestral: mais econômico\n\n"
            "Escolha o que faz sentido e garanta seu lugar 🧡"
        )
        msg_buttons = msg.button_response()
        msg_buttons.button("Reservar mesa! 🧡", "https://juntai.app/")
        return str(resp)

    else:
        msg = resp.message("Digite *oi* para começar ou *1* para continuar.")
        return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
