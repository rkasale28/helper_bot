# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

centers={
    "mumbai":"Yashwant Natya Mandir, Matunga Road",
    "pune": "Balgandharva Natya Mandir, Shivaji Nagar",
    "thane": "Dr. Kashinath Ghanekar Natyagruha, Ghodbunder Rd",
    "navi mumbai": "Vishnudas Bhave Natyagruha, Vashi"
}

commodities={
    "utensils": True,
    "clothes": True,
    "readymade food packets": True,
    "school supplies": True
}

class ActionShowCenter(Action):

    def name(self) -> Text:
        return "action_show_center"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city=tracker.get_slot("city")
        center=centers.get(city)

        if center is None:
            output = "Sorry...! We don't have center in {}. But, we will definitely try to build a center there.".format(city)
        else:
            output = "Our center in {} is at {}".format(city,center)

        dispatcher.utter_message(text=output)

        return []

class ActionShowRequirements(Action):

    def name(self) -> Text:
        return "action_show_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        required=[k for k,v in commodities.items() if v=True]

        output=''

        for i in required:
            output+=i+"<br>"

        dispatcher.utter_message(text=output)

        return []

class ActionShowCommodity(Action):

    def name(self) -> Text:
        return "action_show_requirements_commodity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        commodity=tracker.get_slot("commodiy")
        result=commodities.get(commodity)

        if result is None or not result:
            output = "No. Thank you for asking, but {} is not required".format(commodity)
        else:
            output = "Yes. {} is required. You can donate it at a center in your city".format(commodity)

        dispatcher.utter_message(text=output)

        return []
