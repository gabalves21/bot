from flask import Flask, request
from twilio.rest import Client
import requests
import os

app = Flask(__name__)

@app.route("/pagamento", methods=["POST"])
def pagamento():
    data = request.get_json()
    if not data:
        return "No data", 400

    if data.get("type") == "payment":
        pagamento_id = data["data"].get("id")
        if not pagamento_id:
            return "Invalid data", 400

        # Consulta o pagamento na API do Mercado Pago
        headers = {
            "Authorization": f"Bearer {os.environ['MP_ACCESS_TOKEN']}"
        }

        response = requests.get(
            f"https://api.mercadopago.com/v1/payments/{pagamento_id}",
            headers=headers
        )

        if response.status_code != 200:
            return "Failed to fetch payment", 500

        pagamento_info = response.json()
        status = pagamento_info.get("status")

        if status == "approved":
            telefone = pagamento_info.get("metadata", {}).get("telefone")
            nome = pagamento_info.get("payer", {}).get("first_name", "Participante")

            if telefone:
                # Envia mensagem no WhatsApp via Twilio
                twilio_sid = os.environ["TWILIO_SID"]
                twilio_token = os.environ["TWILIO_AUTH_TOKEN"]
                twilio_number = os.environ["TWILIO_WHATSAPP_NUMBER"]

                client = Client(twilio_sid, twilio_token)

                mensagem = (
                    f"Olá, {nome}! 👋\n\n"
                    f"Pagamento confirmado ✅\n\n"
                    f"Seu jantar será na *quarta-feira às 20h*.\n"
                    f"O local será revelado um dia antes para manter a surpresa! 🍽️✨"
                )

                client.messages.create(
                    from_=f"whatsapp:{twilio_number}",
                    to=f"whatsapp:{telefone}",
                    body=mensagem
                )

        return "OK", 200

    return "Ignored", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
