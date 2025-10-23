#!/bin/bash

# ASAAP Deployment Script
# This script automates the deployment and startup of the ASAAP airline chatbot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=8501
VENV_DIR="venv"
LOG_DIR="logs"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Windows
is_windows() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        return 0
    else
        return 1
    fi
}

# Setup virtual environment
setup_venv() {
    log_info "Setting up virtual environment..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python -m venv $VENV_DIR
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    if is_windows; then
        source $VENV_DIR/Scripts/activate
    else
        source $VENV_DIR/bin/activate
    fi
    
    log_success "Virtual environment activated"
}

# Install dependencies
install_deps() {
    log_info "Installing dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt not found!"
        exit 1
    fi
    
    pip install -r requirements.txt
    log_success "Dependencies installed"
}

# Initialize database
init_database() {
    log_info "Initializing database..."
    
    python -c "
from app.chatbot import AirlineChatbot
try:
    bot = AirlineChatbot()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
    exit(1)
"
    
    log_success "Database initialized"
}

# Check if ports are available
check_ports() {
    log_info "Checking port availability..."
    
    # Check backend port
    if lsof -i :$BACKEND_PORT >/dev/null 2>&1; then
        log_warning "Port $BACKEND_PORT is already in use"
        log_info "Attempting to kill existing process..."
        pkill -f "uvicorn.*$BACKEND_PORT" || true
        sleep 2
    fi
    
    # Check frontend port
    if lsof -i :$FRONTEND_PORT >/dev/null 2>&1; then
        log_warning "Port $FRONTEND_PORT is already in use"
        log_info "Attempting to kill existing process..."
        pkill -f "streamlit.*$FRONTEND_PORT" || true
        sleep 2
    fi
    
    log_success "Ports are available"
}

# Create logs directory
create_logs_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p $LOG_DIR
        log_success "Logs directory created"
    fi
}

# Start backend server
start_backend() {
    log_info "Starting backend server on port $BACKEND_PORT..."
    
    # Start in background
    nohup uvicorn app.main:app --host 127.0.0.1 --port $BACKEND_PORT > $LOG_DIR/backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait for server to start
    sleep 5
    
    # Check if server is running
    if curl -f http://127.0.0.1:$BACKEND_PORT/docs >/dev/null 2>&1; then
        log_success "Backend server started successfully (PID: $BACKEND_PID)"
        echo $BACKEND_PID > $LOG_DIR/backend.pid
    else
        log_error "Backend server failed to start"
        exit 1
    fi
}

# Start frontend UI
start_frontend() {
    log_info "Starting frontend UI on port $FRONTEND_PORT..."
    
    # Start in background
    nohup streamlit run ui/app_ui.py --server.port $FRONTEND_PORT > $LOG_DIR/frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # Wait for UI to start
    sleep 5
    
    # Check if UI is running
    if curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
        log_success "Frontend UI started successfully (PID: $FRONTEND_PID)"
        echo $FRONTEND_PID > $LOG_DIR/frontend.pid
    else
        log_error "Frontend UI failed to start"
        exit 1
    fi
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Test backend
    if curl -f http://127.0.0.1:$BACKEND_PORT/docs >/dev/null 2>&1; then
        log_success "Backend health check passed"
    else
        log_error "Backend health check failed"
        return 1
    fi
    
    # Test frontend
    if curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
        log_success "Frontend health check passed"
    else
        log_error "Frontend health check failed"
        return 1
    fi
    
    # Test chatbot functionality
    RESPONSE=$(curl -s -X POST "http://127.0.0.1:$BACKEND_PORT/chat" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "message=Hello" | grep -o '"response":"[^"]*"' | cut -d'"' -f4)
    
    if [ ! -z "$RESPONSE" ]; then
        log_success "Chatbot functionality test passed"
        log_info "Sample response: $RESPONSE"
    else
        log_error "Chatbot functionality test failed"
        return 1
    fi
}

# Display status
show_status() {
    log_info "ASAAP Application Status:"
    echo ""
    echo "🌐 Frontend UI: http://localhost:$FRONTEND_PORT"
    echo "🔧 Backend API: http://127.0.0.1:$BACKEND_PORT"
    echo "📚 API Docs: http://127.0.0.1:$BACKEND_PORT/docs"
    echo ""
    echo "📊 Process IDs:"
    if [ -f "$LOG_DIR/backend.pid" ]; then
        echo "   Backend: $(cat $LOG_DIR/backend.pid)"
    fi
    if [ -f "$LOG_DIR/frontend.pid" ]; then
        echo "   Frontend: $(cat $LOG_DIR/frontend.pid)"
    fi
    echo ""
    echo "📝 Logs:"
    echo "   Backend: $LOG_DIR/backend.log"
    echo "   Frontend: $LOG_DIR/frontend.log"
    echo ""
}

# Stop services
stop_services() {
    log_info "Stopping services..."
    
    # Stop backend
    if [ -f "$LOG_DIR/backend.pid" ]; then
        BACKEND_PID=$(cat $LOG_DIR/backend.pid)
        kill $BACKEND_PID 2>/dev/null || true
        rm -f $LOG_DIR/backend.pid
        log_success "Backend stopped"
    fi
    
    # Stop frontend
    if [ -f "$LOG_DIR/frontend.pid" ]; then
        FRONTEND_PID=$(cat $LOG_DIR/frontend.pid)
        kill $FRONTEND_PID 2>/dev/null || true
        rm -f $LOG_DIR/frontend.pid
        log_success "Frontend stopped"
    fi
    
    # Kill any remaining processes
    pkill -f "uvicorn.*app.main:app" || true
    pkill -f "streamlit.*ui/app_ui.py" || true
    
    log_success "All services stopped"
}

# Main deployment function
deploy() {
    log_info "Starting ASAAP deployment..."
    echo ""
    
    setup_venv
    install_deps
    init_database
    check_ports
    create_logs_dir
    start_backend
    start_frontend
    
    sleep 3
    
    if health_check; then
        log_success "ASAAP deployment completed successfully!"
        echo ""
        show_status
    else
        log_error "ASAAP deployment failed health check"
        stop_services
        exit 1
    fi
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "start")
        check_ports
        create_logs_dir
        start_backend
        start_frontend
        show_status
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        stop_services
        sleep 2
        check_ports
        create_logs_dir
        start_backend
        start_frontend
        show_status
        ;;
    "status")
        show_status
        ;;
    "health")
        health_check
        ;;
    "logs")
        echo "Backend logs:"
        tail -f $LOG_DIR/backend.log
        ;;
    *)
        echo "Usage: $0 {deploy|start|stop|restart|status|health|logs}"
        echo ""
        echo "Commands:"
        echo "  deploy  - Full deployment (setup, install, start)"
        echo "  start   - Start services only"
        echo "  stop    - Stop all services"
        echo "  restart - Restart services"
        echo "  status  - Show application status"
        echo "  health  - Perform health check"
        echo "  logs    - Show backend logs"
        exit 1
        ;;
esac
