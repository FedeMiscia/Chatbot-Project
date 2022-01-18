# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



import pandas as pd
import json
from pathlib import Path
from typing import Any, Text, Dict, List
import requests
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet



class ActionFindInfoCourses(Action):

    def name(self) -> Text:
        return "action_find_info_courses"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = str(tracker.get_slot('corso')).lower() #Nome dello slot da prendere: corso
        corsi = pd.read_excel('../datasets/Corsi.xlsx')
        corsi['Nome'] = corsi['Nome'].str.lower() #Nomi corsi tutti in minuscolo per evitare incongruenze con l'entity
        
        selections = []

        # Creo una lista  con tutti i corsi il cui nome contiene il nome inserito dall'utente
        for index, row in corsi.iterrows():
            if name in row['Nome']:
                selections.append([row['Nome'],row['Descrizione']])
                
        
        if len(selections) == 1:
            output = str(selections[0][1])
        else:
            # print("Intendevi una delle seguenti?\n")
            #     for selection in selections:
            #         print('- '+selection[0]+"\n")
            output = "Non riesco a trovare un risultato, sei sicur* di aver scritto bene?"
            
        dispatcher.utter_message(text=output)            
        return [FollowupAction("utter_did_that_help")]