# import requests
# from bs4 import BeautifulSoup

# url = "http://www.eugenewu.net/"
# page = requests.get(url)

# soup = BeautifulSoup(page.content, 'html.parser')
# # print(soup)

# # Find elements by tag
# elements = soup.find_all('div', class_='col-md-6')
# # print(elements)

# # Extract text
# for element in elements:
#     text = element.text
#     if "Bio" in text:
#         print(text)
#     # Process the extracted text

# try:
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Process the response
#         print("Success")
#     else:
#         print(f"Failed with status code: {response.status_code}")
# except Exception as e:
#     print(f"Error occurred: {e}")

import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_professor_website(url):
    """
    Scrape professor's website to extract bio information based on specific HTML structure
    
    Parameters:
    url (str): URL of the professor's website
    
    Returns:
    dict: Dictionary containing bio information
    """
    try:
        # Send HTTP request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize dictionary to store results
        results = {
            'bio': [],
            'awards': '',
            'lab_info': ''
        }
        
        # Find the main div containing bio information
        bio_div = soup.find('div', class_='col-md-6')
        
        if bio_div:
            # Extract main bio paragraphs
            bio_paragraphs = bio_div.find_all('p')
            
            for p in bio_paragraphs:
                # Clean the text by removing extra whitespace
                text = ' '.join(p.get_text().strip().split())
                
                # Categorize the content based on context
                if "Eugene Wu is" in text:
                    results['bio'].append(text)
                elif "received" in text and "award" in text.lower():
                    results['awards'] = text
                elif "Joining The Lab" in text:
                    results['lab_info'] = text
        
        # Clean up the results
        results['bio'] = '\n'.join(results['bio'])
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None
    except Exception as e:
        print(f"Error parsing the website: {e}")
        return None

# Example usage
if __name__ == "__main__":
    url = "http://www.eugenewu.net/"
    results = scrape_professor_website(url)
    
    if results:
        # print("Bio:")
        # print(results['bio'])
        # print("\nAwards and Recognition:")
        # print(results['awards'])
        # print("\nLab Information:")
        # print(results['lab_info'])

        eugene_details = json.dumps(results)

        print(eugene_details)