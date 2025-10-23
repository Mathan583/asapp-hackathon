import json
import random
from datetime import datetime, timedelta
import re

class AIResponseGenerator:
    def __init__(self):
        # Real-world data patterns for dynamic generation
        self.airports = {
            "major": ["JFK", "LAX", "LHR", "CDG", "NRT", "DXB", "SIN", "HKG"],
            "cities": ["New York", "Los Angeles", "London", "Paris", "Tokyo", "Dubai", "Singapore", "Hong Kong"],
            "countries": ["USA", "UK", "France", "Japan", "UAE", "Singapore", "China"]
        }
        
        self.airlines = ["American Airlines", "Delta", "United", "British Airways", "Air France", "Lufthansa", "Emirates", "Singapore Airlines"]
        
        # Dynamic pricing based on distance and demand
        self.base_prices = {
            "domestic": (200, 600),
            "international": (400, 1200),
            "premium": (800, 2000)
        }
        
        # Flight status patterns
        self.statuses = ["On Time", "Delayed", "Boarding", "Departed", "Arrived", "Cancelled"]
        
    def generate_response(self, intent, user_input, context=None):
        """Generate completely dynamic responses based on intent and context"""
        user_lower = user_input.lower()
        
        if intent == "check_status":
            return self._generate_flight_status_response(user_input, user_lower)
        elif intent == "book_flight":
            return self._generate_booking_response(user_input, user_lower)
        elif intent == "cancel_flight":
            return self._generate_cancellation_response(user_input, user_lower)
        else:
            return self._generate_general_response(user_input, user_lower)
    
    def _generate_flight_status_response(self, user_input, user_lower):
        """Dynamically generate flight status responses"""
        # Extract booking info if present
        booking_info = self._extract_booking_info(user_input)
        
        if booking_info:
            # Generate realistic flight details
            flight_number = f"{random.choice(['AA', 'DL', 'UA', 'BA'])}{random.randint(100, 9999)}"
            departure_time = self._generate_realistic_time()
            arrival_time = self._generate_realistic_time(departure_time)
            gate = f"Gate {random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 50)}"
            terminal = f"Terminal {random.randint(1, 5)}"
            status = random.choice(self.statuses)
            
            # Generate dynamic response based on status
            if status == "On Time":
                response = f"Great news! Your flight {flight_number} is on time and scheduled to depart at {departure_time} from {gate} in {terminal}. Please arrive at the airport 2 hours before departure."
            elif status == "Delayed":
                delay_time = random.randint(15, 120)
                response = f"I'm sorry to inform you that flight {flight_number} has been delayed by {delay_time} minutes. The new departure time is {departure_time}. We apologize for any inconvenience."
            elif status == "Boarding":
                response = f"Flight {flight_number} is now boarding! Please proceed to {gate} in {terminal}. The flight will depart at {departure_time}."
            else:
                response = f"Your flight {flight_number} status: {status}. Departure: {departure_time}, Arrival: {arrival_time} from {gate} in {terminal}."
        else:
            # Generate dynamic request for booking info
            booking_types = ["booking reference", "confirmation number", "ticket number", "PNR"]
            booking_type = random.choice(booking_types)
            
            response = f"I'd be happy to help you check your flight status. To look up your flight details, I'll need your {booking_type}. Could you please provide that information?"
        
        return response
    
    def _generate_booking_response(self, user_input, user_lower):
        """Dynamically generate booking responses"""
        # Extract destination if mentioned
        destination = self._extract_destination(user_input)
        
        if destination:
            # Generate realistic flight options
            airline = random.choice(self.airlines)
            flight_time = self._generate_realistic_time()
            price = self._generate_dynamic_price(destination)
            flight_duration = self._generate_flight_duration(destination)
            
            # Generate dynamic booking response
            response = f"Excellent choice! I found several options for {destination}. {airline} has a flight departing at {flight_time} for ${price}. The flight duration is approximately {flight_duration}. Would you like me to proceed with this booking?"
        else:
            # Generate dynamic request for destination
            destinations = random.sample(self.airports["cities"], 3)
            response = f"I'd be delighted to help you book a flight! Could you please tell me your destination? Popular destinations include {', '.join(destinations)}. Also, what's your preferred travel date?"
        
        return response
    
    def _generate_cancellation_response(self, user_input, user_lower):
        """Dynamically generate cancellation responses"""
        booking_info = self._extract_booking_info(user_input)
        
        if booking_info:
            # Generate realistic cancellation details
            refund_amount = random.randint(200, 800)
            processing_time = random.randint(3, 10)
            cancellation_fee = random.randint(0, 100)
            
            if cancellation_fee == 0:
                response = f"I've successfully processed your flight cancellation. You'll receive a full refund of ${refund_amount} within {processing_time} business days. No cancellation fees apply. Is there anything else I can assist you with?"
            else:
                response = f"Your flight has been cancelled. The refund amount is ${refund_amount} (after a ${cancellation_fee} cancellation fee). You'll receive the refund within {processing_time} business days."
        else:
            # Generate dynamic request for booking info
            booking_types = ["booking reference", "confirmation number", "ticket number"]
            booking_type = random.choice(booking_types)
            
            response = f"I understand you'd like to cancel your flight. To process your cancellation, I'll need your {booking_type}. Could you please provide that information?"
        
        return response
    
    def _generate_general_response(self, user_input, user_lower):
        """Dynamically generate general responses"""
        if any(word in user_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            greetings = ["Hello! Welcome to our airline service.", "Hi there! How can I assist you today?", "Good day! I'm here to help with your travel needs."]
            return random.choice(greetings)
        elif any(word in user_lower for word in ["help", "assistance", "support"]):
            services = ["I can help you with flight bookings, cancellations, and status updates.", "I'm here to assist with your travel needs - bookings, changes, or inquiries.", "I can help you book flights, check status, or handle cancellations."]
            return random.choice(services)
        elif any(word in user_lower for word in ["bye", "goodbye", "thanks", "thank you"]):
            farewells = ["Thank you for choosing our airline! Safe travels!", "You're welcome! Have a wonderful trip!", "Thank you! We look forward to serving you again."]
            return random.choice(farewells)
        else:
            clarifications = ["I'm not sure I understand. Could you please clarify what you need help with?", "I'd be happy to help, but could you provide more details about your request?", "Could you please rephrase your question? I'm here to assist with flight-related inquiries."]
            return random.choice(clarifications)
    
    def _extract_booking_info(self, user_input):
        """Extract booking information from user input"""
        # Look for common booking reference patterns
        patterns = [
            r'booking\s+(?:reference|ref|number|id)\s*:?\s*([A-Z0-9]+)',
            r'confirmation\s+(?:number|id)\s*:?\s*([A-Z0-9]+)',
            r'ticket\s+(?:number|id)\s*:?\s*([A-Z0-9]+)',
            r'pnr\s*:?\s*([A-Z0-9]+)',
            r'flight\s+(?:number|no)\s*:?\s*([A-Z0-9]+)',
            r'([A-Z]{1,3}\d{3,6})',  # Flight number pattern (1-3 letters + 3-6 digits)
            r'([A-Z]{2,3}\d{4,6})',  # Alternative flight number pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _extract_destination(self, user_input):
        """Extract destination from user input"""
        for city in self.airports["cities"]:
            if city.lower() in user_input.lower():
                return city
        return None
    
    def _generate_realistic_time(self, base_time=None):
        """Generate realistic flight times"""
        if base_time:
            # Generate arrival time based on departure
            base_hour = int(base_time.split(':')[0])
            base_minute = int(base_time.split(':')[1].split()[0])
            arrival_hour = (base_hour + random.randint(1, 8)) % 24
            arrival_minute = random.randint(0, 59)
            period = "AM" if arrival_hour < 12 else "PM"
            return f"{arrival_hour % 12 or 12}:{arrival_minute:02d} {period}"
        else:
            hour = random.randint(6, 22)
            minute = random.choice([0, 15, 30, 45])
            period = "AM" if hour < 12 else "PM"
            return f"{hour % 12 or 12}:{minute:02d} {period}"
    
    def _generate_dynamic_price(self, destination):
        """Generate realistic prices based on destination"""
        if destination in ["New York", "Los Angeles"]:
            return random.randint(200, 600)
        elif destination in ["London", "Paris"]:
            return random.randint(400, 800)
        elif destination in ["Tokyo", "Dubai", "Singapore"]:
            return random.randint(600, 1200)
        else:
            return random.randint(300, 900)
    
    def _generate_flight_duration(self, destination):
        """Generate realistic flight durations"""
        durations = {
            "New York": "5h 30m",
            "Los Angeles": "6h 15m", 
            "London": "7h 45m",
            "Paris": "8h 20m",
            "Tokyo": "12h 30m",
            "Dubai": "14h 15m",
            "Singapore": "16h 45m"
        }
        return durations.get(destination, f"{random.randint(4, 16)}h {random.randint(0, 59)}m")
