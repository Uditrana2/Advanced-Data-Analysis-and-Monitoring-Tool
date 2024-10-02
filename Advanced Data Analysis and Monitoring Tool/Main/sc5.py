#Main file take input from urls.txt file 
#with visualization 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os
import difflib
from datetime import datetime, timedelta
import glob
import logging
import matplotlib.pyplot as plt

# Read the first URL from urls.txt
with open("urls.txt", "r") as file:
    urls = file.readlines()
if urls:
    url = urls[0].strip()  # Get the first URL
else:
    print("No URLs found in urls.txt")
    exit()

# Retrieve the HTML content via a GET request
response = requests.get(url)
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the page links from anchor tags (<a>)
links = soup.find_all('a')

# Create a list to store the data
data = []
for link in links:
    page_name = link.text.strip()
    web_link = link.get('href')
    if web_link:
        complete_link = urljoin(url, web_link)
        data.append({
            'Service Provider': 'Super Duper Tennis',
            'Page Name': page_name,
            'Complete Web Link': complete_link
        })

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Configure logging
logging.basicConfig(filename='website_monitoring.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log an informational message
logging.info('Website monitoring started.')

# Loop through each row of the DataFrame
for provider, page, link in zip(df['Service Provider'].to_list(), df['Page Name'].to_list(), df['Complete Web Link'].to_list()):
    files = glob.glob(r"{}{}*.txt".format(provider, page))
    files_sorted = sorted(files, key=os.path.getctime, reverse=True)

    if files_sorted and len(files_sorted) > 1:  # Check if the list has at least two files
        current_content = open(files_sorted[0], 'r', encoding="utf-8").readlines()
        prior_content = open(files_sorted[1], 'r', encoding="utf-8").readlines()

        comparison = difflib.context_diff(current_content, prior_content, n=3, lineterm='\n')

        compared_text = "\n".join([line.rstrip() for line in '\n'.join(comparison).splitlines() if line.strip()])
        if compared_text == '':
            change_description = 'No alterations detected on {} compared to {}'.format(datetime.today().strftime('%Y-%m-%d'), files_sorted[1].split('_')[2].split('.')[0])
        else:
            if "We couldn't find the page you were looking for" in compared_text:
                change_description = 'URL modified on {} compared to {}'.format(datetime.today().strftime('%Y-%m-%d'), files_sorted[1].split('_')[2].split('.')[0])
            else:
                change_description = 'Alterations detected on {} compared to {}'.format(datetime.today().strftime('%Y-%m-%d'), files_sorted[1].split('_')[2].split('.')[0])

        # Log the detected changes
        logging.info(change_description)

# Read the log file into a pandas DataFrame
log_data = pd.read_csv('website_monitoring.log', delimiter=' - ', engine='python', header=None, names=['Timestamp', 'Level', 'Message'])

log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'], format='%Y-%m-%d %H:%M:%S,%f')

# Filter the log data to include only INFO level messages
log_data = log_data[log_data['Level'] == 'INFO']

# Aggregate the data by date and count the number of changes per day
changes_per_day = log_data.groupby(log_data['Timestamp'].dt.date).size()

# Ensure that all dates within a specified range are included, with zero changes indicated for dates with no changes
start_date = min(changes_per_day.index)
end_date = max(changes_per_day.index)
date_range = pd.date_range(start=start_date, end=end_date)
changes_per_day = changes_per_day.reindex(date_range, fill_value=0)

# Plot the changes over time
plt.figure(figsize=(10, 6))  # Adjust figure size for better visualization
plt.hlines(0, start_date, end_date, colors='r', linestyles='solid')  # Draw the horizontal line parallel to the x-axis
plt.ylim(-1, 1)  # Set y-axis limits to show the line clearly
plt.xlabel('Date')
plt.ylabel('Number of Changes')
plt.title('Website Content Changes Over Time')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()
