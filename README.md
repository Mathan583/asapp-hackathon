# ✈️ ASAAP - Airline Smart Assistant AI Platform

A sophisticated AI-powered airline chatbot built with FastAPI, Streamlit, and ChromaDB that provides intelligent responses to customer queries about flight bookings, cancellations, status checks, and various airline services.

## 🚀 Features

### Core Functionality
- **Intelligent Intent Detection**: Recognizes 10+ different customer intents including booking, cancellation, status checks, pet policies, and more
- **Dynamic Response Generation**: Uses a hybrid approach combining real airline customer service data (2102+ responses) with AI-powered dynamic generation
- **Vector Database Integration**: ChromaDB for semantic search and similarity matching
- **Real-time Flight Information**: Generates realistic flight details, prices, times, and status updates
- **Professional UI**: Modern Streamlit-based chat interface with conversation history

### Supported Intents
- 🎫 **Flight Booking**: Book flights with dynamic pricing and availability
- ❌ **Flight Cancellation**: Cancel flights with refund information
- 📊 **Flight Status**: Check flight status with real-time updates
- 🐕 **Pet Policy**: Information about pet travel policies
- 🧳 **Baggage Policy**: Baggage allowance and damaged bag claims
- 💺 **Seat Selection**: Seat preferences and availability
- 💰 **Fare Inquiry**: Pricing information and discounts
- 🔄 **Flight Changes**: Modify or reschedule existing bookings
- 🍽️ **Meals**: In-flight meal options and dietary requirements
- 📶 **Wi-Fi**: Onboard internet services
- 🏢 **Lounge Access**: Airport lounge information
- 👥 **Loyalty Program**: Frequent flyer benefits

## 🏗️ Architecture

### Backend (FastAPI)
- **Main API**: `app/main.py` - FastAPI server with chat endpoint
- **Chatbot Core**: `app/chatbot.py` - Main chatbot logic and intent detection
- **AI Response Generator**: `app/enhanced_ai_generator.py` - Dynamic response generation
- **Vector Database**: `app/vector_db.py` - ChromaDB integration
- **Model Utils**: `app/model_utils.py` - AI model utilities

### Frontend (Streamlit)
- **UI**: `ui/app_ui.py` - Modern chat interface with conversation history

### Data
- **Response Dataset**: `app/responses.json` - 2102+ real airline customer service responses
- **Intent Examples**: `data/sample_intents.json` - Training examples for intent detection
- **Vector Database**: `data/chroma_airline/` - ChromaDB persistent storage

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ASAAP
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot()"
   ```

## 🚀 Usage

### Quick Start (Automated)

**Windows:**
```bash
deploy.bat deploy
```

**Linux/Mac:**
```bash
./deploy.sh deploy
```

### Manual Setup

1. **Start the Backend Server**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start the Frontend UI** (in a new terminal)
   ```bash
   streamlit run ui/app_ui.py
   ```

3. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend API: http://127.0.0.1:8000
   - API Docs: http://127.0.0.1:8000/docs

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

### API Usage

**Chat Endpoint**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "message=Do you allow cats on flights?"
```

**Response**
```json
{
  "response": "Small cats and dogs are welcome in the cabin if they meet the carrier size requirements and remain inside it during the flight."
}
```

## 🧠 How It Works

### 1. Intent Detection
The system uses keyword-based pattern matching with priority ordering to detect user intents:

```python
# Pet policy detection
if any(word in user_lower for word in ["pet", "cat", "dog", "animal", "pets", "bring my", "allow", "cabin"]):
    intent = "pet_policy"
```

### 2. Response Generation
- **Dataset Responses**: Uses 2102+ real airline customer service responses
- **Dynamic Generation**: Creates realistic flight details, prices, and times
- **Context Awareness**: Adapts responses based on user input content

### 3. Vector Search
- Converts text to embeddings using SentenceTransformer
- Stores intent examples in ChromaDB for similarity search
- Provides context-aware response selection

## 📊 Dataset

The system uses a comprehensive dataset of real airline customer service interactions:

- **2,102 customer interactions** from actual airline customer service
- **Multiple intents**: Pet Travel, Flight Status, Booking, Complaints, etc.
- **Rich metadata**: Intent, tone, policy reference, and response text
- **Professional language**: Real airline customer service terminology

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
# Database
CHROMA_DB_PATH=data/chroma_airline

# API
API_HOST=127.0.0.1
API_PORT=8000

# UI
UI_PORT=8501
```

### Customization
- **Add new intents**: Update `data/sample_intents.json`
- **Modify responses**: Edit `app/responses.json`
- **Adjust patterns**: Update intent detection in `app/chatbot.py`

## 🧪 Testing

### Test Individual Components
```bash
# Test chatbot
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot(); print(bot.get_response('Do you allow cats on flights?'))"

# Test intent detection
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot(); print(bot.get_response('I want to book a flight to Paris'))"
```

### Test API
```bash
# Test chat endpoint
curl -X POST "http://127.0.0.1:8000/chat" -d "message=Hello"
```

## 📁 Project Structure

```
ASAAP/
├── app/
│   ├── main.py                 # FastAPI server
│   ├── chatbot.py              # Main chatbot logic
│   ├── enhanced_ai_generator.py # AI response generator
│   ├── vector_db.py            # ChromaDB integration
│   ├── model_utils.py          # AI model utilities
│   ├── responses.json          # Customer service dataset
│   └── airline_policy.json     # Policy definitions
├── ui/
│   └── app_ui.py               # Streamlit UI
├── data/
│   ├── sample_intents.json     # Intent examples
│   └── chroma_airline/         # Vector database
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: Real airline customer service interactions
- **Technologies**: FastAPI, Streamlit, ChromaDB, SentenceTransformers
- **AI Models**: all-MiniLM-L6-v2 for embeddings

## 📚 Documentation

### Runbook
For detailed operational procedures, troubleshooting, and maintenance:
- **[RUNBOOK.md](RUNBOOK.md)** - Complete operational guide
- **Deployment Scripts** - Automated setup and management
- **Monitoring Tools** - Health checks and performance tracking

### Key Files
- `RUNBOOK.md` - Operational procedures and troubleshooting
- `deploy.sh` / `deploy.bat` - Automated deployment scripts
- `monitor.py` - System monitoring and health checks

## 📞 Support

For support, email support@asap-airline.com or create an issue in this repository.

---

**Built with ❤️ for the airline industry**
