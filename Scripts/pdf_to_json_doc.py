import pdfplumber
import json
from typing import Dict, List, Optional
import os
import re

def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    """
    Extract content from a PDF file and organize it by pages.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing page content
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    pages_content = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    page_data = {
                        "page_number": page_num,
                        "content": text.strip(),
                        "metadata": {
                            "width": page.width,
                            "height": page.height
                        }
                    }
                    pages_content.append(page_data)
                    
        return pages_content
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def pdf_to_json(pdf_path: str, output_path: Optional[str] = None) -> str:
    """
    Convert PDF content to JSON format and optionally save to file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path to save the JSON output
        
    Returns:
        str: JSON string of the PDF content
    """
    # try:
    # Extract content from PDF
    pages_content = extract_pdf_content(pdf_path)
    
    # Create JSON structure
    pdf_data = {
        "document_name": os.path.basename(pdf_path),
        "total_pages": len(pages_content),
        "pages": pages_content
    }

    # Convert to JSON string
    json_output = json.dumps(pdf_data, indent=2, ensure_ascii=False)
    json_input = json.loads(json_output)

    user_id_regex = r"ID: ([0-9]+)"
    user_id_string = json_input['pages'][0]['content']
    # print(user_id_string)
    matches = re.findall(user_id_regex, user_id_string, re.MULTILINE)
    unique_user_id = matches[0]
    # print(type(unique_user_id))

    # Save to file if output path is provided
    output_path = output_path+f"/{unique_user_id}.json"
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
            
    return json_output
        
    # except Exception as e:
    #     raise Exception(f"Conversion failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Convert PDF to JSON
        result = pdf_to_json(
            pdf_path="/Users/vareeshbainwala/Documents/Phd_Application_Review/Liu_Jiaxiang_Jerry_.pdf",
            output_path="/Users/vareeshbainwala/Documents/Phd_Application_Review/"
        )
        print("Conversion successful!")
        
    except Exception as e:
        print(f"Error: {str(e)}")