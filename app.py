# app.py
from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

# Global variables to track test status
stress_active = False
start_time = None

def cpu_stress():
    """Function to stress CPU"""
    global stress_active
    while stress_active:
        # Simple CPU-intensive calculation
        x = 0
        for i in range(1000000):
            x += i * i

@app.route('/')
def home():
    return jsonify({
        "status": "Server is running",
        "instructions": {
            "start_test": "GET /start",
            "stop_test": "GET /stop",
            "check_status": "GET /status"
        }
    })

@app.route('/start')
def start_stress():
    """Start CPU stress test"""
    global stress_active, start_time
    
    if not stress_active:
        stress_active = True
        start_time = time.time()
        
        # Start CPU stress threads
        for _ in range(2):
            thread = threading.Thread(target=cpu_stress)
            thread.daemon = True
            thread.start()
        
        return jsonify({
            "message": "CPU stress test started",
            "status": "running",
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({
            "message": "CPU stress test is already running",
            "status": "running",
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        })

@app.route('/stop')
def stop_stress():
    """Stop CPU stress test"""
    global stress_active, start_time
    
    if stress_active:
        stress_active = False
        duration = time.time() - start_time if start_time else 0
        start_time = None
        
        return jsonify({
            "message": "CPU stress test stopped",
            "status": "stopped",
            "duration_seconds": round(duration, 2)
        })
    else:
        return jsonify({
            "message": "CPU stress test is not running",
            "status": "stopped"
        })

@app.route('/status')
def status():
    """Get current test status"""
    global stress_active, start_time
    
    current_status = {
        "stress_test_active": stress_active,
        "current_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    if stress_active and start_time:
        current_status["running_duration_seconds"] = round(time.time() - start_time, 2)
        current_status["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    
    return jsonify(current_status)

if __name__ == '__main__':
    print("Server starting on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)