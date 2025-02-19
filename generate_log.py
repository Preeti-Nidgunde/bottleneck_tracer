import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Number of log entries
num_entries = 200

# Start and end times for log entries
start_time = datetime(2024, 10, 29, 10, 0, 0)
end_time = datetime(2024, 10, 29, 12, 0, 0)  # 2-hour window

# Generate timestamps
timestamps = [start_time + timedelta(seconds=random.randint(0, int((end_time - start_time).total_seconds()))) for _ in range(num_entries)]
timestamps.sort() #Important: Sort the timestamps

# Possible request methods
methods = ['GET', 'POST', 'PUT', 'DELETE']

# Possible URLs (simplified)
urls = ['/home', '/products', '/login', '/api/data', '/contact', '/about', '/search']

# Possible response codes
codes = [200, 200, 200, 200, 200, 200, 200, 404, 500, 500] #Added some error codes

# Generate data
data = {
    'timestamp': timestamps,
    'request_method': [random.choice(methods) for _ in range(num_entries)],
    'request_url': [random.choice(urls) for _ in range(num_entries)],
    'response_code': [random.choice(codes) for _ in range(num_entries)],
    'response_time': [random.randint(50, 2500) for _ in range(num_entries)]  # Response times in milliseconds
}

df = pd.DataFrame(data)

# Save to CSV (access.log)
df.to_csv('api_logs.csv', index=False, header=['timestamp', 'request_method', 'request_url', 'response_code', 'response_time'])  # No header row as per your request

print("API log file generated successfully.")