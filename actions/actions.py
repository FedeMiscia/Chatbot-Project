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
from rasa_sdk.events import AllSlotsReset


class ActionFindInfoCourses(Action):

    def name(self) -> Text:
        return "action_find_info_courses"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = str(tracker.get_slot('corso')) #Nome dello slot da prendere: corso
        corsi = pd.read_excel('datasets/Corsi.xlsx')
        #corsi['Nome'] = corsi['Nome'].str.lower() #Nomi corsi tutti in minuscolo per evitare incongruenze con l'entity
        
        selections = []

        # Creo una lista  con tutti i corsi il cui nome contiene il nome inserito dall'utente
        for index, row in corsi.iterrows():
            if name.lower() == row['Nome'].lower():
                selections.append([row['Nome'],row['Descrizione']])
                break
            elif name.lower() in row['Nome'].lower():
                selections.append([row['Nome'],row['Descrizione']])
                
        
        if len(selections) == 1:
            output = str(selections[0][1])
            dispatcher.utter_message(text=output)  
            return [FollowupAction("utter_another_question")]
        
        elif len(selections) > 1:
            output = "Ho trovato più corrispondenze. Riformula con uno dei seguenti corsi:\n"
            for selection in selections:
                output += ('- '+selection[0]+"\n")
            dispatcher.utter_message(text=output)  
            return [AllSlotsReset()]
            
        elif len(selections) == 0:
            output = "Mmm...non ho capito bene, sei sicuro/a che il nome del corso sia corretto?"
            dispatcher.utter_message(text=output) 
            return [] 

class ActionFindInfoFaculties(Action):

    def name(self) -> Text:
        return "action_find_info_faculties"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = str(tracker.get_slot('facolta')).lower() #Nome dello slot da prendere: facolta
        
        facolta = pd.read_csv('datasets/Facolta_Dipartimento.csv', encoding="ISO-8859-1", sep=";")
        
        facolta['Facolta'] = facolta['Facolta'].str.lower() #Nomi corsi tutti in minuscolo per evitare incongruenze con l'entity

        facolta = facolta[facolta["Facolta"] == name]

        if len(facolta) == 0:
            output = "Non riesco a trovare un risultato, sei sicur* di aver scritto bene?"
        else:
            triennale = facolta[facolta['Laurea']=="Triennale"]
            orientamento_professionale = facolta[facolta['Laurea']=="Orientamento professionale"]
            magistrale = facolta[facolta['Laurea']=="Magistrale"]
            magistrale_cu = facolta[facolta['Laurea'] == "Magistrale a ciclo unico"]
            triennale = triennale.values.tolist()
            orientamento_professionale = orientamento_professionale.values.tolist()
            magistrale = magistrale.values.tolist()
            magistrale_cu = magistrale_cu.values.tolist()
        
        #Creazione dell'output
        output = "Presso la facoltà di {name} vengono erogati i seguenti corsi di laurea:\n".format(name=name)
        output = output +'-- TRIENNALE --\n\n'
        for row in triennale:
            listToStr = ' ('.join([str(elem) for elem in row[2:4]])+')'
            output = output + '\t- ' + listToStr +'\n' 

        output = output + '\n\n-- MAGISTRALE --\n\n'
        for row in magistrale:
            listToStr = ' ('.join([str(elem) for elem in row[2:4]])+')'
            output = output + '\t- ' + listToStr +'\n' 

        if len(magistrale_cu) > 0:
            output = output +'\n\n-- MAGISTRALE A CICLO UNICO --\n\n'
            for row in magistrale_cu:
                listToStr = ' ('.join([str(elem) for elem in row[2:4]])+')'
                output = output + '\t- ' + listToStr +'\n' 

        if len(orientamento_professionale) > 0:
            output = output + '\n\n-- ORIENTAMENTO PROFESSIONALE --\n\n'
            for row in orientamento_professionale:
                listToStr = ' ('.join([str(elem) for elem in row[2:4]])+')'
                output = output + '\t- ' + listToStr +'\n' 
            
        dispatcher.utter_message(text=output)            
        return []

