import json

file_path = "dns.log"

with open(file_path, 'r') as file:
    data = file.read()
lines = data.strip().split('\n')
parsed_data = [json.loads(line) for line in lines]

print(json.dumps(parsed_data, indent=2))
