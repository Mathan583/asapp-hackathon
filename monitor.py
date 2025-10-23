#!/usr/bin/env python3
"""
ASAAP Monitoring Script
Monitors the health and performance of the ASAAP airline chatbot system
"""

import requests
import time
import psutil
import json
import os
from datetime import datetime
import argparse

class ASAAPMonitor:
    def __init__(self, backend_url="http://127.0.0.1:8000", frontend_url="http://localhost:8501"):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.log_file = "monitoring.log"
        
    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def check_backend_health(self):
        """Check if backend is responding"""
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=5)
            if response.status_code == 200:
                self.log("Backend health check: PASSED")
                return True
            else:
                self.log(f"Backend health check: FAILED (Status: {response.status_code})", "ERROR")
                return False
        except requests.exceptions.RequestException as e:
            self.log(f"Backend health check: FAILED ({str(e)})", "ERROR")
            return False
    
    def check_frontend_health(self):
        """Check if frontend is responding"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.log("Frontend health check: PASSED")
                return True
            else:
                self.log(f"Frontend health check: FAILED (Status: {response.status_code})", "ERROR")
                return False
        except requests.exceptions.RequestException as e:
            self.log(f"Frontend health check: FAILED ({str(e)})", "ERROR")
            return False
    
    def test_chatbot_functionality(self):
        """Test chatbot response generation"""
        test_messages = [
            "Hello",
            "Do you allow pets on flights?",
            "I want to book a flight",
            "Check my flight status"
        ]
        
        results = []
        for message in test_messages:
            try:
                response = requests.post(
                    f"{self.backend_url}/chat",
                    data={"message": message},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "response" in data and data["response"]:
                        results.append(True)
                        self.log(f"Chat test '{message}': PASSED")
                    else:
                        results.append(False)
                        self.log(f"Chat test '{message}': FAILED (No response)", "ERROR")
                else:
                    results.append(False)
                    self.log(f"Chat test '{message}': FAILED (Status: {response.status_code})", "ERROR")
                    
            except requests.exceptions.RequestException as e:
                results.append(False)
                self.log(f"Chat test '{message}': FAILED ({str(e)})", "ERROR")
        
        success_rate = sum(results) / len(results) * 100
        self.log(f"Chatbot functionality: {success_rate:.1f}% success rate")
        return success_rate >= 80  # 80% success rate threshold
    
    def check_system_resources(self):
        """Check system resource usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Check thresholds
            cpu_ok = cpu_percent < 80
            memory_ok = memory_percent < 85
            disk_ok = disk_percent < 90
            
            self.log(f"System resources - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%, Disk: {disk_percent:.1f}%")
            
            if not cpu_ok:
                self.log(f"High CPU usage: {cpu_percent:.1f}%", "WARNING")
            if not memory_ok:
                self.log(f"High memory usage: {memory_percent:.1f}%", "WARNING")
            if not disk_ok:
                self.log(f"High disk usage: {disk_percent:.1f}%", "WARNING")
            
            return cpu_ok and memory_ok and disk_ok
            
        except Exception as e:
            self.log(f"System resource check failed: {str(e)}", "ERROR")
            return False
    
    def check_database_health(self):
        """Check ChromaDB database health"""
        try:
            # Check if database directory exists
            db_path = "data/chroma_airline"
            if not os.path.exists(db_path):
                self.log("Database directory not found", "ERROR")
                return False
            
            # Check if database files exist
            required_files = ["chroma.sqlite3"]
            for file in required_files:
                if not os.path.exists(os.path.join(db_path, file)):
                    self.log(f"Database file missing: {file}", "ERROR")
                    return False
            
            # Check database size
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(db_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            
            size_mb = total_size / (1024 * 1024)
            self.log(f"Database size: {size_mb:.2f} MB")
            
            if size_mb < 1:
                self.log("Database size seems too small", "WARNING")
                return False
            
            self.log("Database health check: PASSED")
            return True
            
        except Exception as e:
            self.log(f"Database health check failed: {str(e)}", "ERROR")
            return False
    
    def measure_response_time(self):
        """Measure average response time"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/chat",
                data={"message": "Hello"},
                timeout=10
            )
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                self.log(f"Response time: {response_time:.2f}ms")
                return response_time < 5000  # 5 second threshold
            else:
                self.log(f"Response time test failed (Status: {response.status_code})", "ERROR")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"Response time test failed: {str(e)}", "ERROR")
            return False
    
    def run_full_check(self):
        """Run complete health check"""
        self.log("Starting full health check...")
        
        checks = {
            "Backend Health": self.check_backend_health(),
            "Frontend Health": self.check_frontend_health(),
            "Chatbot Functionality": self.test_chatbot_functionality(),
            "System Resources": self.check_system_resources(),
            "Database Health": self.check_database_health(),
            "Response Time": self.measure_response_time()
        }
        
        passed = sum(checks.values())
        total = len(checks)
        
        self.log(f"Health check completed: {passed}/{total} checks passed")
        
        if passed == total:
            self.log("All systems operational", "SUCCESS")
            return True
        else:
            self.log("Some systems have issues", "WARNING")
            return False
    
    def continuous_monitoring(self, interval=60):
        """Run continuous monitoring"""
        self.log(f"Starting continuous monitoring (interval: {interval}s)")
        
        try:
            while True:
                self.run_full_check()
                self.log(f"Waiting {interval} seconds before next check...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log("Monitoring stopped by user")
        except Exception as e:
            self.log(f"Monitoring error: {str(e)}", "ERROR")

def main():
    parser = argparse.ArgumentParser(description="ASAAP System Monitor")
    parser.add_argument("--backend", default="http://127.0.0.1:8000", help="Backend URL")
    parser.add_argument("--frontend", default="http://localhost:8501", help="Frontend URL")
    parser.add_argument("--interval", type=int, default=60, help="Monitoring interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run check once and exit")
    
    args = parser.parse_args()
    
    monitor = ASAAPMonitor(args.backend, args.frontend)
    
    if args.once:
        monitor.run_full_check()
    else:
        monitor.continuous_monitoring(args.interval)

if __name__ == "__main__":
    main()
