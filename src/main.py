from crawler import crawl
from indexer import build_index, save_index, load_index
from search import print_word, find_pages

def main():
    index = None  # Start with no index loaded

    while True:
        user_input = input("> ").strip()
        
        if not user_input:
            continue  # Ignore empty input
        
        parts = user_input.split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "build":
            crawled_pages = crawl()
            index = build_index(crawled_pages)
            save_index(index)
            print("Index built successfully.")
        
        elif command == "load":
            index = load_index()
            print("Index loaded successfully.")
        
        elif command == "print":
            if index:
                print_word(index, args)
            else:                
                print("No index loaded. Please build or load an index first.")
        
        elif command == "find":
            if index:
                results = find_pages(index, args)
                if results:
                    print("Pages Found:")
                    for url in results:
                        print(url)
                else:
                    print("No pages found for that query")
            else:
                print("No index loaded. Please build or load an index first.")
        
        elif command == "quit":
            print("Goodbye!")
            break
        
        else:
            print(f"Unknown command: '{command}'")

if __name__ == "__main__":
    main()