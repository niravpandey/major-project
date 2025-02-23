import requests
import re
import json
from bs4 import BeautifulSoup
import time

def scrape_subject_data(code):
    # URL of the subject page
    url = f"https://handbook.unimelb.edu.au/2025/subjects/{code}"

    # Parse the HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Subject details
    subject_data = {}

    # Extracting details with checks
    subject_data['short_title'] = soup.find('meta', attrs={'name': 'short_title'})['content'] if soup.find('meta', attrs={'name': 'short_title'}) else None
    subject_data['code'] = soup.find('meta', attrs={'name':'code'})['content'] if soup.find('meta', attrs={'name':'code'}) else None
    subject_data['points'] = soup.find('meta', attrs={'name':'points'})['content'] if soup.find('meta', attrs={'name':'points'}) else None
    subject_data['year'] = soup.find('meta', attrs={'name':'year'})['content'] if soup.find('meta', attrs={'name':'year'}) else None
    subject_data['course_type'] = soup.find('meta', attrs={'name':'type'})['content'] if soup.find('meta', attrs={'name':'type'}) else None
    subject_data['level'] = soup.find('meta', attrs={'name':'level'})['content'] if soup.find('meta', attrs={'name':'level'}) else None
    subject_data['delivery'] = soup.find('meta', attrs={'name':'delivery'})['content'] if soup.find('meta', attrs={'name':'delivery'}) else None

    # Availability with checks
    availability_row = soup.find('th', string=lambda text: text and "Availability" in text.strip())
    subject_data['availability'] = [item.text.strip() for item in availability_row.find_next('td').find_all('div')] if availability_row else None

    # Learning Outcomes with checks
    learning_outcomes = soup.find('h2', string="Intended learning outcomes")
    subject_data['outcomes'] = [item.text.strip() for item in learning_outcomes.find_next('ul').find_all('li')] if learning_outcomes else None

    return subject_data

def save_to_json(subject_data, filename="data/subject_data.json"):
    with open(filename, 'w') as f:
        json.dump(subject_data, f, indent=4)
start = time.time()
codes = [
    "COMP10002", "MATH10012", "PSYC10003", "BIOL10003", "MGMT10001", 
    "CHEM10009", "PHIL10005", "ENVS10001", "LAW1101", "STAT10001", 
    "ARTS10001", "ECON10004", "MUSI10005", "ACCT10001", "SOCI10002", 
    "GEOG10002", "ANTH10001", "PHYS10001", "LANG10001", "EDUC10001", 
    "MDHS10001", "NURS10001", "ENGR10001", "VART10001", "LING10001", 
    "FINA10001", "CIVL10001", "ARCH10001", "EDUC10002", "CHEM10001", 
    "MATH10001", "PHIL10006", "PSYC10002", "ACCT10002", "FINS10001"
]
all_subject_data = []

for code in codes:
    subject_data = scrape_subject_data(code)
    all_subject_data.append(subject_data)

# Save all subject data into a single JSON file
with open('data/all_subjects_data.json', 'w') as f:
    json.dump(all_subject_data, f, indent=4)
end = time.time()

elapsed = end-start

print(f"{elapsed:0.2f}s for {len(codes)} items!")