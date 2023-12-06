import re
import json

def parse_dns_log_line_by_line(log_file_path):
    try:
        parsed_entries = []
        line_number = 0
        with open(log_file_path, 'r') as file:
            for line in file:
                line_number += 1
                date_match = re.search('\d{2}-[a-zA-Z]{3}-\d{4}', line)
                ip_match = re.search('\d{2}:\d{2}:\d{2}\.\d{3}', line)
                query_match = re.search('queries: (.+)', line)
                general_match = re.search('general: (.+)', line)
                xfer_match = re.search('xfer-in: (.+)', line)
                notify_match = re.search('notify: (.+)', line)

                date = date_match.group() if date_match else None
                ip = ip_match.group() if ip_match else None
                query = query_match.group(1) if query_match else None
                general = general_match.group(1) if general_match else None
                xfer = xfer_match.group(1) if xfer_match else None
                notify = notify_match.group(1) if notify_match else None
                


                entry = {
                    "line_number": line_number,
                    "date": date,
                    "ip": ip,
                    "queries": query,
                    "general": general,
                    "xfer_in": xfer,
                    "notify": notify
                }
                
                parsed_entries.append(entry)

        return parsed_entries


    except FileNotFoundError:
        print(f"Error: File not found at path {log_file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


dns_log_file_path = 'E:\\NetOptiq\\dns_log_file.log'
parsed_entries = parse_dns_log_line_by_line(dns_log_file_path)

# Write to JSON file
json_file_path = 'parsed_dns_log.json'
with open(json_file_path, 'w') as json_file:
    json.dump(parsed_entries, json_file, indent=4)

print(f"Parsed entries written to {json_file_path}")
