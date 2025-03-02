import json
import re
import pandas as pd
from fuzzywuzzy import fuzz

def detect_companies(text : str, companies_data : pd.DataFrame, threshold : int =80 ):
    """
    Detect company mentions in text by ticker or any of their associated names.
    
    Args:
        text: The text to search for company mentions
        companies_data: DataFrame with 'ticker', 'names', and 'aliases' columns
        threshold: Similarity threshold for fuzzy matching (0-100)
        
    Returns:
        List of detected companies 
    """
    detected = []

    for _, company in companies_data.iterrows():
        ticker = company['ticker']
        all_names = [name for name in company['names']]

        # # Check for exact ticker match (case insensitive)
        ticker_pattern = r'\b' + re.escape(ticker) + r'\b' 
        ticker_matches = re.findall(ticker_pattern, text)
        
        if ticker_matches:
            detected.append(company['ticker'])
            continue

        # # Check for exact name match using any of the names (case insensitive)
        name_matched = False
        for name in all_names:
            name_pattern = r'\b' + re.escape(name) + r'\b' 
            name_matches = re.findall(name_pattern, text)
            
            if name_matches:
                detected.append(company['ticker'])
                name_matched = True
                break
        
        if name_matched:
            continue
        
        """
        Discarding fuzzy matching for now because I don't think Jim Cramer makes typos
        """
        # # If no exact match, try fuzzy matching for company names
        # words = re.findall(r'\b\w+(?:\s+\w+){0,5}\b', text)
        # for name in all_names:
        #     for word_group in words:
        #         similarity = fuzz.partial_ratio(name, word_group.lower())
        #         if similarity >= threshold:
        #             detected.append(company['ticker'])
        #             name_matched = True
        #             break
        #     if name_matched:
        #         break
    # print(detected)
    
    return detected

# Example usage
if __name__ == "__main__":
    # Load companies data from csv into dictionary
    with open("./storage/companies.csv") as f:
        company_dict = {"ticker" : [], "names" : []}

        for line in f.readlines():
            line = line.strip().split(",")
            company_dict["ticker"].append(line[0])
            company_dict["names"].append(line[1:])

    companies = pd.DataFrame(company_dict)
    # print(companies)
    sample_text = "People will wonder if Nvidia has now become a 'perfect' security, alongside PLTR, META, AMZN, and Google."
    detect_companies(sample_text, companies)