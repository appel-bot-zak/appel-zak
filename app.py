from flask import Flask
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)
load_dotenv()

@app.route('/appel')
def lancer_appel():
    try:
        if os.path.exists("appel.lock"):
            return "⛔ Appel déjà en cours ou déjà lancé."
        
        # Création du fichier lock
        with open("appel.lock", "w") as lock_file:
            lock_file.write("verrouillé")

        # Délai d'attente furtif
        time.sleep(20)

        # Récupère les infos depuis .env
        account_sid = os.getenv("TWILIO_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_NUMBER")
        zak_number = os.getenv("ZAK_NUMBER")

        print("SID:", account_sid)
        print("TOKEN:", auth_token)
        print("FROM:", twilio_number)
        print("TO:", zak_number)

        client = Client(account_sid, auth_token)

        appel = client.calls.create(
            to=zak_number,
            from_=twilio_number,
            twiml='<Response><Say voice="alice" language="fr-FR">Zak, c’est urgent. Rappelle-moi dès que possible.</Say></Response>'
        )

        return f"✅ Appel lancé ! SID : {appel.sid}"

    except Exception as e:
        return f"❌ Erreur : {str(e)}"

    finally:
        if os.path.exists("appel.lock"):
            os.remove("appel.lock")

if __name__ == "__main__":
    app.run()
    