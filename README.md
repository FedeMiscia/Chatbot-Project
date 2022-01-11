# Chatbot-Project

RASA Workflow

1. Posizionarsi nella directory di progetto
2. Attivare l’ambiente Rasa tramite: conda activate NOME AMBIENTE
3. Ora sono disponibili i comandi RASA (rasa train, rasa shell…)

Per le azioni, fare parallelamente:
1. Nuova finestra di terminale
2. Posizionarsi nella directory di progetto
3. Attivare l’ambiente Rasa tramite: conda activate NOME AMBIENTE
4. Attivare il server: rasa run actions

Per la connessione a telegram: ngrok http 5005 
copiare nel file credentials.yml il webhook seguito da:
/webhooks/telegram/webhook

In credentials.yml deve essere presente il seguente blocco di codice:
telegram:
  access_token: fornito da both father su telegram
  verify: nome del bot
  webhook_url: quello copiato da ngrok


