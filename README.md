# Bot de WhatsApp com Python e Twilio

Este projeto é um bot simples de WhatsApp usando Flask + Twilio com botões interativos simulados via mensagens.

## Como usar no Render

1. Crie uma conta em [https://render.com](https://render.com)
2. Faça um fork ou clone deste repositório no GitHub
3. No Render, clique em "New Web Service"
4. Conecte seu repositório e use estas configurações:
   - Build Command: *(deixe em branco)*
   - Start Command: `python app.py`
   - Root Directory: *(raiz do projeto)*
5. Após deploy, você terá uma URL pública. Ex: `https://whatsapp-bot.onrender.com`

## Configurar no Twilio

1. Ative o Sandbox do WhatsApp: https://www.twilio.com/console/sms/whatsapp/sandbox
2. Vá em "WHEN A MESSAGE COMES IN" e cole a URL do Render:
   ```
   https://whatsapp-bot.onrender.com/whatsapp
   ```
3. Teste enviando "oi" para o número de sandbox.

---
Desenvolvido com 💬 por ChatGPT
