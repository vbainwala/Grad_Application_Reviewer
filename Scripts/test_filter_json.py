import json
import re
from typing import Dict, List

def search_document(document: Dict, pattern: str) -> List[Dict]:
    """
    Search through all pages in a document for a regex pattern.
    
    Args:
        document (Dict): JSON document with the specified structure
        pattern (str): Regex pattern to search for
    
    Returns:
        List[Dict]: List of matches with page numbers and matched content
    """
    matches = []
    
    # Compile regex pattern for better performance
    regex = re.compile(pattern)
    
    # Search through each page
    for page in document['pages']:
        page_matches = regex.finditer(page['content'])
        
        # Add each match to results
        for match in page_matches:
            matches.append({
                'page_number': page['page_number'],
                'match': match.group(),
                'start_pos': match.start(),
                'end_pos': match.end(),
                'context': page['content'][max(0, match.start()-50):match.end()+50]  # Include some context
            })
    
    return matches

# Example usage
if __name__ == "__main__":
    # Sample document
    document = {
        "document_name": "document.pdf",
        "total_pages": 55,
        "pages": [
            {
                "page_number": 1,
                "content": "This is a sample text with some email@example.com and another email@test.com",
                "metadata": {
                    "width": 612,
                    "height": 792
                }
            },
            {
                "page_number": 2,
                "content": "More content with contact@domain.com",
                "metadata": {
                    "width": 612,
                    "height": 792
                }
            }
        ]
    }
    
    # Search for email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    results = search_document(document, email_pattern)
    
    # Print results
    for match in results:
        print(f"Found on page {match['page_number']}: {match['match']}")
        print(f"Context: ...{match['context']}...")
        print("-" * 50)