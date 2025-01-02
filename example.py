import os
from util import llm_call 
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Callable


def chain(input: str, prompts: List[str]) -> str:
    """Chain multiple LLM calls sequentially, passing results between steps."""
    result = input
    for i, prompt in enumerate(prompts, 1):
        print(f"\nStep {i}:")
        result = llm_call(f"{prompt}\nInput: {result}")
        print(result)
    return result

# Example 1: Chain workflow for structured data extraction and formatting. 
# Each step progressively transforms raw text into a formatted table.
data_processing_steps = [
    """Clean and standardize team names. 
    Example format:
    Lakers -> Los Angeles Lakers
    BuCKs -> Milwaukee Bucks
    Nuggggggets -> Denver Nuggets
""",

""" Format player names consistently.
Example format: 
Anthony Davis -> A. Davis
Jayson Tatum -> J. Tatum
""",

"""Standardize points per game notation.
Remove special characters and add PPG suffix
Example format:
26.1% points per game -> 26.1 PPG,
$32.6 points per game -> 32.6 PPG
""",

"""Format the sorted data as a markdown table with columns: 
| Team | Player | Points per Game |
|:--|--:|
| Lakers | A. Davis | 26.1 PPG |
| Celtics | J. Tatum | 28.3 PPG |
| 76ers | T. Maxey | 25.9 PPG |
"""
]

report = """
NBA Top Scorers: 
Lakers: Anthony Davis, 26.1% points per game
celtics: Jayson Tatum, $28.3 points per game
76ers: Tyrese Maxey, #25.9 points per game
BuCKs: Giannis Antetokounmpo, $32.6 points per game
thunder: Shai Gilgeous-Alexander, 31.4 points per game
Nuggggggets: Nikola Jokic, 31.0* points per game
kings: De'Aaron Fox, 26.5! points per game
"""

print("\nInput text:")
print(report)
formatted_result = chain(report, data_processing_steps)

#pd.read_excel('/Users/jarredrobidoux/Documents/LLM workflows/Grocery List.xlsx')



#Example 2: Prompt chaining an Excel file
def chain_excel(excel_path: str, prompts: List[str]) -> str:
    """Chain multiple LLM calls using Excel data as input."""
     #Read Excel file 
    df = pd.read_excel('/Users/jarredrobidoux/Documents/LLM workflows/Grocery List.xlsx')
    
    # Convert DataFrame to string representation
    result = df.to_string()
    
   #  Process through the chain
    for i, prompt in enumerate(prompts, 1):
        print(f"\nStep {i}:")
        result = llm_call(f"{prompt}\nInput: {result}")
        print(result)
    return result


#Example prompts for Excel data 
excel_analysis_steps = [
    """Analyze this data and edit the file where you see fit.
    #Return the edited file as a .xlsx file called 'edited_grocery_list.xlsx'.""",

    """Create a new column in our file called 'Euro Conversion' and convert the price of each item to Euros.
    Remember, the exchange rate is 1.00 Euros = 1.036 USD. 
    """,

    """Create a new column in our file called 'Discounted Price' and convert the column 'Euro Price' to a 50% discount.
    When you calculate a discounted price, you are multiplying the price by .5 in our case for 50% discount.""",

    """Create a new column in our file called 'Comestibles' and convert every name from the grocery list column to spanish. 
    Example: 
    Apple -> Manzana""",

    """After you've created the new columns, remove the 'grocery list' column from the file. 
    Return the edited file. """
]

# Use the chain 
excel_path = "/Users/jarredrobidoux/Documents/LLM workflows/Grocery List.xlsx"
result = chain_excel(excel_path, excel_analysis_steps)
