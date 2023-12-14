import re
import time
from datetime import datetime


log_file_path = "/home/bewin/Projects/Backend-1/Sample/query.log"

def process_log_entry(entry):
    timestamp, action, details = entry
    a = details.split()
    date_string_with_year = f"2023 {timestamp}"
    datetime_object = datetime.strptime(date_string_with_year, "%Y %b %d %H:%M:%S")

    
    print(f"Timestamp: {datetime_object}")
    print(f"Action: {action}")
    print(f"Details: {details}")
    print(a[0])
    print(a[1])
    print(a[2])
    print(a[3])
    print(a[4])
    print(a[5])
    print(a[6])
    print(a[7])
    print("\n")

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        log_entries = file.read()
    matches = re.findall(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) .* (reply): (.+)', log_entries)
    return matches

processed_entries = []

while True:
    current_entries = read_log_file(log_file_path)

    # Check for new entries
    new_entries = [entry for entry in current_entries if entry not in processed_entries]
    for entry in new_entries:
        process_log_entry(entry)

    # Update processed_entries
    processed_entries = current_entries

    # Sleep for a specified interval (e.g., 1 second)
    time.sleep(1)
