# app.py
from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

# Global variables to track test status
stress_active = False
ram_stress_active = False
start_time = None
ram_start_time = None

def cpu_stress():
    """Function to stress CPU"""
    global stress_active
    while stress_active:
        # Simple CPU-intensive calculation
        x = 0
        for i in range(1000000):
            x += i * i

def ram_stress():
    """Function to stress RAM"""
    global ram_stress_active
    memory_holder = []
    while ram_stress_active:
        # Allocate memory in MB chunks
        memory_holder.append(bytearray(1024 * 1024))  # 1MB
        time.sleep(0.1)  # Adjust allocation speed

@app.route('/')
def home():
    return jsonify({
        "status": "Server is running",
        "instructions": {
            "start_cpu_test": "GET /start_cpu",
            "stop_cpu_test": "GET /stop_cpu",
            "start_ram_test": "GET /start_ram",
            "stop_ram_test": "GET /stop_ram",
            "check_status": "GET /status"
        }
    })

@app.route('/start_cpu')
def start_cpu_stress():
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

@app.route('/stop_cpu')
def stop_cpu_stress():
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

@app.route('/start_ram')
def start_ram_stress():
    """Start RAM stress test"""
    global ram_stress_active, ram_start_time

    if not ram_stress_active:
        ram_stress_active = True
        ram_start_time = time.time()

        # Start RAM stress thread
        thread = threading.Thread(target=ram_stress)
        thread.daemon = True
        thread.start()

        return jsonify({
            "message": "RAM stress test started",
            "status": "running",
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({
            "message": "RAM stress test is already running",
            "status": "running",
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ram_start_time))
        })

@app.route('/stop_ram')
def stop_ram_stress():
    """Stop RAM stress test"""
    global ram_stress_active, ram_start_time

    if ram_stress_active:
        ram_stress_active = False
        duration = time.time() - ram_start_time if ram_start_time else 0
        ram_start_time = None

        return jsonify({
            "message": "RAM stress test stopped",
            "status": "stopped",
            "duration_seconds": round(duration, 2)
        })
    else:
        return jsonify({
            "message": "RAM stress test is not running",
            "status": "stopped"
        })

@app.route('/status')
def status():
    """Get current test status"""
    global stress_active, ram_stress_active, start_time, ram_start_time

    current_status = {
        "cpu_stress_test_active": stress_active,
        "ram_stress_test_active": ram_stress_active,
        "current_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    if stress_active and start_time:
        current_status["cpu_running_duration_seconds"] = round(time.time() - start_time, 2)
        current_status["cpu_start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))

    if ram_stress_active and ram_start_time:
        current_status["ram_running_duration_seconds"] = round(time.time() - ram_start_time, 2)
        current_status["ram_start_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ram_start_time))

    return jsonify(current_status)

if __name__ == '__main__':
    print("Server starting on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
