import json
import re
import os
from collections import defaultdict
from pathlib import Path


def extract_numeric_part(filename):
    """
    Extract numeric characters from a filename.
    
    Args:
        filename (str): The filename to process.
    
    Returns:
        str: The numeric part of the filename.
    """
    match = re.search(r'\d+', filename)
    return match.group() if match else None

def read_application_data(input_file):
    with open(input_file,'r') as file:
        application_data = json.load(file)

    return application_data

def read_resume_data(input_file):
    with open(input_file, 'r') as file:
        resume_data = json.load(file)

    return resume_data

def default_candidate():
    return {
        "ID": None,  # Default value could be None or an empty string if ID is a string
        "SOP": "",  # Statement of Purpose, initialized as an empty string
        "Resume": ""
        # "Publications": [],  # List to store publication entries
        # "Education": {},
        # "Faculty Members": [],  # List for storing faculty member names or details
        # "Recommendation Letters": [] , # List for storing recommendation letters
        # "Research Areas": []
    }

def get_personal_statement(application_data):
    sop_pattern = "Personal Statement"
    personal_statement = []
    value = 1111
    for page in application_data['pages']:
        if sop_pattern in page['content']:
            page_content = page['content'].split('\n')
            personal_statement += page_content[1:-1]
    
    return personal_statement

def get_education_history(application_data):
    graduate_info = {}
    undergrad_info = {}
    education_pattern = "Academic History"

    for page in application_data['pages']:
        if education_pattern in page['content']:
            content = page['content'].split('\n')[2:]
            for line in content:
                line = line.strip()
                # Determine the section based on the line
                if "Graduate" in line:
                    current_section = "Graduate"
                elif "Undergraduate" in line:
                    current_section = "Undergraduate"

                # Extract information based on keywords
                if "Institution" in line:
                    institution = line.split("Institution")[1].strip()
                    if current_section == "Graduate":
                        graduate_info["Institution"] = institution.split(" (")[0].strip()
                    elif current_section == "Undergraduate":
                        undergrad_info["Institution"] = institution.split(" (")[0].strip()
                
                elif "Degree" in line:
                    degree = line.split("Degree")[1].split(":")[0].strip()
                    if current_section == "Graduate":
                        graduate_info["Degree"] = degree
                    elif current_section == "Undergraduate":
                        undergrad_info["Degree"] = degree

                elif "Major" in line:
                    major = line.split("Major")[1].strip()
                    if current_section == "Graduate":
                        graduate_info["Major"] = major
                    elif current_section == "Undergraduate":
                        undergrad_info["Major"] = major

                elif "GPA" in line and "Recalculated" in line:
                    gpa = line.split("Recalculated GPA")[1].split("/")[0].strip()
                    if current_section == "Graduate":
                        graduate_info["GPA"] = gpa
                    elif current_section == "Undergraduate":
                        undergrad_info["GPA"] = gpa
                elif "GPA" in line:
                    gpa = line.split("GPA")[1].split("/")[0].strip()
                    if current_section == "Graduate":
                        graduate_info["GPA"] = gpa
                    elif current_section == "Undergraduate":
                        undergrad_info["GPA"] = gpa
    
    return graduate_info, undergrad_info

def get_faculty_names(application_data):
    faculty_pattern = "faculty members"
    for page in application_data['pages']:
        if faculty_pattern in page['content']:
            print(page['page_number'])

def get_research_areas(application_data):
    available_research_areas = ['Artificial Intelligence','Augmented Reality and Virtual Reality','Biomedical Informatics and Computational Biology',
                                'Computer Architecture','Databases and Data Management','Design Automation','Embedded Systems','Graphics',
                                'Human–Computer Interaction','Information Retrieval','Machine Learning','Machine Learning Systems','Natural Language Processing',
                                'Network Systems','Programming Languages','Robotics','Security and Privacy','Software Engineering','Software Systems',
                                'Speech Language Processing','Theory','Vision']
    research_pattern = "research areas"
    interest_areas = []
    for page in application_data['pages']:
        if research_pattern in page['content']:
            for area in available_research_areas:
                if area in page['content']:
                    interest_areas.append(area)

    return interest_areas

