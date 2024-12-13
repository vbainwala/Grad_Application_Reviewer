import requests
from bs4 import BeautifulSoup
import json

# URL of the Columbia CS Faculty webpage
url = "https://www.cs.columbia.edu/people/faculty/"

def scrape_columbia_cs_faculty(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract professor details
        faculty_data = []
        faculty_sections = soup.find_all('div', class_='faculty-details')
        
        for faculty in faculty_sections:
            # Extract professor name
            name_tag = faculty.find('span', class_='faculty-name')
            name = name_tag.get_text(strip=True) if name_tag else "Name not found"
            
            # Extract research interests
            interests_tag = faculty.find('div',class_='faculty-interests')  # Adjust this if interests have a specific class or tag
            interests = interests_tag.get_text(strip=True) if interests_tag else "Interests not listed"
            
            faculty_data.append({'name': name, 'interests': interests})
        
        return faculty_data
    
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

# Run the scraper and print the results
faculty_list = scrape_columbia_cs_faculty(url)

professors = []

for faculty in faculty_list:
    faculty_details = {}
    faculty_details['name'] = ' '.join(faculty['name'].split(',')[::-1])
    faculty_details['research_interests'] = faculty['interests'].split(':')[-1]
    # print(faculty_details)
    faculty_details['name'] = faculty_details['name'].strip()
    faculty_details['research_interests'] = faculty_details['research_interests'].strip()
    professors.append(faculty_details)
    # print(f"Name: {faculty['name']}")
    # print(f"Interests: {faculty['interests']}")
    # print("-" * 40)

json_object = json.dumps(professors, indent = 2)

with open('/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Dataset/Input_documents/Current/professors.json', 'w') as file:
    file.write(json_object)