file_path = 'block.conf'
output_file_path = 'output.conf'
import re

unique_values = set()

with open(file_path, 'r') as file, open(output_file_path, 'w') as output_file:
    for line_number, line in enumerate(file, start=1):
        pattern = re.compile(r'local-zone: "(.*?)" redirect')
        match = pattern.search(line)
        if match:
            ip_address = match.group(1)
            if ip_address not in unique_values:
                unique_values.add(ip_address)
                output_file.write(f'local-zone: "{ip_address}" redirect\n')
                output_file.write(f'local-data: "{ip_address} A 0.0.0.0"\n')


