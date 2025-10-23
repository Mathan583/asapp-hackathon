import json
import random
from datetime import datetime, timedelta

class ResponseGenerator:
    def __init__(self, templates_file="app/response_templates.json"):
        with open(templates_file, "r") as f:
            self.templates = json.load(f)
        
        # Sample data for dynamic responses
        self.sample_flights = {
            "times": ["10:30 AM", "2:30 PM", "6:45 PM", "8:15 AM", "4:20 PM"],
            "destinations": ["Paris", "New York", "London", "Tokyo", "Dubai", "Sydney"],
            "departures": ["New York", "Los Angeles", "Chicago", "Miami", "Seattle"],
            "prices": [299, 450, 380, 520, 340, 280],
            "statuses": ["On Time", "Delayed", "Boarding", "Departed"],
            "booking_refs": ["ABC123", "XYZ789", "DEF456", "GHI012", "JKL345"]
        }
    
    def get_response(self, intent, user_input, context=None):
        """Generate dynamic response based on intent and context"""
        user_lower = user_input.lower()
        
        if intent == "check_status":
            return self._get_status_response(user_input, user_lower)
        elif intent == "book_flight":
            return self._get_booking_response(user_input, user_lower)
        elif intent == "cancel_flight":
            return self._get_cancellation_response(user_input, user_lower)
        else:
            return self._get_general_response(user_input, user_lower)
    
    def _get_status_response(self, user_input, user_lower):
        """Generate flight status response"""
        # Check if user provided booking information
        if any(word in user_lower for word in ["booking", "reference", "ticket", "confirmation", "id", "number"]):
            flight_time = random.choice(self.sample_flights["times"])
            departure = random.choice(self.sample_flights["departures"])
            destination = random.choice(self.sample_flights["destinations"])
            status = random.choice(self.sample_flights["statuses"])
            
            template = self.templates["check_status"]["flight_found"]
            return template.format(
                flight_time=flight_time,
                departure=departure,
                destination=destination,
                status=status
            )
        else:
            return self.templates["check_status"]["no_booking_info"]
    
    def _get_booking_response(self, user_input, user_lower):
        """Generate booking response"""
        # Extract destination if mentioned
        destination = None
        for dest in self.sample_flights["destinations"]:
            if dest.lower() in user_lower:
                destination = dest
                break
        
        if destination:
            flight_time = random.choice(self.sample_flights["times"])
            price = random.choice(self.sample_flights["prices"])
            
            template = self.templates["book_flight"]["with_destination"]
            return template.format(
                destination=destination,
                flight_time=flight_time,
                price=price
            )
        else:
            return self.templates["book_flight"]["no_destination"]
    
    def _get_cancellation_response(self, user_input, user_lower):
        """Generate cancellation response"""
        # Check if user provided booking information
        if any(word in user_lower for word in ["booking", "reference", "ticket", "confirmation", "id", "number"]):
            booking_ref = random.choice(self.sample_flights["booking_refs"])
            refund_amount = random.choice(self.sample_flights["prices"])
            
            template = self.templates["cancel_flight"]["cancellation_confirmed"]
            return template.format(
                booking_ref=booking_ref,
                refund_amount=refund_amount
            )
        else:
            return self.templates["cancel_flight"]["no_booking_info"]
    
    def _get_general_response(self, user_input, user_lower):
        """Generate general response"""
        if any(word in user_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return self.templates["general"]["greeting"]
        elif any(word in user_lower for word in ["help", "assistance", "support"]):
            return self.templates["general"]["help"]
        elif any(word in user_lower for word in ["bye", "goodbye", "thanks", "thank you"]):
            return self.templates["general"]["goodbye"]
        else:
            return self.templates["general"]["unclear"]
    
    def add_context_awareness(self, user_input, conversation_history=None):
        """Add context awareness to responses"""
        if conversation_history:
            # Check if user is continuing a previous conversation
            last_intent = conversation_history.get("last_intent")
            if last_intent == "book_flight" and "yes" in user_input.lower():
                return "Perfect! Your flight has been booked. You'll receive a confirmation email shortly."
            elif last_intent == "cancel_flight" and "yes" in user_input.lower():
                return "Your flight has been cancelled. You'll receive a refund within 5-7 business days."
        
        return None
