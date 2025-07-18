from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os # Importa o módulo os para acessar variáveis de ambiente

app = Flask(__name__)

# Um dicionário simples para armazenar o estado da conversa por usuário.
# ATENÇÃO: Em um ambiente de produção, use um banco de dados (como Firestore)
# para persistir o estado dos usuários, pois este dicionário é volátil
# e será resetado se o servidor reiniciar.
user_states = {} # Ex: {'whatsapp:+5511999999999': 'awaiting_reservation_choice'}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    """
    Função principal que lida com as mensagens recebidas do WhatsApp via Twilio.
    """
    # Obtém o corpo da mensagem recebida, remove espaços em branco e converte para minúsculas
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '') # Formato: 'whatsapp:+5519971117864'

    # Cria um objeto MessagingResponse para construir a resposta TwiML
    resp = MessagingResponse()
    
    # Obtém o estado atual do usuário ou define como 'start' se for a primeira interação
    current_state = user_states.get(from_number, 'start')

    # --- Lógica do Fluxo de Conversa ---

    if current_state == 'start':
        # Esta é a primeira interação ou o fluxo foi reiniciado.
        
        # Tenta obter o nome da pessoa. O WhatsApp não envia o nome diretamente,
        # então 'amigo(a)' é um placeholder. Em um bot real, você poderia pedir o nome
        # ou buscá-lo em um banco de dados se já tiver interagido antes.
        user_name = "amigo(a)" 
        
        # Mensagem 1: Saudação
        msg_text = f"Oi, {user_name}. Tudo bem? 😊\n\n"
        
        # Mensagem 2: Aprovação da inscrição na Juntai
        msg_text += "Aqui é a Julia! Sua inscrição na Juntai foi aprovada 🎉\n"
        msg_text += "Agora é oficial: você está prestes a viver uma noite especial, com pessoas incríveis, boa comida e conexões autênticas 🍽️✨\n"
        msg_text += "Tudo acontece em um ambiente cuidadosamente pensado, com pessoas que combinam com você.\n\n"
        
        # Mensagem 3: Explicação sobre os jantares e a IA
        msg_text += "Nossos jantares acontecem todas as quartas, com grupos de 5 desconhecidos que têm tudo pra se dar bem.\n"
        msg_text += "A mágica acontece com a nossa inteligência artificial, que cruza os interesses de cada pessoa e monta mesas com sintonia real, nem tudo igual, mas com assunto garantido. 🍷✨\n"
        msg_text += "Ah, e o restaurante? É um lugar surpresa. A gente só revela o endereço um dia antes do jantar, pra deixar a experiência ainda mais especial.\n"
        msg_text += "Você gostaria de participar?"

        # Adiciona a mensagem ao objeto de resposta
        message = resp.message(msg_text)
        
        # Adiciona o Botão de Resposta Rápida "Sim, reservar mesa!"
        # Quando este botão é clicado, o texto definido em 'media_url' (neste caso, "SIM_RESERVAR_MESA")
        # é enviado de volta para o seu bot como uma nova mensagem.
        message.quick_reply("Sim, reservar mesa!", media_url="SIM_RESERVAR_MESA")
        
        # Atualiza o estado do usuário para indicar que estamos aguardando a escolha de reserva
        user_states[from_number] = 'awaiting_reservation_choice'

    elif current_state == 'awaiting_reservation_choice' and incoming_msg == 'sim_reservar_mesa':
        # O usuário clicou no botão "Sim, reservar mesa!"
        
        # Mensagem sobre vagas limitadas e planos
        msg_text = "Pra garantir essa experiência, a gente trabalha com vagas limitadas: são só 60 por mês por cidade.\n"
        msg_text += "Pra participar, é só reservar sua mesa. Mas não deixa pra depois, porque elas podem acabar a qualquer momento ⏳🍽️\n"
        msg_text += "A gente tem três tipos de plano:\n"
        msg_text += "🔸 Plano Único: acesso por 1 mês, sem renovação automática.\n"
        msg_text += "🔸 Plano Mensal: renovação todo mês, e você participa enquanto estiver ativo.\n"
        msg_text += "🔸 Plano Trimestral: renovação a cada 3 meses, com um valor mais em conta.\n"
        msg_text += "É só escolher o que faz mais sentido pra você e garantir seu lugar na mesa 🧡"

        message = resp.message(msg_text)
        
        # Adiciona o Botão de Resposta Rápida "Reservar mesa! 🧡"
        # Novamente, 'media_url' define o texto que será enviado ao bot.
        # Explicamos a limitação para botões de URL diretamente clicáveis.
        message.quick_reply("Reservar mesa! 🧡", media_url="RESERVAR_MESA_CTA")
        
        # Atualiza o estado do usuário para aguardar o clique no botão de CTA
        user_states[from_number] = 'awaiting_cta_click'

    elif current_state == 'awaiting_cta_click' and incoming_msg == 'reservar_mesa_cta':
        # O usuário clicou no botão "Reservar mesa! 🧡"
        
        # Mensagem final com o link
        msg_text = "Ótimo! Para reservar sua mesa e escolher seu plano, acesse o link:\n"
        msg_text += "👉 https://juntai.app/\n\n"
        msg_text += "Lembre-se: para ter um botão clicável diretamente no WhatsApp que leva a um site, "
        msg_text += "é necessário usar um 'Message Template' pré-aprovado pelo WhatsApp. "
        msg_text += "Este é um recurso avançado para bots em produção. 😉"
        
        resp.message(msg_text)
        
        # Reseta o estado do usuário para 'start' ou para um estado de 'finalizado'
        user_states[from_number] = 'start'

    else:
        # Resposta padrão para mensagens não esperadas ou para reiniciar o fluxo
        resp.message("Olá! Para começar, digite 'Oi'.")
        user_states[from_number] = 'start' # Garante que o estado seja reiniciado

    # Retorna a resposta TwiML para o Twilio
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    # Obtém a porta do ambiente (útil para o Render) ou usa 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    # Executa o aplicativo Flask.
    # Em um ambiente de produção (como o Render), um servidor WSGI (ex: Gunicorn)
    # seria usado para rodar o aplicativo de forma mais robusta.
    # Para testes locais, você pode rodar este arquivo diretamente.
    app.run(host="0.0.0.0", port=port)