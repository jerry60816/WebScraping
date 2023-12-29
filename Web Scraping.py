import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Scrape data
URL = 'https://www.basketball-reference.com/leagues/NBA_2023_per_game.html'
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'id': 'per_game_stats'})

# Extract headers
headers = [th.getText() for th in table.find_all('tr', limit=2)[0].find_all('th')]
headers = headers[1:]  # Remove the rank column

# Extract rows
rows = table.find_all('tr')[1:]
player_stats = [[td.getText() for td in rows[i].find_all('td')]
                for i in range(len(rows))]

# Write to CSV
with open('NBA_Player_Stats.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(player_stats)

# Read data for analysis
df = pd.read_csv('NBA_Player_Stats.csv')

# Convert 3P% to numeric and handle missing values
df['3P%'] = pd.to_numeric(df['3P%'], errors='coerce')
df = df.dropna(subset=['3P%'])

# Analysis: Calculate Average 3P%
average_3p = df['3P%'].mean()
print(f"Average 3P%: {average_3p}")

# Visualization: Histogram of 3P%
plt.hist(df['3P%'], bins=20, color='blue', alpha=0.7)
plt.xlabel('3-Point Percentage')
plt.ylabel('Number of Players')
plt.title('Distribution of 3-Point Percentage in NBA')
plt.axvline(average_3p, color='red', linestyle='dashed', linewidth=1)
plt.show()
