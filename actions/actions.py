# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

class ActionFindInfo(Action):

    def name(self) -> Text:
        return "action_find_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = str(tracker.get_slot('country')) #Prendiamo lo slot 'country'
        r = requests.get(url='https://restcountries.com/v3.1/name/{}'.format(name.lower())) #Si prende le richiesta tramite l'url (nell'url aggiungiamo lo slot)
        
        output=''
        # 200 è il codice che dice che è andato tutto bene
        if r.status_code == 200:
            data = r.json() #memorizziamo il json della richiesta
            
            # prendiamo dal json le informazioni che ci servono, effettuiamo il parsing
            flag = list(data[0]['flags'].values())[0]
            capital = list(data[0]['capital'])[0]
            moneta = list(data[0]['currencies'].values())[0]['name']
            area = data[0]['area']
            subregion = data[0]['subregion']
            output = '{} is a state located in {}, the area is {}, the capital is {}, the currency is {} and you can see the flag at this link {}'
        
        else: 
            output = 'something went wrong'
            
        dispatcher.utter_message(text=output)

            
        return []
