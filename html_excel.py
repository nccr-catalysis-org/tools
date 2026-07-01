#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 18:11:45 2026

@author: nr
"""

import re
import os
import pandas as pd
from bs4 import BeautifulSoup

def html_to_excel(html_file, excel_file):
    """
    Parses an HTML file with a list of links and descriptions,
    and extracts the data into an Excel spreadsheet.
    """
    if not os.path.exists(html_file):
        print(f"Error: The file '{html_file}' does not exist.")
        return

    print(f"Parsing '{html_file}'...")
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    data = []
    
    # Find all list items inside the unordered list
    for li in soup.find_all('li'):
        a_tag = li.find('a')
        if not a_tag:
            continue
            
        url = a_tag.get('href', '').strip()
        name = a_tag.get_text(strip=True)
        
        # Get the full text of the li, and strip out the name and separator
        # to isolate the description cleanly.
        full_text = li.get_text()
        # Regex to remove the "Name:" prefix at the start
        description = re.sub(rf'^\s*{re.escape(name)}\s*:\s*', '', full_text).strip()

        data.append({
            'URL': url,
            'Name': name,
            'Description': description
        })

    # Create DataFrame and save to Excel
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False)
    print(f"Successfully extracted {len(df)} items into '{excel_file}'.")


def excel_to_html(excel_file, outfile):
    """
    Reads link data from an Excel spreadsheet, removes duplicate URLs,
    and generates a styled HTML file.
    """
    if not os.path.exists(excel_file):
        print(f"Error: The file '{excel_file}' does not exist.")
        return

    print(f"Reading '{excel_file}'...")
    df = pd.read_excel(excel_file)
    
    # Ensure columns exist and fill missing values with empty strings
    for col in ['URL', 'Name', 'Description']:
        if col not in df.columns:
            df[col] = ""
        else:
            df[col] = df[col].fillna("").astype(str).str.strip()

    # Identify and report duplicates before dropping them
    duplicate_mask = df.duplicated(subset=['URL'], keep='first')
    if duplicate_mask.any():
        print("\n[Warning] Duplicate URLs detected and removed:")
        for _, row in df[duplicate_mask].iterrows():
            print(f"  - Skipped: {row['Name']} ({row['URL']})")
        print("")

    # Drop duplicate URLs, keeping the first occurrence
    df = df.drop_duplicates(subset=['URL'], keep='first')

    # Recreate the exact HTML boilerplate from your index.html style
    html_content = """<head>
    <style>
        body {
            font-family: sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
        }
        li {
            margin-bottom: 10px;
        }
    </style>
</head>
<h2 id="title">
 List of digital tools built by NCCR Catalysis (under construction)
</h2>
<ul>
"""

    # Generate the <li> elements
    for _, row in df.iterrows():
        # Handle cases where URL or Name might be missing gracefully
        if not row['URL'] or not row['Name']:
            continue
            
        li_item = f' <li>\n  <strong>\n   <a href="{row["URL"]}" rel="noopener noreferrer" target="_blank">\n    {row["Name"]}\n   </a>\n   :\n  </strong>\n  {row["Description"]}\n </li>\n'
        html_content += li_item

    # Close the tags
    html_content += "</ul>"

    # Write the output file
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Successfully generated clean HTML file: '{outfile}' ({len(df)} items included).")


# --- Example Workflow Execution ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        raise ValueError(""""You can run the functions independently or use in one of the following ways:
                         - python html_excel.py index.html tool_list.xlsx
                         - python html_excel.py tool_list.html index_updated.html""")
    if sys.argv[1].endswith(".html"):
        html_to_excel(sys.argv[1], sys.argv[2])
    if sys.argv[1].endswith(".xlsx"):
        excel_to_html(sys.argv[1], sys.argv[2])
