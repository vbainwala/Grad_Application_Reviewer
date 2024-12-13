import pymupdf
import fitz
import pathlib
import pymupdf4llm

# md_text = pymupdf4llm.to_markdown("/Users/vareeshbainwala/Documents/Phd_Application_Review/Input_Documents/Liu_Jiaxiang_Jerry_.pdf")

# doc = fitz.open("/Users/vareeshbainwala/Documents/Phd_Application_Review/Input_Documents/Liu_Jiaxiang_Jerry_.pdf")

# for page in doc:
#     text = page.get_text()
#     print(text)

# print(md_text)

# pathlib.Path("/Users/vareeshbainwala/Documents/Phd_Application_Review/Input_Documents/jerry.md").write_bytes(md_text.encode())


with open('/Users/vareeshbainwala/Documents/Phd_Application_Review/Input_Documents/jerry.md', 'r', encoding='utf-8') as file:
    lines = file.readlines()

regex_start = "recommend this applicant"
regex_intermediate = "Reference Form"
regex_end = "Publications (optional)"
indexes = []
recommendation_letter = []
count = 0
for i in range(len(lines)):
    if regex_start in lines[i]:
        count+=1
        
    
for index in indexes:
    pass

# print(lines[696])
    
print(indexes)