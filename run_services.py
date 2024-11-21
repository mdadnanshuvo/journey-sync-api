import subprocess
import time

# Start the user service
user_service = subprocess.Popen(["python3", "./Users/user_service.py"])

# Wait for the user service to be fully up (optional but helpful)
time.sleep(2)  # Adjust the sleep time if needed

# Start the destination service
destination_service = subprocess.Popen(["python3", "./Destination/destination_service.py"])

# Wait for both services to finish (optional)
# user_service.wait()
# destination_service.wait()
