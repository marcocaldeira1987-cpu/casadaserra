import os
from flask import Flask, render_template, request

app = Flask(__name__)

# O teu número de telemóvel para receber as reservas via WhatsApp
TELEFONE_PROPRIETARIO = "351968991834"

@app.route('/', methods=['GET', 'POST'])
def home():
    dados_reserva = None
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email_cliente = request.form.get('email')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        pessoas = request.form.get('pessoas', 'Não especificado')
        mensagem_cliente = request.form.get('mensagem', 'Nenhuma')
        
        # Criar a mensagem detalhada para enviar por WhatsApp
        texto_whatsapp = (
            f"🏔️ *Novo Pedido de Reserva - Casa da Serra*\n\n"
            f"👤 *Nome:* {nome}\n"
            f"📱 *Telefone:* {telefone}\n"
            f"✉️ *E-mail:* {email_cliente}\n"
            f"📅 *Check-in:* {checkin}\n"
            f"📅 *Check-out:* {checkout}\n"
            f"👥 *Hóspedes:* {pessoas}\n"
            f"💬 *Detalhes:* {mensagem_cliente}"
        )
        
        # Gerar o link direto para o WhatsApp
        import urllib.parse
        whatsapp_url = f"https://wa.me/{TELEFONE_PROPRIETARIO}?text={urllib.parse.quote(texto_whatsapp)}"
        
        dados_reserva = {
            'nome': nome,
            'whatsapp_url': whatsapp_url
        }

    return render_template('index.html', dados_reserva=dados_reserva)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)