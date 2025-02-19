import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For better visualizations
import numpy as np

log_file = "api_logs.csv"  

try:
    chunksize = 100000  # Adjust chunk size as needed
    log_data_chunks = []
    for chunk in pd.read_csv(log_file, names=['timestamp', 'request_method', 'request_url', 'response_code', 'response_time'], chunksize=chunksize, error_bad_lines=False): #error_bad_lines skips lines with parsing errors
        log_data_chunks.append(chunk)

    log_data = pd.concat(log_data_chunks, ignore_index=True) 

    log_data['timestamp'] = pd.to_datetime(log_data['timestamp'], errors='coerce') #errors='coerce' will set invalid timestamps to NaT (Not a Time)
    log_data.dropna(subset=['timestamp'], inplace=True) #Remove rows with invalid timestamps


except FileNotFoundError:
    print(f"Error: Log file '{log_file}' not found.")
    exit()
except pd.errors.ParserError:
    print(f"Error: Could not parse the log file. Check the format.")
    exit()


# 2. Data Cleaning and Preprocessing
log_data.dropna(inplace=True)  

# Convert response_time to numeric, handling potential errors
log_data['response_time'] = pd.to_numeric(log_data['response_time'], errors='coerce')
log_data.dropna(subset=['response_time'], inplace=True)  # Remove rows with non-numeric response times



# 3. Analysis: Identify Slow Requests (Configurable threshold)
slow_request_threshold = int(input("Enter the threshold for slow requests (in milliseconds): "))

slow_requests = log_data[log_data['response_time'] > slow_request_threshold]

# 4. Aggregation and Analysis (More detailed)
top_n = int(input("Enter the number of top slow URLs to display: "))
average_response_time_by_url = log_data.groupby('request_url')['response_time'].mean().sort_values(ascending=False).head(top_n)

# Number of slow requests by URL (top N)
slow_request_count_by_url = slow_requests.groupby('request_url')['response_time'].count().sort_values(ascending=False).head(top_n)


# 5. Visualization (Improved with Seaborn)
plt.figure(figsize=(15, 8))  # Larger figure for better readability

# Plot average response time by URL
plt.subplot(2, 1, 1)
sns.barplot(x=average_response_time_by_url.index, y=average_response_time_by_url.values)
plt.title('Average Response Time by URL')
plt.ylabel('Response Time (ms)')
plt.xticks(rotation=45, ha='right') #Rotate x-axis labels for readability

# Plot the number of slow requests by URL
plt.subplot(2, 1, 2)
sns.barplot(x=slow_request_count_by_url.index, y=slow_request_count_by_url.values, color='orange')
plt.title('Number of Slow Requests by URL')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# 6. Further Analysis (Enhanced)
percentage_slow_requests = (len(slow_requests) / len(log_data)) * 100
print(f"Percentage of slow requests: {percentage_slow_requests:.2f}%")

# Response time distribution (histogram with KDE)
plt.figure(figsize=(10, 6))
sns.histplot(log_data['response_time'], kde=True, bins=50) #Added KDE
plt.title('Response Time Distribution')
plt.xlabel('Response Time (ms)')
plt.ylabel('Frequency')
plt.show()

# Time series analysis (example - hourly average response time)
log_data['hour'] = log_data['timestamp'].dt.hour
hourly_average_response = log_data.groupby('hour')['response_time'].mean()

plt.figure(figsize=(10,6))
plt.plot(hourly_average_response.index, hourly_average_response.values)
plt.title('Hourly Average Response Time')
plt.xlabel('Hour of Day')
plt.ylabel('Average Response Time (ms)')
plt.xticks(range(24)) #Set x-axis ticks for each hour
plt.grid(True)
plt.show()
