import spacy
import re
from collections import defaultdict

class SimpleNLU:
    def __init__(self):
        """Initialize a simple NLU component using spaCy"""
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("Downloading spaCy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
            self.nlp = spacy.load("en_core_web_md")
        
        self.patterns = {
            'request_recipe': [
                r'recipe for ([\w\s]+)',
                r'how (to|do I) (make|cook) ([\w\s]+)',
                r'show me ([\w\s]+) recipes',
                r'I want to (make|cook|prepare) ([\w\s]+)'
            ],
            'time_constraint': [
                r'(quick|fast|easy|simple)',
                r'(\d+) minutes?',
                r'under (\d+) minutes?'
            ],
            'exclude_ingredient': [
                r'no ([\w\s]+)',
                r'without ([\w\s]+)',
                r"don'?t (have|want|like) ([\w\s]+)"
            ],
            'include_ingredient': [
                r'with ([\w\s]+)',
                r'using ([\w\s]+)',
                r'has ([\w\s]+)'
            ]
        }
    
    def parse(self, text):
        """Parse user input to extract intents and entities"""
        text = text.lower()
        doc = self.nlp(text)
        
        intent = "unknown"
        
        for pattern in self.patterns['request_recipe']:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                intent = "request_recipe"
                break
        
        entities = []
        
        dish = None
        for pattern in self.patterns['request_recipe']:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches and len(matches.groups()) > 0:
                dish = matches.groups()[-1].strip()
                entities.append({
                    "entity": "dish",
                    "value": dish
                })
                break
        
        for pattern in self.patterns['time_constraint']:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                value = matches.group(1)
                if value.isdigit():
                    entities.append({
                        "entity": "time",
                        "value": int(value)
                    })
                else:
                    entities.append({
                        "entity": "time",
                        "value": value
                    })
        
        for pattern in self.patterns['exclude_ingredient']:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches and len(matches.groups()) > 0:
                ingredient = matches.groups()[-1].strip()
                entities.append({
                    "entity": "exclude_ingredient",
                    "value": ingredient
                })
        
        for pattern in self.patterns['include_ingredient']:
            matches = re.search(pattern, text, re.IGNORECASE)
            if matches:
                ingredient = matches.group(1).strip()
                entities.append({
                    "entity": "include_ingredient",
                    "value": ingredient
                })
        
        for ent in doc.ents:
            if ent.label_ == "FOOD":
                if not any(e["entity"] == "include_ingredient" and e["value"] == ent.text for e in entities):
                    entities.append({
                        "entity": "include_ingredient",
                        "value": ent.text
                    })
        
        return {
            "intent": intent,
            "entities": entities,
            "text": text
        }
    
    def extract_query_info(self, parsed_data):
        """Convert parsed NLU data into query and constraints for the recipe engine"""
        query = parsed_data["text"]
        constraints = defaultdict(list)
        
        for entity in parsed_data["entities"]:
            entity_type = entity["entity"]
            value = entity["value"]
            
            if entity_type == "dish":
                query = value 
            elif entity_type == "time":
                if isinstance(value, int):
                    constraints["max_time"] = value
                elif value in ["quick", "fast"]:
                    constraints["max_time"] = 30
                elif value in ["easy", "simple"]:
                    constraints["difficulty"] = "easy"
            elif entity_type == "exclude_ingredient":
                constraints["exclude_ingredients"].append(value)
            elif entity_type == "include_ingredient":
                constraints["include_ingredients"].append(value)
        
        for key, value in constraints.items():
            if isinstance(value, list) and len(value) == 1:
                constraints[key] = value[0]
        
        return query, dict(constraints)