def get_recommendation_letters(application_data):
    recommendation_letters = defaultdict(list)
    recommendation_pattern = "I recommend this applicant "
    recommendation_end_pattern = "Form Title Publications"
    recommendation_start = []
    recommendation_end = []
    for page in application_data['pages']:
        if recommendation_pattern in page['content']:
           recommendation_start.append(page['page_number']+1)
        if recommendation_end_pattern in page['content']:
            recommendation_end.append(page['page_number']-1)

    recommendation_end.insert(0,recommendation_start[-1]-2)
    # print(recommendation_start)
    # print(recommendation_end)

    n = len(recommendation_start)
    # print(n)
    for i in range(n):
        letters = ""
        for page_number in range(len(application_data['pages'])):
            if page_number+1 >= recommendation_start[i] and page_number+1 <= recommendation_end[i]-1 and i==0:
                content = application_data['pages'][page_number]['content']
                letters+=' '.join(content.split('\n')[1:-1])
            elif page_number+1 >= recommendation_start[i] and page_number+1 <=recommendation_end[i] and i==1:
                # print(page_number)
                content = application_data['pages'][page_number]['content']
                letters+=' '.join(content.split('\n')[1:-1])
        
        recommendation_letters[i+1] = letters

    return recommendation_letters

def get_publications(application_data):
    paper_pattern = "Publication Title"
    regex_publication = r"Publication\s+Title\s+(.*?)\s+Publication"
    publications = []
    for page in application_data['pages']:
        if paper_pattern in page['content']:
            content = page['content'].split('\n')
            content = ' '.join(content)
            # print(content)
            matches = re.findall(regex_publication,content)
            for match in matches:
                publications.append(match)
    return publications

def get_resume(resume_data):
    resume_pattern = "Resume"
    resume = []
    for page in resume_data['pages']:
        if resume_pattern in page['content']:
            page_content = page['content'].split('\n')
            resume+= page_content[1:-1]
    return resume

if __name__ == "__main__":

    # Provide the input path to JSON Documents
    # sop_folder = Path("/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Personal_statement_Json")
    # resume_folder = Path("/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Resumes_Json")
    input_folder = Path("/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Dataset/Processed Files/Test")
    output_folder = Path("/Users/vareeshbainwala/Documents/Grad_Application_Reviewer/Dataset/Processed_Json/Test")

    # files_sop = sorted(os.listdir(sop_folder))
    # files_resume = sorted(os.listdir(resume_folder))
    # files_sop.remove('.DS_Store')
    files = sorted(os.listdir(input_folder))
    # print(files_sop, files_resume)

    # files = zip(files_sop, files_resume)
    # print(files)
    for item in files:
        numeric = extract_numeric_part(item)
        relevant_data = default_candidate()
        # Get the Personal Statement of Applicant
        sop_data = read_application_data(os.path.join(input_folder, item))
        personal_statement = get_personal_statement(sop_data)
        relevant_data['SOP'] = ' '.join(personal_statement)
        
        #Get the Resume of the applicant
        resume_data = read_resume_data(os.path.join(input_folder, item))
        resume = get_resume(resume_data)
        relevant_data['Resume'] = ' '.join(resume)

        relevant_data['ID'] = numeric

        new_filename = output_folder / f"processed_{numeric}.json"
            
        # Write the processed data to a new JSON file
        with open(new_filename, 'w', encoding='utf-8') as f:
            json.dump(relevant_data, f, indent=4)
            
        print(f"Successfully processed {numeric}")
    
    # for file_sop in files_sop:
    #     numeric1 = extract_numeric_part(file_sop)
    #     if numeric1 is None:
    #         continue

    #     for file_resume in files_resume:
    #         numeric2 = extract_numeric_part(file_resume)
    #         if numeric2

    # for file_path in folder.glob('*.json'):
    #     try:
    #         # Read the JSON file
    #         relevant_data = default_candidate()
    #         if "sop" in file_path:
    #             personal_statement_data = read_application_data(file_path)
    #             personal_statement = get_personal_statement(personal_statement_data)
    #             # print(personal_statement)
    #             relevant_data['SOP'] = ' '.join(personal_statement)

    #         elif "resumes" in file_path:
    #             resume_data = read_resume_data(file_path)
    #             resume = get_resume(resume_data)
    #             relevant_data['Resume'] = ' '.join(resume)

    #         relevant_data['ID'] = file_path.name.replace('.json','')
    #         # Create the new filename
    #         new_filename = folder / f"processed_{file_path.name}"
            
    #         # Write the processed data to a new JSON file
    #         with open(new_filename, 'w', encoding='utf-8') as f:
    #             json.dump(relevant_data, f, indent=4)
                
    #         print(f"Successfully processed {file_path.name}")
        
    #     except json.JSONDecodeError:
    #         print(f"Error: {file_path.name} is not a valid JSON file")
    #     except Exception as e:
    #         print(f"Error processing {file_path.name}: {str(e)}")