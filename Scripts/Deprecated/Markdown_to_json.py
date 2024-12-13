import json
import re

# Path to the input markdown file
file_path = '/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Dataset/Outputs/final_scores.md'

# Initialize the data structure
professor_data = {}

# Variables to keep track of the current professor and applicant details
current_professor = None
current_applicant = None
justification_flag = False
justification_data = {}

# Read the markdown content
with open(file_path, 'r') as file:
    markdown_content = file.readlines()

# Parsing the markdown content
for line in markdown_content:
    line = line.strip()
    
    # Check for professor name (handles both formats with and without **)
    professor_match = re.match(r'### \d+\.\s(?:\*\*(.+?)\*\*|(.+))', line)
    if professor_match:
        if current_professor and current_applicant:  # Save last applicant
            current_applicant["Justification"] = justification_data
            professor_data[current_professor].append(current_applicant)
            current_applicant = None

        # Extract professor name (either group 1 or 2 will match)
        current_professor = professor_match.group(1) or professor_match.group(2)
        professor_data[current_professor] = []
        continue
    
    # Check for applicant ID
    applicant_match = re.match(r'#### Applicant ID:\s(\d+)', line)
    if applicant_match:
        if current_applicant:  # Save previous applicant's data
            current_applicant["Justification"] = justification_data
            professor_data[current_professor].append(current_applicant)

        current_applicant = {
            "Applicant ID": applicant_match.group(1)
        }
        justification_data = {}  # Reset justification
        justification_flag = False
        continue
    
    # Check for scoring details
    score_match = re.match(r'- \*\*(.+?):\*\*\s(.+)', line)
    if score_match and current_applicant is not None:
        score_type, score_value = score_match.groups()
        if "Score" in score_type:
            try:
                score_value = float(score_value)
            except ValueError:
                pass  # Keep as string if it cannot be converted to a float
        current_applicant[score_type] = score_value
        continue
    
    # Check for justification section
    if line.startswith('- **Justification:**'):
        justification_flag = True
        continue
    
    # Parse justification details
    if justification_flag:
        justification_match = re.match(r'- \*\*(.+?):\*\*\s(.+)', line)
        if justification_match:
            justification_key, justification_value = justification_match.groups()
            justification_data[justification_key] = justification_value

# Save the last applicant's data
if current_professor and current_applicant:
    current_applicant["Justification"] = justification_data
    professor_data[current_professor].append(current_applicant)

# Save as JSON
output_path = '/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Dataset/Outputs/professor_applicants.json'
with open(output_path, 'w') as json_file:
    json.dump(professor_data, json_file, indent=4)

print(f"JSON file saved at: {output_path}")