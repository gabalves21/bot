from flask import Flask, request
from twilio.rest import Client
import os

app = Flask(__name__)

# Dados do Twilio (definir no Render > Environment)
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
whatsapp_number = "whatsapp:+12028398609"  # Sandbox ou número oficial do Twilio
client = Client(account_sid, auth_token)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    from_number = request.values.get("From")
    user_name = request.values.get("ProfileName", "")

    if incoming_msg in ["oi", "olá", "inicio", "início"]:
        # Mensagem inicial com botões
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=f"Oi, {user_name}! Tudo bem? 😊\n\nEscolha uma das opções abaixo:",
            persistent_action=[
                "reply?text=1",
                "reply?text=2"
            ]
        )

    elif incoming_msg == "1":
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=(
                "Aqui é a Julia! Sua inscrição na Juntai foi aprovada 🎉\n\n"
                "Agora é oficial: você está prestes a viver uma noite especial, com pessoas incríveis, "
                "boa comida e conexões autênticas 🍽️✨\n\n"
                "Tudo acontece em um ambiente cuidadosamente pensado, com pessoas que combinam com você."
            ),
            persistent_action=[
                "reply?text=2"
            ]
        )

    elif incoming_msg == "2":
        # Mensagem explicativa com botão "Reservar"
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=(
                "Nossos jantares acontecem todas as quartas, com grupos de 5 desconhecidos que têm tudo pra se dar bem.\n\n"
                "A mágica acontece com a nossa inteligência artificial, que cruza os interesses de cada pessoa "
                "e monta mesas com sintonia real 🍷✨\n\n"
                "Ah, e o restaurante? É um lugar surpresa. A gente só revela o endereço um dia antes do jantar.\n\n"
                "Você gostaria de participar?"
            ),
            persistent_action=[
                "reply?text=reservar"
            ]
        )

    elif incoming_msg == "reservar":
        # Mensagem final com link clicável
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body=(
                "Pra garantir essa experiência, a gente trabalha com vagas limitadas: são só 60 por mês por cidade.\n\n"
                "Pra participar, é só reservar sua mesa. Mas não deixa pra depois, porque elas podem acabar a qualquer momento ⏳🍽️\n\n"
                "Temos 3 tipos de plano:\n"
                "🔸 Plano Único: 1 mês, sem renovação automática\n"
                "🔸 Plano Mensal: renovação mensal\n"
                "🔸 Plano Trimestral: mais econômico\n\n"
                "👉 *Clique no link para reservar:* https://juntai.app/"
            )
        )

    else:
        # Resposta padrão
        client.messages.create(
            from_=whatsapp_number,
            to=from_number,
            body="Digite *oi* para começar ou escolha uma das opções apresentadas."
        )

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
