import sys
import pandas as pd
from datetime import datetime
from time import perf_counter_ns
import gzip

def analyze(start_date,start_hour,end_date,end_hour):
    data = pd.read_csv("2022_place_canvas_history.csv.gzip", compression='gzip', parse_dates=['timestamp'])

if len(sys.argv) != 5:
    print("Usage: python analyze_rplace.py <start_hour> <end_hour>")
    sys.exit(1)
# start_datetime = datetime.strptime(f"{sys.argv[1]} {sys.argv[2]:02}:00:00", "%Y-%m-%d %H:%M:%S")
# end_datetime = datetime.strptime(f"{sys.argv[3]} {sys.argv[4]:02}:00:00", "%Y-%m-%d %H:%M:%S")

start_datetime = pd.to_datetime(f"{sys.argv[1]} {sys.argv[2]}:00:00", utc=True)
end_datetime = pd.to_datetime(f"{sys.argv[3]} {sys.argv[4]}:00:00", utc=True)
timeframe_data = []

start_timer = perf_counter_ns()
# data = pd.read_csv("2022_place_canvas_history.csv.gzip", compression='gzip', \
#                     parse_dates=['timestamp'], usecols=["timestamp","pixel_color","coordinate"], chunksize=10000)
data = []
for chunk in pd.read_csv("2022_place_canvas_history.csv.gzip", compression='gzip', \
                    parse_dates=['timestamp'], usecols=["timestamp","pixel_color","coordinate"], chunksize=1000000):
                    chunk['timestamp'] = pd.to_datetime(chunk['timestamp'], errors='coerce', utc=True)

                    filtered_chunk = chunk[(chunk['timestamp'] >= start_datetime) & 
                           (chunk['timestamp'] < end_datetime)]
                    data.append(filtered_chunk)
                    print("hi")
data = pd.concat(data)
filtered_data = data[(data['timestamp'] >= start_datetime) & (data['timestamp'] <= end_datetime)]

most_color = filtered_data['pixel_color'].value_counts().sort_index().idxmax()
most_location = filtered_data['coordinate'].value_counts().sort_index().idxmax()
end_timer = perf_counter_ns()
timer = end_timer - start_timer

filtered_data.to_csv("logs.csv", index=False)
print("Timeframe:", sys.argv[1], sys.argv[2], " o", sys.argv[3], sys.argv[4])
print("Execution Time:",timer/1000000, "ms")
print("Most placed color:", most_color)
print("Most placed Pixel Location:", most_location)
            

