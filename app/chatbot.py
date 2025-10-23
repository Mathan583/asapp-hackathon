import json
import re
from app.model_utils import AirlineModel
from app.vector_db import VectorDB
from app.enhanced_ai_generator import EnhancedAIResponseGenerator

class AirlineChatbot:
    def __init__(self):
        self.model = AirlineModel()
        self.db = VectorDB()
        self.enhanced_ai_generator = EnhancedAIResponseGenerator()

        with open("app/airline_policy.json", "r") as f:
            self.policies = json.load(f)

        # Preload intents into ChromaDB
        import os
        if self.db.collection.count() == 0:  # if empty
            with open("data/sample_intents.json") as f:
                intents = json.load(f)
            for item in intents:
                for ex in item["examples"]:
                    vector = self.model.get_embedding(ex)
                    self.db.insert([vector])
            print("✅ Preloaded intents into ChromaDB!")

    def get_response(self, user_input):
        embedding = self.model.get_embedding(user_input)
        matches = self.db.search([embedding])
        intent = "general"

        # Enhanced keyword-based intent mapping
        user_lower = user_input.lower()
        
        # Check for specific intents first (most specific to least specific)
        
        # Pet policy intent
        if any(word in user_lower for word in ["pet", "cat", "dog", "animal", "pets", "bring my", "allow", "cabin"]):
            intent = "pet_policy"
        # Baggage policy intent
        elif any(word in user_lower for word in ["baggage", "luggage", "bag", "damaged", "broken", "allowance"]):
            intent = "baggage_policy"
        # Seat selection intent
        elif any(word in user_lower for word in ["seat", "window", "aisle", "choose", "select", "preference"]):
            intent = "seat_selection"
        # Fare inquiry intent
        elif any(word in user_lower for word in ["price", "cost", "fare", "expensive", "cheap", "discount", "offer", "how much", "ticket cost", "ticket price"]):
            intent = "fare_inquiry"
        # Change flight intent
        elif any(word in user_lower for word in ["change", "modify", "reschedule", "postpone", "different date"]):
            intent = "change_flight"
        # Check-in intent
        elif any(word in user_lower for word in ["check in", "checkin", "online check", "boarding pass"]):
            intent = "check_in"
        # Meals intent
        elif any(word in user_lower for word in ["meal", "food", "eat", "vegetarian", "dietary", "pre-order"]):
            intent = "meals"
        # Wi-Fi intent
        elif any(word in user_lower for word in ["wifi", "wi-fi", "internet", "online", "connect"]):
            intent = "wifi"
        # Cancellation intent
        elif (any(word in user_lower for word in ["cancel", "cancellation", "refund"]) or
              any(phrase in user_lower for phrase in ["don't need", "do not need", "no longer need", "not needed", "dont need"]) or
              any(phrase in user_lower for phrase in ["cancel the", "cancel my", "want to cancel"])):
            intent = "cancel_flight"
        # Booking intent (but exclude negative cases)
        elif (any(word in user_lower for word in ["book", "reserve", "buy", "purchase"]) or
              (any(phrase in user_lower for phrase in ["get a flight", "need a flight"]) and 
               not any(phrase in user_lower for phrase in ["don't", "dont", "do not", "no longer", "not"]))):
            intent = "book_flight"
        # Flight status intent (more specific patterns)
        elif (any(word in user_lower for word in ["when", "time", "schedule", "departure", "arrival", "status", "my flight", "flight status", "check"]) or
              any(word in user_lower for word in ["booking", "reference", "ticket", "confirmation", "pnr", "flight number"]) or
              re.search(r'\b[A-Z]{2,3}\d{3,4}\b', user_input)):  # Direct flight number detection
            intent = "check_status"
        # General help
        elif any(word in user_lower for word in ["help", "assistance", "support"]):
            intent = "general"

        # Use enhanced AI-powered dynamic response generator with large dataset
        return self.enhanced_ai_generator.generate_response(intent, user_input)
