import json
import re
import pandas as pd
from fuzzywuzzy import fuzz

def detect_companies(text : str, companies_data : pd.DataFrame, threshold : int =80 ):
    detected = []

    for _, company in companies_data.iterrows():
        ticker = company['ticker']
        all_names = [name for name in company['names']]

        # Ticker matching, ticker must be all caps
        ticker_pattern = r'\b' + re.escape(ticker) + r'\b' 
        ticker_matches = re.findall(ticker_pattern, text)
        
        if ticker_matches:
            detected.append(company['ticker'])
            continue

        # find company name in text, company name and text are normalized to be all lowercase,
        # may produce the occasional false positive
        name_matched = False
        for name in all_names:
            name_pattern = r'\b' + re.escape(name.lower()) + r'\b' 
            name_matches = re.findall(name_pattern, text.lower())
            
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
    sample_text = "AMAZON AMZN amazon Google, GOog, GooGlE, nvidia, meta aasdfasdf"
    print(detect_companies(sample_text, companies))