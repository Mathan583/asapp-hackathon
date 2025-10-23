# ASAAP - Airline Smart Assistant AI Platform

A conversational AI chatbot for airline customer service built with FastAPI, Streamlit, and ChromaDB. The system provides intelligent responses to customer queries about flight bookings, cancellations, status checks, and various airline services.

## Features

- **Intelligent Intent Detection**: Recognizes customer intents including booking, cancellation, status checks, pet policies, baggage, seat selection, and more
- **Dynamic Response Generation**: Uses real airline customer service data combined with AI-powered response generation
- **Vector Database Integration**: ChromaDB for semantic search and similarity matching
- **Real-time Information**: Generates realistic flight details, prices, times, and status updates
- **Modern UI**: Streamlit-based chat interface with conversation history

## Quick Start

### Automated Deployment

**Windows:**
```bash
deploy.bat deploy
```

**Linux/Mac:**
```bash
./deploy.sh deploy
```

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database:**
   ```bash
   python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot()"
   ```

3. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **Start the frontend UI (in a new terminal):**
   ```bash
   streamlit run ui/app_ui.py
   ```

5. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs

## Usage

### API Usage

**Chat Endpoint:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "message=Do you allow pets on flights?"
```

**Response:**
```json
{
  "response": "Small cats and dogs are welcome in the cabin if they meet the carrier size requirements and remain inside it during the flight."
}
```

### Deployment Commands

**Windows (deploy.bat):**
```bash
deploy.bat deploy    # Full deployment
deploy.bat start     # Start services only
deploy.bat stop      # Stop all services
deploy.bat restart   # Restart services
deploy.bat status    # Show status
deploy.bat health    # Health check
```

**Linux/Mac (deploy.sh):**
```bash
./deploy.sh deploy    # Full deployment
./deploy.sh start     # Start services only
./deploy.sh stop      # Stop all services
./deploy.sh restart   # Restart services
./deploy.sh status    # Show status
./deploy.sh health    # Health check
```

### Monitoring

**Run system monitoring:**
```bash
python monitor.py --once      # Single health check
python monitor.py            # Continuous monitoring
python monitor.py --interval 30  # Custom interval (30s)
```

## How It Works

The system uses a hybrid approach combining:

1. **Intent Detection**: Keyword-based pattern matching with priority ordering
2. **Response Generation**: Real airline customer service responses (2102+ entries) combined with dynamic AI generation
3. **Vector Search**: SentenceTransformer embeddings stored in ChromaDB for similarity matching

## Project Structure

```
ASAAP/
├── app/
│   ├── main.py                 # FastAPI server
│   ├── chatbot.py              # Main chatbot logic
│   ├── enhanced_ai_generator.py # AI response generator
│   ├── vector_db.py            # ChromaDB integration
│   ├── model_utils.py          # AI model utilities
│   └── responses.json          # Customer service dataset
├── ui/
│   └── app_ui.py               # Streamlit UI
├── data/
│   └── sample_intents.json     # Intent examples
├── deploy.sh / deploy.bat      # Deployment scripts
├── monitor.py                  # Monitoring tool
├── RUNBOOK.md                  # Operational guide
└── requirements.txt            # Dependencies
```

## Supported Intents

- Flight booking and reservations
- Flight cancellation and refunds
- Flight status and tracking
- Pet travel policies
- Baggage policies and claims
- Seat selection and preferences
- Fare inquiries and pricing
- Flight changes and modifications
- Check-in procedures
- Meal options and dietary requirements
- Wi-Fi and onboard services
- Lounge access information
- Loyalty program benefits

## Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for model downloads

## Documentation

For detailed operational procedures, troubleshooting, and maintenance:
- **RUNBOOK.md** - Complete operational guide
- **Deployment Scripts** - Automated setup and management
- **Monitoring Tools** - Health checks and performance tracking

## Testing

**Test individual components:**
```bash
# Test chatbot
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot(); print(bot.get_response('Do you allow cats on flights?'))"

# Test API
curl -X POST "http://127.0.0.1:8000/chat" -d "message=Hello"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please create an issue in this repository.