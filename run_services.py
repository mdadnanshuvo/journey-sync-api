import os
import subprocess
import sys

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)  # Ensure BASE_DIR is in PYTHONPATH

# Path to the virtual environment
VENV_DIR = os.path.join(BASE_DIR, "venv")  # Update to match your venv location

# Define services with their module paths and port information
services = [
    {"name": "User Service", "module": "Users.user_service", "port": 5000},
    {"name": "Auth Service", "module": "Auth.auth_service", "port": 5001},
    {"name": "Destination Service", "module": "Destination.destination_service", "port": 5002},
]

# Detect Python executable
python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
if not os.path.exists(python_executable):
    python_executable = os.path.join(VENV_DIR, "bin", "python")  # Linux/Mac

# List to hold process objects
processes = []

try:
    # Start all services
    for service in services:
        print(f"Starting {service['name']} on port {service['port']}...")

        # Launch the service using -m for module execution
        command = [python_executable, "-m", service["module"]]

        # Start the process
        process = subprocess.Popen(command, cwd=BASE_DIR)
        processes.append(process)

    # Keep the main script running
    print("All services are running. Press CTRL+C to stop.")
    for process in processes:
        process.wait()

except KeyboardInterrupt:
    # Handle termination
    print("\nShutting down all services...")
    for process in processes:
        process.terminate()
        process.wait()
