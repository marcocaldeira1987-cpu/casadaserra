import os
from flask import Flask, render_template, request
import resend

app = Flask(__name__)

# Configuração da chave de API do Resend
resend.api_key = "re_hhxHoD9L_7U4KWye4zcQGteb9QytPombM"

# E-mail onde vais receber os pedidos de reserva
EMAIL_DESTINO = "marcocaldeira1987@gmail.com"

@app.route('/', methods=['GET', 'POST'])
def home():
    mensagem_sucesso = None
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email_cliente = request.form.get('email')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        pessoas = request.form.get('pessoas', 'Não especificado')
        mensagem_cliente = request.form.get('mensagem', '')
        
        # Envio do e-mail de reserva através da API do Resend
        try:
            r = resend.Emails.send({
                "from": "Casa da Serra <onboarding@resend.dev>",
                "to": [EMAIL_DESTINO],
                "reply_to": email_cliente,
                "subject": f"🏔️ Novo Pedido de Reserva: {nome} ({pessoas} pessoas)",
                "html": f"""
                <h3>Novo pedido de reserva recebido no site Casa da Serra!</h3>
                <p><strong>Nome:</strong> {nome}</p>
                <p><strong>Telefone:</strong> {telefone}</p>
                <p><strong>E-mail:</strong> {email_cliente}</p>
                <p><strong>Datas pretendidas:</strong> {checkin} a {checkout}</p>
                <p><strong>Número de hóspedes:</strong> {pessoas}</p>
                <hr>
                <p><strong>Mensagem / Detalhes:</strong></p>
                <p>{mensagem_cliente}</p>
                """
            })
            print(f"E-mail de reserva enviado com sucesso! ID: {r}")
            mensagem_sucesso = f"Obrigado, {nome}! O seu pedido de reserva foi enviado com sucesso. Entraremos em contacto brevemente para confirmar os detalhes."
        except Exception as e:
            print(f"Erro ao enviar e-mail via Resend: {e}")
            mensagem_sucesso = f"Obrigado, {nome}! Os seus dados foram registados e entraremos em contacto brevemente."

    return render_template('index.html', mensagem_sucesso=mensagem_sucesso)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)