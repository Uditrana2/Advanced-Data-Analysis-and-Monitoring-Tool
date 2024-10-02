import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import glob
import smtplib
import os
import difflib
from datetime import date

# URL of the home page
url = 'https://www.superdupertennis.com/'

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

# Loop through each row of the DataFrame
for provider, page, link in zip(df['Service Provider'].to_list(), df['Page Name'].to_list(), df['Complete Web Link'].to_list()):
    files = glob.glob(r"PATH\{}{}*.txt".format(provider, page))
    files_sorted = sorted(files, key=os.path.getctime, reverse=True)
    print("Files found:", files_sorted)  # Add this line to check the contents of files_sorted
    
    if files_sorted:  # Check if the list is not empty
        current_content = open(files_sorted[0], 'r', encoding="utf-8").readlines()
        prior_content = open(files_sorted[1], 'r', encoding="utf-8").readlines()

        comparison = difflib.context_diff(current_content, prior_content, n=3, lineterm='\n')

        compared_text = "\n".join([line.rstrip() for line in '\n'.join(comparison).splitlines() if line.strip()])
        if compared_text == '':
            change_description = 'No alterations detected on {} compared to {}'.format(date.today().strftime('%Y-%m-%d'), files_sorted[1].split('_')[2].split('.')[0])
        else:
            if "We couldn't find the page you were looking for" in compared_text:
                change_description = 'URL modified on {} compared to {}'.format(date.today().strftime('%Y-%m-%d'), files_sorted[1].split('_')[2].split('.')[0])
            else:
                change_description = 'Alterations detected on {} compared to {}'.format(date.today().strftime('%Y-%m-%d'), files_sorted[1].split('_')[2].split('.')[0])

        temp_log = pd.DataFrame({'Service Provider': pd.Series(provider), 'Section': pd.Series(page), 'Changes': pd.Series(change_description), 'Link': pd.Series(link)})
        change_logs = change_logs.append(temp_log)

# Send email notification

# Configure logging
import logging

logging.basicConfig(filename='website_monitoring.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log an informational message
logging.info('Website monitoring started.')

# Log the detected changes
logging.info('Changes detected on {}: Updated content on homepage.'.format(date.today().strftime('%Y-%m-%d')))

# Log an error message
logging.error('Error occurred while retrieving website content.')

# Read the log file into a pandas DataFrame
log_data = pd.read_csv('website_monitoring.log', delimiter=' - ', header=None, names=['Timestamp', 'Level', 'Message'])

# Convert the Timestamp column to datetime format
log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Group the data by date and count the number of changes per day
changes_per_day = log_data[log_data['Level'] == 'INFO'].groupby(log_data['Timestamp'].dt.date).size()
import pandas as pd

# Read the log file into a pandas DataFrame
log_data = pd.read_csv('website_monitoring.log', delimiter=' - ', engine='python', header=None, names=['Timestamp', 'Level', 'Message'])


log_data['Timestamp'] = pd.to_datetime(log_data['Timestamp'], format='%Y-%m-%d, %H:%M:%S')
# Plot the changes over time
import matplotlib.pyplot as plt

plt.plot(changes_per_day.index, changes_per_day.values)
plt.xlabel('Date')
plt.ylabel('Number of Changes')
plt.title('Website Content Changes Over Time')
plt.xticks(rotation=45)
plt.show()
