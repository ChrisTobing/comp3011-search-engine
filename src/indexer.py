import re

def build_index(pages):
    index = {}
    for page in pages:
        url = page["url"]
        content = page["content"]
        words = re.findall(r'[a-z]+', content.lower())
        
        for position, word in enumerate(words):  # enumerate gives position for free
            if word not in index:
                index[word] = {}  # Dictionary not set
            
            if url not in index[word]:
                index[word][url] = {"frequency": 0, "positions": []}
            
            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)
    
    return index

def save_index(index, filepath="data/index.json"):
    """Saves the index to a JSON file"""
    pass

def load_index(filepath="data/index.json"):
    """Loads the index from a JSON file"""
    pass