class ActionFindInfoAddresses(Action):

    def name(self) -> Text:
        return "action_find_info_addresses"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        laurea = str(tracker.get_slot('laurea')).lower() #Nome dello slot da prendere: laurea
        name = str(tracker.get_slot('indirizzo')).lower() #Nome dello slot da prendere: indirizzo

        facolta = pd.read_csv('datasets/Facolta_Dipartimento.csv', encoding="UTF-8", sep=";")
        facolta['Nome'] = facolta['Nome'].str.lower()
        facolta = facolta[facolta["Nome"] == name.lower()]
        selected_facolta = facolta[facolta["Laurea"].str.lower() == laurea]

        if(len(facolta) == 0):
            output = "Il corso di laurea che hai inserito non esiste nella nostra università"
        elif (laurea not in ["triennale", "magistrale"]):
            output = "Attenzione, hai inserito una tipologia di laurea che non esiste."
        elif (len(selected_facolta) == 0):
            output = "Non riesco a trovare un risultato, sei sicur* di aver scritto bene?" 
        else:
            descrizione = selected_facolta["Descrizione"].to_list()
            output = str(descrizione[0])
           
        dispatcher.utter_message(text=output)            
        return [AllSlotsReset()]

class ActionFindInfoAula(Action):

    def name(self) -> Text:
        return "action_find_info_aula"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = str(tracker.get_slot('aula')).lower() #Nome dello slot da prendere: aula
        aule = pd.read_excel('datasets/aule.xlsx')
        aule['Aula'] = aule['Aula'].str.lower() #Nomi delle aule tutti in minuscolo
        
        selections = []

        #Lista contenente Polo e piano corrispondenti
        for index, row in aule.iterrows():
            if name in row['Aula']:
                selections.append(("Polo:"+" "+ row['Polo']," " +"Piano:" +" "+ str(row['Piano'])))
                
        
        if len(selections) == 1:
            mystring = ''
            for x in selections[0]:
                mystring += '' + x
            output = mystring
        elif len(selections)== 0:
            output = "Non riesco a trovare un risultato! Prova a scrivere tutto in minuscolo o forse l'aula che stai cercando non esiste!"
           
        dispatcher.utter_message(text=output)            
        return [FollowupAction("utter_more_info")]

class ActionCoursesList(Action):

    def name(self) -> Text:
        return "action_courses_list"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nome_laurea = str(tracker.get_slot('laurea_2'))
        anno = str(tracker.get_slot('anno'))
        semestre = str(tracker.get_slot('semestre'))
        corsi = pd.read_excel('datasets/Corsi.xlsx')
        corsi['Anno'] = corsi['Anno'].astype(str)
        
        if (nome_laurea.casefold() == "triennale"):
            laurea = "IT04"
        elif (nome_laurea.casefold() == "magistrale"):
            laurea = "IM12"
        else:
            laurea = "null"
            
        
        filtrati = corsi['Nome'][(corsi['Corso'] == laurea) & (corsi['Anno'] == anno) & (corsi['Semestre'] == semestre)]
        output = ""
        
        if len(filtrati) != 0:
            output = "Ecco i corsi previsti per Ingegneria Informatica - Automazione " + nome_laurea + ", " + anno + " anno, " + semestre + " semestre: \n"
            for index, row in corsi.iterrows():
                if (row['Corso'] == laurea) & (row['Anno'] == anno) & (row['Semestre'] == semestre):
                    output += ("- " + row['Nome'] + " "+ row['Tipologia'] + "\n")
            
            dispatcher.utter_message(text=output)
            return [FollowupAction("utter_list_courses_type"), AllSlotsReset()]
        else:
            output= "Non trovo nulla con i dati che hai inserito, riprova!"
            
            dispatcher.utter_message(text=output)
            return [FollowupAction("lista_corsi_form"), AllSlotsReset()]
        
        
class ActionChangeRequest(Action):

    def name(self) -> Text:
        return "action_change_request"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
                   
        return [AllSlotsReset()]