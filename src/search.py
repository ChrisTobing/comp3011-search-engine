def print_word(index, word):
    word = word.lower()
    
    if word in index:
        print(f"{word}: {index[word]}")
    else:
        print(f"'{word}' not found in index.")

def find_pages(index, query):
    query_words = query.lower().split()
    
    if not query_words:
        return []
    
    result = None
    for word in query_words:
        if word not in index:
            print(f"'{word}' not found in index.")
            return []
        
        url_set = set(index[word].keys())  # Get URLs for this word
        
        if result is None:
            result = url_set               # First word — initialise result
        else:
            result = result & url_set      # Subsequent words — intersect
    
    return list(result) if result else []