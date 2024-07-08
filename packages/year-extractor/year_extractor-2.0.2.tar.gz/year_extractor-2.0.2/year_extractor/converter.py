import spacy
import dateparser
from datetime import datetime

class YearExtractor:
    def __init__(self):
        # Load the spaCy model once during initialization
        self.nlp = spacy.load("en_core_web_lg")

    def extract_and_convert(self, text):
        # Process the text using the spaCy model
        doc = self.nlp(text)
        
        # Extract date entities
        date_entities = [ent for ent in doc.ents if ent.label_ == "DATE"]
        print("Extracted date entities:", date_entities)
        # Process all date entities
        years = []
        for ent in date_entities:
            print("Processing entity:", ent.text)
            # Use dateparser to parse the date entity
            date = dateparser.parse(ent.text, settings={'PREFER_DATES_FROM': 'past'})
            print("Parsed date:", date)
            if date:
                years.append(date.year)  # Append the year as an integer

        if not years:
            current_year = datetime.now().year
            print("No valid date found, returning current year:", current_year)
            years.append(current_year)
          
        
        return years  # Return the list of years

