# 🚀 ASAAP Runbook - Airline Smart Assistant AI Platform

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [Running the Application](#running-the-application)
5. [Monitoring & Health Checks](#monitoring--health-checks)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)
8. [Scaling & Performance](#scaling--performance)
9. [Backup & Recovery](#backup--recovery)
10. [Emergency Procedures](#emergency-procedures)

---

## 🎯 System Overview

### Architecture Components
- **Backend**: FastAPI server (Port 8000)
- **Frontend**: Streamlit UI (Port 8501)
- **Database**: ChromaDB (Persistent storage)
- **AI Models**: SentenceTransformer + Custom Response Generator
- **Data**: 2102+ customer service responses

### Key Services
- **Chat API**: `/chat` endpoint for user interactions
- **Intent Detection**: 10+ airline service intents
- **Response Generation**: Hybrid dataset + AI approach
- **Vector Search**: ChromaDB for similarity matching

---

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Network**: Internet connection for model downloads

### Software Dependencies
```bash
# Core Python packages
python>=3.8
pip>=21.0

# Required packages (see requirements.txt)
fastapi>=0.68.0
uvicorn>=0.15.0
streamlit>=1.0.0
chromadb>=0.4.0
sentence-transformers>=2.0.0
transformers>=4.20.0
```

---

## 🚀 Installation & Setup

### Step 1: Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd ASAAP

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Verify Python version
python --version  # Should be 3.8+
```

### Step 2: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(fastapi|streamlit|chromadb|sentence-transformers)"
```

### Step 3: Initialize Database
```bash
# Initialize ChromaDB with sample data
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot(); print('✅ Database initialized successfully')"
```

### Step 4: Verify Setup
```bash
# Test chatbot functionality
python -c "
from app.chatbot import AirlineChatbot
bot = AirlineChatbot()
response = bot.get_response('Hello')
print(f'Test response: {response}')
"
```

---

## 🏃 Running the Application

### Development Mode

#### Start Backend Server
```bash
# Terminal 1: Start FastAPI server
cd ASAAP
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Start Frontend UI
```bash
# Terminal 2: Start Streamlit UI
cd ASAAP
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run ui/app_ui.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Production Mode

#### Using Gunicorn (Linux/Mac)
```bash
# Install Gunicorn
pip install gunicorn

# Start production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Using Docker (Optional)
```dockerfile
# Create Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 8501

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Monitoring & Health Checks

### Health Check Endpoints

#### Backend Health Check
```bash
# Check if FastAPI server is running
curl http://127.0.0.1:8000/docs

# Test chat endpoint
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "message=Hello"
```

#### Frontend Health Check
```bash
# Check if Streamlit is accessible
curl http://localhost:8501
```

### System Monitoring

#### Check Process Status
```bash
# Check running processes
ps aux | grep -E "(uvicorn|streamlit)"

# Check port usage
netstat -tulpn | grep -E "(8000|8501)"
```

#### Log Monitoring
```bash
# Monitor application logs
tail -f logs/app.log  # If logging is configured

# Check system resources
top -p $(pgrep -f "uvicorn|streamlit")
```

### Performance Metrics

#### Response Time Testing
```bash
# Test API response time
time curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "message=Do you allow pets on flights?"
```

#### Memory Usage
```bash
# Check memory usage
ps aux | grep -E "(uvicorn|streamlit)" | awk '{print $2, $4, $6}'
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
**Error**: `Address already in use`
**Solution**:
```bash
# Find process using port
lsof -i :8000  # or :8501

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

#### 2. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'app'`
**Solution**:
```bash
# Ensure you're in the correct directory
pwd  # Should show ASAAP directory

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. ChromaDB Connection Issues
**Error**: `ChromaDB connection failed`
**Solution**:
```bash
# Check database directory permissions
ls -la data/chroma_airline/

# Recreate database
rm -rf data/chroma_airline/
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot()"
```

#### 4. Model Download Issues
**Error**: `OSError: Can't load tokenizer`
**Solution**:
```bash
# Clear model cache
rm -rf ~/.cache/huggingface/

# Reinstall transformers
pip install transformers --force-reinstall

# Test model loading
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2')"
```

#### 5. Memory Issues
**Error**: `CUDA out of memory` or high RAM usage
**Solution**:
```bash
# Use CPU instead of GPU
export CUDA_VISIBLE_DEVICES=""

# Reduce batch size in model_utils.py
# Set max_new_tokens to lower value

# Monitor memory usage
htop  # or top
```

### Debug Mode

#### Enable Debug Logging
```python
# Add to app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Test Individual Components
```bash
# Test chatbot directly
python -c "
from app.chatbot import AirlineChatbot
bot = AirlineChatbot()
print('Chatbot initialized successfully')
"

# Test response generator
python -c "
from app.enhanced_ai_generator import EnhancedAIResponseGenerator
gen = EnhancedAIResponseGenerator()
print('Response generator initialized successfully')
"

# Test vector database
python -c "
from app.vector_db import VectorDB
db = VectorDB()
print('Vector database initialized successfully')
"
```

---

## 🔄 Maintenance

### Daily Tasks
- [ ] Check application logs for errors
- [ ] Monitor response times
- [ ] Verify all services are running
- [ ] Check disk space usage

### Weekly Tasks
- [ ] Update dependencies: `pip list --outdated`
- [ ] Clean up log files
- [ ] Backup ChromaDB data
- [ ] Review performance metrics

### Monthly Tasks
- [ ] Update Python packages
- [ ] Review and update response dataset
- [ ] Performance optimization review
- [ ] Security updates

### Database Maintenance
```bash
# Backup ChromaDB
cp -r data/chroma_airline/ backups/chroma_airline_$(date +%Y%m%d)/

# Clean up old backups (keep last 7 days)
find backups/ -type d -mtime +7 -exec rm -rf {} \;
```

---

## 📈 Scaling & Performance

### Horizontal Scaling
```bash
# Run multiple FastAPI instances
uvicorn app.main:app --port 8000 &
uvicorn app.main:app --port 8001 &
uvicorn app.main:app --port 8002 &

# Use load balancer (nginx)
# Configure nginx to distribute load across ports
```

### Performance Optimization

#### Database Optimization
```python
# In vector_db.py - optimize ChromaDB settings
self.client = chromadb.PersistentClient(
    path=path,
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)
```

#### Caching
```python
# Add response caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_response(user_input: str):
    return bot.get_response(user_input)
```

### Resource Limits
```bash
# Set memory limits
ulimit -v 2097152  # 2GB virtual memory

# Monitor resource usage
watch -n 1 'ps aux | grep -E "(uvicorn|streamlit)"'
```

---

## 💾 Backup & Recovery

### Backup Procedures

#### Full System Backup
```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup application code
cp -r app/ $BACKUP_DIR/
cp -r ui/ $BACKUP_DIR/
cp -r data/ $BACKUP_DIR/
cp requirements.txt $BACKUP_DIR/
cp README.md $BACKUP_DIR/

# Backup database
cp -r data/chroma_airline/ $BACKUP_DIR/

echo "Backup completed: $BACKUP_DIR"
```

#### Database-Only Backup
```bash
# Backup ChromaDB
tar -czf chromadb_backup_$(date +%Y%m%d).tar.gz data/chroma_airline/
```

### Recovery Procedures

#### Full System Recovery
```bash
# Restore from backup
BACKUP_DIR="backups/20241201_120000"  # Replace with actual backup
cp -r $BACKUP_DIR/* ./

# Reinstall dependencies
pip install -r requirements.txt

# Test system
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot()"
```

#### Database Recovery
```bash
# Restore ChromaDB
tar -xzf chromadb_backup_20241201.tar.gz
```

---

## 🚨 Emergency Procedures

### Service Outage Response

#### 1. Immediate Assessment
```bash
# Check service status
curl -f http://127.0.0.1:8000/docs || echo "Backend DOWN"
curl -f http://localhost:8501 || echo "Frontend DOWN"

# Check system resources
df -h  # Disk space
free -h  # Memory
top  # CPU usage
```

#### 2. Quick Restart
```bash
# Kill existing processes
pkill -f "uvicorn"
pkill -f "streamlit"

# Restart services
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
streamlit run ui/app_ui.py &
```

#### 3. Rollback Procedure
```bash
# Rollback to previous version
git checkout HEAD~1  # Previous commit
pip install -r requirements.txt
# Restart services
```

### Data Corruption Recovery
```bash
# Rebuild ChromaDB from scratch
rm -rf data/chroma_airline/
python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot()"
```

### Security Incident Response
```bash
# Immediate actions
# 1. Stop all services
pkill -f "uvicorn"
pkill -f "streamlit"

# 2. Check logs for suspicious activity
grep -i "error\|exception\|failed" logs/*.log

# 3. Review access logs
# 4. Update security patches
pip install --upgrade fastapi streamlit
```

---

## 📞 Support Contacts

### Internal Team
- **Development Team**: dev-team@company.com
- **DevOps Team**: devops@company.com
- **On-Call Engineer**: +1-XXX-XXX-XXXX

### External Resources
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **ChromaDB Documentation**: https://docs.trychroma.com/

### Escalation Procedures
1. **Level 1**: Check logs and restart services
2. **Level 2**: Contact development team
3. **Level 3**: Escalate to DevOps team
4. **Level 4**: Contact external support

---

## 📝 Change Log

### Version History
- **v1.0.0**: Initial release with basic chatbot functionality
- **v1.1.0**: Added pet policy and enhanced intent detection
- **v1.2.0**: Improved UI and response generation

### Known Issues
- **Issue #1**: High memory usage with large datasets
- **Issue #2**: Slow response times during peak usage
- **Issue #3**: ChromaDB connection timeout on startup

---

**Last Updated**: December 2024  
**Document Version**: 1.0  
**Maintained By**: ASAAP Development Team
