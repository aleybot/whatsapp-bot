from flask import Flask, request
import requests

app = Flask(_name_)

VERIFY_TOKEN = "212man"  # Puedes inventarlo, lo usarás al conectar el Webhook
ACCESS_TOKEN = "EAAVh4aTwXwsBO7gdlgCnMxLZCd34vZBs35r56uY5eaJZA3Od9BHLtjZBKqzCv0YwafZCoxhPD22EelVuHlSBTTDL40tOUA8oecTEsM2Y60NBbuog1INEGQFEwzJwfgKNoa4oFVrplszQggv3V78JUA37PFAfI6uyNXGdiDn8zYzXqQAoXIpwZCQN9hBEXW3str7oMSFDwFZBCw37g335wCHS5R4bcaqkqe4"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Token de verificación inválido", 403

    data = request.get_json()
    print("Mensaje recibido:", data)

    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = message['from']
        msg_text = message['text']['body']

        # Respuesta automática
        respuesta = f"Hola! Recibí tu mensaje: '{msg_text}'"
        enviar_respuesta(from_number, respuesta)

    except Exception as e:
        print("Error al procesar mensaje:", e)

    return "ok", 200

def enviar_respuesta(numero, texto):
    url = "https://graph.facebook.com/v19.0/644162355454407/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    r = requests.post(url, headers=headers, json=body)
    print("Respuesta enviada:", r.status_code, r.text)

if _name_ == '_main_':
    app.run(port=5000)