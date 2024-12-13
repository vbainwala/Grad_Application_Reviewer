import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # try:
        # Initialize an empty list to store the JSON objects
        json_data = []

        # Open the CSV file and read it
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Process each row in the CSV file
            for row in csv_reader:
                experience = json.loads(row['Experience'])
                if row['Publications']:
                  publications = row['Publications']
                else:
                  publications = ""
                education = row['Education']
                applicant_id = row['ID']

                # Construct the JSON object for the current row
                json_object = {
                    "applicant_id": applicant_id,
                    "experience": experience,
                    "publications": publications,
                    "education": education
                }

                # Append the JSON object to the list
                json_data.append(json_object)

        # Write the JSON data to the output file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"JSON file created successfully at: {json_file_path}")

    # except Exception as e:
    #     print(f"An error occurred: {e}")

# Input CSV file path and output JSON file path
csv_file_path = 'iteration_2_docetl.csv'  # Replace with your input CSV file path
json_file_path = 'applications.json'  # Replace with your desired JSON file path

# Convert CSV to JSON
csv_to_json(csv_file_path, json_file_path)

with open('applications.json','r') as json_file:
    json_data = json.load(json_file)

