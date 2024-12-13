# Filtering out necessary information from the JSON to create a document

import json
from typing import Dict, List, Optional
import os
import re


input_path = "/Users/vareeshbainwala/Documents/Phd_Application_Review/123456.json"
output_path = "/Users/vareeshbainwala/Documents/Phd_Application_Review/"

regex = r"ID: ([0-9]+)"

#Read json input
with open(input_path, 'r') as file:
    data = json.load(file)

# print(type(data['pages'][0]['content']))
test_str = data['pages'][0]['content']

matches = re.findall(regex, test_str, re.MULTILINE)

print(type(matches[0]))