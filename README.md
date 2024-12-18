# AppReview : PhD Application Reviewer
PhD Application Reviewer that provides rankings of students based on the Professors Research Areas. This is currently limited to Computer Science Department at Columbia University.
This was completed as part of COMS6998 : Introduction to Deep Learning and LLMs based Generative AI at Columbia University during Fall 2024.

## Tutorial for Using the LLM Agent for Application Review

### Prerequisites

The **LLM Agent** is designed to streamline the review of graduate applications by matching applicant data with professor profiles. To ensure compatibility with the existing pipeline, input documents must adhere to specific formats. This tutorial outlines the steps required to preprocess documents, extract information, and perform application reviews using the provided pipeline.

---
### Step 1: Preprocessing Raw Input Documents

1. **Convert PDF Documents to JSON**

    Use the scripts available in the [Scripts/Preprocessing](https://github.com/vbainwala/Grad_Application_Reviewer/tree/main/Scripts/Preprocessing) folder to convert raw input PDF files into JSON format. Ensure the output adheres to the following schema:

```json
[
    {
        "ID": "Unique Identifier for Applicant",
        "Application": {
            "SOP": "String value",
            "Resume": "String value"
        }
    },
    
]
```
2. **Upload to the DocETL Pipeline**

    After generating the JSON files, upload them via the DocETL pipeline UI.
    Use the prompt provided in the `Grad_Application_Review_pipeline.yaml` file to configure the pipeline.

---
### Step 2: Extracting Information from the Pipeline

1.	**Download Extracted Data**

    Once the pipeline has been executed, download the extracted information in CSV format.

2.	**Convert CSV to JSON**

    Use the `csv_to_json.py` script located in the scripts directory to convert the extracted CSV into a JSON file named `applications.json`.

---
### Step 3: Creating Professor Profiles

Define professor profiles in JSON format as follows:

```json
[
  {
    "name": "Professor Name",
    "research_interests": "str containing research interests"
  },
  
]
```
Save the professor profiles for use in the application review process to `professors.json`

---
### Step 4: Performing Application Reviews with the LLM Agent

1.	**Run the Agent Code**

    An interactive IPython Notebook is available to guide you through the matching process. This notebook provides the necessary code for interacting with the agent.

2.	**Agent Workflow**

    The LLM agent is composed of the following modular chains, which break down tasks into smaller components:
    - **Parse Application Chain**: Processes applicant data.
    - **Parse Professor Chain**: Processes professor profiles.
    - **Match and Rank Chain**: Matches applicants with professors and ranks them based on relevance.
    - **Assign Score Chain**: Calculates a score for each match.

---
### Step 5: Output

The final output includes a ranking of applicants for each professor along with an assigned score, enabling an efficient review of applications.

---
#### Additional Notes

- Ensure all dependencies for the scripts and notebook are installed before proceeding.
- Use the provided schemas and pipeline prompts for optimal performance.
- For troubleshooting or further customization, refer to the documentation included with the repository.
