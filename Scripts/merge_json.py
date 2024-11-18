import json
import glob
from pathlib import Path

def merge_json_files():
    merged_data = []
    folder = Path("/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/json_documents")
    # Loop through all JSON files in the current directory
    for filename in folder.glob('*.json'):
        print(filename)
        with open(filename, 'r') as infile:
            # Use extend instead of append to flatten the list
            data = json.load(infile)
            print(type(data))
            entry = {
                'ID': data['ID'],
                'Application': {
                    'SOP': data['SOP'],
                    'Recommendation Letters': data['Recommendation Letters'],
                    'Education': data['Education'],
                    'Publications': data['Publications'],
                    'Faculty Members': data['Faculty Members'],
                    'Research Areas': data['Research Areas']
                }
            }
            merged_data.append(entry)
    
    # Write the merged data to a new JSON file
    with open('/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/json_documents/merged_file.json', 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)

# Call the merging function
merge_json_files()