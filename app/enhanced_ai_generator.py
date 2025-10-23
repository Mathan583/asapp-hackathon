import json
import random
import re
from datetime import datetime, timedelta
from collections import defaultdict

class EnhancedAIResponseGenerator:
    def __init__(self, responses_file="app/responses.json"):
        with open(responses_file, "r") as f:
            self.responses_data = json.load(f)
        
        # Build intent mapping from the dataset
        self.intent_responses = defaultdict(list)
        self.tone_responses = defaultdict(list)
        self.policy_responses = defaultdict(list)
        
        # Process the dataset
        self._process_dataset()
        
        # Real-world data patterns
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
        
    def _process_dataset(self):
        """Process the responses dataset to build intent, tone, and policy mappings"""
        for entry in self.responses_data:
            intent = entry.get("intent", "General")
            tone = entry.get("tone", "Formal")
            policy = entry.get("policy_reference", "General")
            response = entry.get("bot_response", "")
            
            self.intent_responses[intent].append({
                "response": response,
                "tone": tone,
                "policy": policy
            })
            
            self.tone_responses[tone].append(response)
            self.policy_responses[policy].append(response)
    
    def generate_response(self, intent, user_input, context=None):
        """Generate enhanced dynamic responses using the dataset"""
        user_lower = user_input.lower()
        
        # Map our intents to dataset intents
        dataset_intent = self._map_to_dataset_intent(intent, user_input)
        
        # Get response from dataset or generate dynamic one
        if dataset_intent in self.intent_responses:
            return self._get_dataset_response(dataset_intent, user_input, user_lower)
        else:
            return self._generate_dynamic_response(intent, user_input, user_lower)
    
    def _map_to_dataset_intent(self, intent, user_input):
        """Map our intents to dataset intents"""
        user_lower = user_input.lower()
        
        if intent == "check_status":
            if any(word in user_lower for word in ["status", "on time", "delayed", "departure"]):
                return "Flight Status"
            elif any(word in user_lower for word in ["booking", "reference", "ticket", "confirmation"]):
                return "Flight Status"
            else:
                return "Flight Status"
        elif intent == "book_flight":
            return "Booking"
        elif intent == "cancel_flight":
            # Map to Change Flight since dataset doesn't have Cancellation intent
            return "Change Flight"
        elif intent == "pet_policy":
            return "Pet Travel"
        elif intent == "baggage_policy":
            return "Damaged Bag"
        elif intent == "seat_selection":
            return "Seat Availability"
        elif intent == "fare_inquiry":
            return "Fare Check"
        elif intent == "change_flight":
            return "Change Flight"
        elif intent == "check_in":
            return "General"
        elif intent == "meals":
            return "General"
        elif intent == "wifi":
            return "General"
        else:
            return "General"
    
    def _get_dataset_response(self, dataset_intent, user_input, user_lower):
        """Get response from the dataset with dynamic modifications"""
        available_responses = self.intent_responses[dataset_intent]
        
        if not available_responses:
            return self._generate_dynamic_response("general", user_input, user_lower)
        
        # For cancellation intent, use custom logic instead of dataset
        if dataset_intent == "Change Flight" and any(phrase in user_lower for phrase in ["dont need", "do not need", "no longer need", "not needed", "dont want"]):
            return self._generate_dynamic_response("cancel_flight", user_input, user_lower)
        
        # Select a base response
        base_response = random.choice(available_responses)
        response_text = base_response["response"]
        
        # Enhance with dynamic content
        enhanced_response = self._enhance_response(response_text, user_input, user_lower)
        
        return enhanced_response
    
    def _enhance_response(self, response, user_input, user_lower):
        """Enhance dataset responses with dynamic content"""
        # Extract booking info if present
        booking_info = self._extract_booking_info(user_input)
        
        if booking_info and "flight" in user_lower:
            # Add specific flight details
            flight_number = f"{random.choice(['AA', 'DL', 'UA', 'BA'])}{random.randint(100, 9999)}"
            departure_time = self._generate_realistic_time()
            gate = f"Gate {random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 50)}"
            terminal = f"Terminal {random.randint(1, 5)}"
            status = random.choice(self.statuses)
            
            if "status" in user_lower or "on time" in user_lower:
                if status == "On Time":
                    return f"Great news! Your flight {flight_number} is on time and scheduled to depart at {departure_time} from {gate} in {terminal}."
                elif status == "Delayed":
                    delay_time = random.randint(15, 120)
                    return f"I'm sorry to inform you that flight {flight_number} has been delayed by {delay_time} minutes. The new departure time is {departure_time}."
                else:
                    return f"Your flight {flight_number} status: {status}. Departure: {departure_time} from {gate} in {terminal}."
        
        # Extract destination if mentioned
        destination = self._extract_destination(user_input)
        if destination and "book" in user_lower:
            flight_time = self._generate_realistic_time()
            price = self._generate_dynamic_price(destination)
            airline = random.choice(self.airlines)
            
            return f"Excellent choice! I found a great option for {destination}. {airline} has a flight departing at {flight_time} for ${price}. Would you like me to proceed with this booking?"
        
        # Return enhanced base response
        return self._add_dynamic_elements(response, user_input)
    
    def _add_dynamic_elements(self, response, user_input):
        """Add dynamic elements to base responses"""
        # Add realistic details to generic responses
        if "check" in response.lower() and "status" in response.lower():
            flight_number = f"{random.choice(['AA', 'DL', 'UA', 'BA'])}{random.randint(100, 9999)}"
            return response.replace("your flight", f"flight {flight_number}")
        
        return response
    
    def _generate_dynamic_response(self, intent, user_input, user_lower):
        """Generate completely dynamic responses when dataset doesn't have specific intent"""
        if intent == "check_status":
            return self._generate_flight_status_response(user_input, user_lower)
        elif intent == "book_flight":
            return self._generate_booking_response(user_input, user_lower)
        elif intent == "cancel_flight":
            return self._generate_cancellation_response(user_input, user_lower)
        else:
            return self._generate_general_response(user_input, user_lower)
    
    def _generate_flight_status_response(self, user_input, user_lower):
        """Generate dynamic flight status responses"""
        booking_info = self._extract_booking_info(user_input)
        
        if booking_info:
            # Use the extracted flight number if it looks like a flight number
            if re.match(r'^[A-Z]{2,3}\d{3,4}$', booking_info):
                flight_number = booking_info
            else:
                flight_number = f"{random.choice(['AA', 'DL', 'UA', 'BA'])}{random.randint(100, 9999)}"
            
            departure_time = self._generate_realistic_time()
            arrival_time = self._generate_realistic_time(departure_time)
            gate = f"Gate {random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 50)}"
            terminal = f"Terminal {random.randint(1, 5)}"
            status = random.choice(self.statuses)
            
            if status == "On Time":
                return f"Great news! Your flight {flight_number} is on time and scheduled to depart at {departure_time} from {gate} in {terminal}. Please arrive at the airport 2 hours before departure."
            elif status == "Delayed":
                delay_time = random.randint(15, 120)
                return f"I'm sorry to inform you that flight {flight_number} has been delayed by {delay_time} minutes. The new departure time is {departure_time}. We apologize for any inconvenience."
            elif status == "Boarding":
                return f"Flight {flight_number} is now boarding! Please proceed to {gate} in {terminal}. The flight will depart at {departure_time}."
            else:
                return f"Your flight {flight_number} status: {status}. Departure: {departure_time}, Arrival: {arrival_time} from {gate} in {terminal}."
        else:
            booking_types = ["booking reference", "confirmation number", "ticket number", "PNR"]
            booking_type = random.choice(booking_types)
            return f"I'd be happy to help you check your flight status. To look up your flight details, I'll need your {booking_type}. Could you please provide that information?"
    
    def _generate_booking_response(self, user_input, user_lower):
        """Generate dynamic booking responses"""
        destination = self._extract_destination(user_input)
        
        if destination:
            airline = random.choice(self.airlines)
            flight_time = self._generate_realistic_time()
            price = self._generate_dynamic_price(destination)
            flight_duration = self._generate_flight_duration(destination)
            
            return f"Excellent choice! I found several options for {destination}. {airline} has a flight departing at {flight_time} for ${price}. The flight duration is approximately {flight_duration}. Would you like me to proceed with this booking?"
        else:
            destinations = random.sample(self.airports["cities"], 3)
            return f"I'd be delighted to help you book a flight! Could you please tell me your destination? Popular destinations include {', '.join(destinations)}. Also, what's your preferred travel date?"
    
    def _generate_cancellation_response(self, user_input, user_lower):
        """Generate dynamic cancellation responses"""
        booking_info = self._extract_booking_info(user_input)
        
        # Check if user is declining/not needing a flight
        if any(phrase in user_lower for phrase in ["dont need", "do not need", "no longer need", "not needed", "dont want"]):
            return "I understand you don't need a flight at this time. No problem at all! If you change your mind in the future, I'll be here to help you with bookings, flight status, or any other travel needs. Is there anything else I can assist you with today?"
        
        if booking_info:
            refund_amount = random.randint(200, 800)
            processing_time = random.randint(3, 10)
            cancellation_fee = random.randint(0, 100)
            
            if cancellation_fee == 0:
                return f"I've successfully processed your flight cancellation. You'll receive a full refund of ${refund_amount} within {processing_time} business days. No cancellation fees apply. Is there anything else I can assist you with?"
            else:
                return f"Your flight has been cancelled. The refund amount is ${refund_amount} (after a ${cancellation_fee} cancellation fee). You'll receive the refund within {processing_time} business days."
        else:
            booking_types = ["booking reference", "confirmation number", "ticket number"]
            booking_type = random.choice(booking_types)
            return f"I understand you'd like to cancel your flight. To process your cancellation, I'll need your {booking_type}. Could you please provide that information?"
    
    def _generate_general_response(self, user_input, user_lower):
        """Generate dynamic general responses"""
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
        patterns = [
            r'booking\s+(?:reference|ref|number|id)\s*:?\s*([A-Z0-9]+)',
            r'confirmation\s+(?:number|id)\s*:?\s*([A-Z0-9]+)',
            r'ticket\s+(?:number|id)\s*:?\s*([A-Z0-9]+)',
            r'pnr\s*:?\s*([A-Z0-9]+)',
            r'flight\s+(?:number|no)\s*:?\s*([A-Z0-9]+)',
            r'\b([A-Z]{2,3}\d{3,4})\b',  # Flight number pattern (2-3 letters + 3-4 digits) - matches UA1033
            r'\b([A-Z]{1,3}\d{3,6})\b',  # Alternative flight number pattern
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
