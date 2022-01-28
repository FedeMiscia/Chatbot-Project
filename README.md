# Chatbot-Project

RASA Workflow

1. Posizionarsi nella directory di progetto
2. Attivare l’ambiente Rasa tramite: conda activate NOME AMBIENTE
3. Ora sono disponibili i comandi RASA (rasa train, rasa shell…)

Per le azioni, fare parallelamente:
1. Nuova finestra di terminale
2. Posizionarsi nella directory di progetto
3. Attivare l’ambiente Rasa tramite: **conda activate NOME AMBIENTE**
4. Fare il train del modello: **rasa train**
5. Attivare il server (su una nuova finestra del terminale): **rasa run actions**
6. Avviare il chatbot: **rasa run** (dopo aver avviato ngrok)

Per la connessione a telegram: **ngrok http 5005** (su una nuova finestra del terminale)
Poi copiare nel file _credentials.yml_ il webhook seguito da: /webhooks/telegram/webhook

In credentials.yml deve essere presente il seguente blocco di codice:
telegram:
  access_token: fornito da both father su telegram
  verify: nome del bot
  webhook_url: quello copiato da ngrok


