@echo off
REM ASAAP Deployment Script for Windows
REM This script automates the deployment and startup of the ASAAP airline chatbot

setlocal enabledelayedexpansion

REM Configuration
set BACKEND_PORT=8000
set FRONTEND_PORT=8501
set VENV_DIR=venv
set LOG_DIR=logs

REM Functions
:log_info
echo [INFO] %~1
goto :eof

:log_success
echo [SUCCESS] %~1
goto :eof

:log_warning
echo [WARNING] %~1
goto :eof

:log_error
echo [ERROR] %~1
goto :eof

REM Setup virtual environment
:setup_venv
call :log_info "Setting up virtual environment..."

if not exist "%VENV_DIR%" (
    python -m venv %VENV_DIR%
    call :log_success "Virtual environment created"
) else (
    call :log_info "Virtual environment already exists"
)

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat
call :log_success "Virtual environment activated"
goto :eof

REM Install dependencies
:install_deps
call :log_info "Installing dependencies..."

if not exist "requirements.txt" (
    call :log_error "requirements.txt not found!"
    exit /b 1
)

pip install -r requirements.txt
call :log_success "Dependencies installed"
goto :eof

REM Initialize database
:init_database
call :log_info "Initializing database..."

python -c "from app.chatbot import AirlineChatbot; bot = AirlineChatbot(); print('✅ Database initialized successfully')"
if errorlevel 1 (
    call :log_error "Database initialization failed"
    exit /b 1
)

call :log_success "Database initialized"
goto :eof

REM Check if ports are available
:check_ports
call :log_info "Checking port availability..."

REM Check backend port
netstat -an | findstr ":%BACKEND_PORT% " >nul
if not errorlevel 1 (
    call :log_warning "Port %BACKEND_PORT% is already in use"
    call :log_info "Attempting to kill existing process..."
    taskkill /f /im python.exe /fi "WINDOWTITLE eq uvicorn*" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

REM Check frontend port
netstat -an | findstr ":%FRONTEND_PORT% " >nul
if not errorlevel 1 (
    call :log_warning "Port %FRONTEND_PORT% is already in use"
    call :log_info "Attempting to kill existing process..."
    taskkill /f /im python.exe /fi "WINDOWTITLE eq streamlit*" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

call :log_success "Ports are available"
goto :eof

REM Create logs directory
:create_logs_dir
if not exist "%LOG_DIR%" (
    mkdir %LOG_DIR%
    call :log_success "Logs directory created"
)
goto :eof

REM Start backend server
:start_backend
call :log_info "Starting backend server on port %BACKEND_PORT%..."

start /b uvicorn app.main:app --host 127.0.0.1 --port %BACKEND_PORT% > %LOG_DIR%\backend.log 2>&1

REM Wait for server to start
timeout /t 5 /nobreak >nul

REM Check if server is running
curl -f http://127.0.0.1:%BACKEND_PORT%/docs >nul 2>&1
if not errorlevel 1 (
    call :log_success "Backend server started successfully"
) else (
    call :log_error "Backend server failed to start"
    exit /b 1
)
goto :eof

REM Start frontend UI
:start_frontend
call :log_info "Starting frontend UI on port %FRONTEND_PORT%..."

start /b streamlit run ui/app_ui.py --server.port %FRONTEND_PORT% > %LOG_DIR%\frontend.log 2>&1

REM Wait for UI to start
timeout /t 5 /nobreak >nul

REM Check if UI is running
curl -f http://localhost:%FRONTEND_PORT% >nul 2>&1
if not errorlevel 1 (
    call :log_success "Frontend UI started successfully"
) else (
    call :log_error "Frontend UI failed to start"
    exit /b 1
)
goto :eof

REM Health check
:health_check
call :log_info "Performing health check..."

REM Test backend
curl -f http://127.0.0.1:%BACKEND_PORT%/docs >nul 2>&1
if errorlevel 1 (
    call :log_error "Backend health check failed"
    exit /b 1
)
call :log_success "Backend health check passed"

REM Test frontend
curl -f http://localhost:%FRONTEND_PORT% >nul 2>&1
if errorlevel 1 (
    call :log_error "Frontend health check failed"
    exit /b 1
)
call :log_success "Frontend health check passed"

REM Test chatbot functionality
for /f "tokens=*" %%i in ('curl -s -X POST "http://127.0.0.1:%BACKEND_PORT%/chat" -H "Content-Type: application/x-www-form-urlencoded" -d "message=Hello"') do set RESPONSE=%%i

if not "%RESPONSE%"=="" (
    call :log_success "Chatbot functionality test passed"
    call :log_info "Sample response received"
) else (
    call :log_error "Chatbot functionality test failed"
    exit /b 1
)
goto :eof

REM Display status
:show_status
call :log_info "ASAAP Application Status:"
echo.
echo 🌐 Frontend UI: http://localhost:%FRONTEND_PORT%
echo 🔧 Backend API: http://127.0.0.1:%BACKEND_PORT%
echo 📚 API Docs: http://127.0.0.1:%BACKEND_PORT%/docs
echo.
echo 📝 Logs:
echo    Backend: %LOG_DIR%\backend.log
echo    Frontend: %LOG_DIR%\frontend.log
echo.
goto :eof

REM Stop services
:stop_services
call :log_info "Stopping services..."

REM Kill Python processes running uvicorn or streamlit
taskkill /f /im python.exe /fi "WINDOWTITLE eq uvicorn*" >nul 2>&1
taskkill /f /im python.exe /fi "WINDOWTITLE eq streamlit*" >nul 2>&1

call :log_success "All services stopped"
goto :eof

REM Main deployment function
:deploy
call :log_info "Starting ASAAP deployment..."
echo.

call :setup_venv
call :install_deps
call :init_database
call :check_ports
call :create_logs_dir
call :start_backend
call :start_frontend

timeout /t 3 /nobreak >nul

call :health_check
if errorlevel 1 (
    call :log_error "ASAAP deployment failed health check"
    call :stop_services
    exit /b 1
)

call :log_success "ASAAP deployment completed successfully!"
echo.
call :show_status
goto :eof

REM Main script logic
if "%1"=="deploy" goto deploy
if "%1"=="start" goto start_only
if "%1"=="stop" goto stop_services
if "%1"=="restart" goto restart_services
if "%1"=="status" goto show_status
if "%1"=="health" goto health_check
if "%1"=="logs" goto show_logs
if "%1"=="" goto deploy

REM Default case - show usage
echo Usage: %0 {deploy^|start^|stop^|restart^|status^|health^|logs}
echo.
echo Commands:
echo   deploy  - Full deployment (setup, install, start)
echo   start   - Start services only
echo   stop    - Stop all services
echo   restart - Restart services
echo   status  - Show application status
echo   health  - Perform health check
echo   logs    - Show backend logs
exit /b 1

:start_only
call :check_ports
call :create_logs_dir
call :start_backend
call :start_frontend
call :show_status
goto :eof

:restart_services
call :stop_services
timeout /t 2 /nobreak >nul
call :check_ports
call :create_logs_dir
call :start_backend
call :start_frontend
call :show_status
goto :eof

:show_logs
type %LOG_DIR%\backend.log
goto :eof
