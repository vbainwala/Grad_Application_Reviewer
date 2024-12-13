from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import json

# Tool: Load applications
def load_applications(file_path):
    """Loads a JSON file containing a list of applications."""
    with open(file_path, "r") as f:
        applications = json.load(f)
    return applications

# Tool: Load professor profiles
def load_professor_profiles(file_path):
    """Loads a JSON file containing professor profiles."""
    with open(file_path, "r") as f:
        professor_profiles = json.load(f)
    return professor_profiles

# Define tools
load_applications_tool = Tool(
    name="load_applications",
    func=load_applications,
    description="Loads a JSON file containing applications with their research areas and applicants' information."
)

load_professor_profiles_tool = Tool(
    name="load_professor_profiles",
    func=load_professor_profiles,
    description="Loads a JSON file containing professor profiles, including their research interests and requirements for students."
)

# Initialize the LLM
llm = OpenAI(temperature=0.7)

# Define prompt for ranking
prompt_template = PromptTemplate(
    input_variables=["applications", "professor_profiles"],
    template=(
        "You are an academic assistant tasked with matching PhD applications to professors based on their research areas and requirements. "
        "For each professor, rank the applicants out of 10 based on their suitability and return an ordered list of applicants for each professor.\n\n"
        "Applications: {applications}\n\n"
        "Professor Profiles: {professor_profiles}\n\n"
        "Provide your results in the format: \n"
        "Professor Name: [\"Applicant_ID (Score)\", ...]"
    )
)

# Define agent
agent = initialize_agent(
    tools=[load_applications_tool, load_professor_profiles_tool],
    llm=llm,
    agent="zero-shot-react-description"
)

# Main execution function
def match_students_to_professors(applications_path, professor_profiles_path):
    # Load applications and professor profiles using tools
    applications = load_applications(applications_path)
    professor_profiles = load_professor_profiles(professor_profiles_path)

    # Run the agent with the loaded data
    result = agent.run(
        prompt_template.format(
            applications=json.dumps(applications),
            professor_profiles=json.dumps(professor_profiles)
        )
    )

    return result

# Example usage
if __name__ == "__main__":
    applications_file = "applications.json"
    professor_profiles_file = "professor_profiles.json"

    rankings = match_students_to_professors(applications_file, professor_profiles_file)
    print(rankings)
