import re   # import python re module for regular expressions
from collections import defaultdict     # defaultdict subclass of dict is imported from collections module 

# Regular expression to parse a log line in Combined Log Format it will capture the parameters of ip, timestamp, http method GET/POST, resource, HTTP version, HTTP status code of 3 digits, bytes captured, referrer url and user agent details
LOG_PATTERN = re.compile(r'^(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] '
                         '"(?P<method>\S+) (?P<resource>\S+) HTTP/\S+" '
                         '(?P<status>\d{3}) (?P<bytes>\d+|-).+"(?P<referrer>[^"]+)" '
                         '"(?P<user_agent>[^"]+)"$')

def parse_log_file(filename):               # We define a function parse_log_file where the log file and opened and processed line by line to yeild parsed log entries
    with open(filename, 'r') as f:
        for line in f:                      # Each log entry is returned as a dictionary with all the parameters of the Combined Log format 
            match = LOG_PATTERN.match(line)
            if match:
                yield match.groupdict()     # If the line is matched, yeild it as the dictionary of matched groups

def calculate_stats(log_filename, output_filename):         # Function to calculate the required statistics
    total_requests = 0
    total_bytes = 0
    resource_counts = defaultdict(int)
    ip_counts = defaultdict(int)
    status_codes = defaultdict(int)
    
    
    for log_entry in parse_log_file(log_filename):          # Process the log file and increment the number of requests
        total_requests += 1
        
                                                            # Process the log file to get the bytes information, the byte is only added if the feild isn't blank that is '-', the bytes are converted to integer
        bytes_transmitted = log_entry['bytes']
        if bytes_transmitted != '-':
            total_bytes += int(bytes_transmitted)
        
        
        resource_counts[log_entry['resource']] += 1         # Process the log file to get the resource count and increment it
        
        
        ip_counts[log_entry['ip']] += 1                     # Process the log file to get the IP count and increment it
        
        
        status_code = log_entry['status'][0]                # Get the first digit of the HTTP code, increment it
        status_codes[status_code] += 1
    
                                                                                                        # Calculating the percentage, max parameters
    most_requested_resource = max(resource_counts, key=resource_counts.get)
    most_requested_resource_count = resource_counts[most_requested_resource]
    most_requested_resource_percentage = (most_requested_resource_count / total_requests) * 100
    
    most_frequent_ip = max(ip_counts, key=ip_counts.get)
    most_frequent_ip_count = ip_counts[most_frequent_ip]
    most_frequent_ip_percentage = (most_frequent_ip_count / total_requests) * 100
                                                                                                        # Calculating the http codes percentage
    status_code_percentages = {
        code: (count / total_requests) * 100
        for code, count in status_codes.items()
    }

                                                                                                        # Output the statistics to a new file in which the data appends
    with open(output_filename, 'w') as output_file:
        output_file.write(f"Total number of requests: {total_requests}\n")
        output_file.write(f"Total data transmitted: {total_bytes} bytes\n")
        output_file.write(f"Most requested resource: {most_requested_resource} ({most_requested_resource_count} requests)\n")
        output_file.write(f"Percentage of requests for this resource: {most_requested_resource_percentage:.2f}%\n")
        output_file.write(f"Remote host with the most requests: {most_frequent_ip} ({most_frequent_ip_count} requests)\n")
        output_file.write(f"Percentage of requests from this host: {most_frequent_ip_percentage:.2f}%\n")
        
       
        output_file.write("\nPercentage of each class of HTTP status code:\n")
        for code_class, percentage in sorted(status_code_percentages.items()):
            output_file.write(f"{code_class}xx: {percentage:.2f}%\n")

                                                                                                        # Defining the log data parameter on which the statists is run       
log_filename = '2.log'  
output_filename = '2_web_output.log'                                                                    # Defining the file where the output would be generated
calculate_stats(log_filename, output_filename)
