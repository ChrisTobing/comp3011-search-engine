# COMP3011 Search Engine Tool

## Overview
A command-line search engine tool built in Python that crawls 
[https://quotes.toscrape.com/](https://quotes.toscrape.com/), 
builds an inverted index of all word occurrences, and allows 
users to search for pages containing specific terms.

Built as part of COMP3011 Web Services and Web Data at the 
University of Leeds.

---

## Project Structure
[comp3011-search-engine]/
├── src/
│   ├── crawler.py      # Web crawler implementation
│   ├── indexer.py      # Inverted index builder
│   ├── search.py       # Search functionality
│   └── main.py         # CLI entry point
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   └── test_search.py
├── data/
│   └── index.json      # Compiled index file
├── requirements.txt
└── README.md

---

## Dependencies

- Python 3.x
- requests
- beautifulsoup4
- pytest

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/[ChrisTobing]/[comp3011-search-engine].git
cd [comp3011-search-engine]
```

### 2. Create and activate a virtual environment
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

Run the tool from the project root directory:

```bash
python3 src/main.py
```

### Commands

#### `build`
Crawls the website, builds the inverted index and saves it to disk.
Note: This will take several minutes due to the politeness window.

#### `load`
Loads a previously built index from disk.

#### `print <word>`
Prints the inverted index entry for a specific word, showing
which pages it appears on, its frequency, and positions.

#### `find <query>`
Returns all pages containing the given word(s). Supports
single and multi-word queries. Multi-word queries return only
pages containing ALL words.

#### `quit`
Exits the search tool.

### Example Session

```
> build
Crawling https://quotes.toscrape.com...
Successfully fetched https://quotes.toscrape.com
...
Index built and saved successfully.


> find love life
Pages found:
https://quotes.toscrape.com/page/3/
https://quotes.toscrape.com/author/Pablo-Neruda


> print love
love: {
'https://quotes.toscrape.com/': {'frequency': 2, 'positions': [4, 17]},
...
}


> quit
Goodbye!
```

---

## Testing

Run the full test suite from the project root:

```bash
pytest tests/ -v
```

### Testing Strategy
- **test_crawler.py** — Tests web crawling with mocked HTTP 
  requests to avoid real network calls
- **test_indexer.py** — Tests index building, word frequency, 
  position tracking, and file save/load operations
- **test_search.py** — Tests single and multi-word search, 
  case insensitivity, and edge cases

---

## Design Decisions

### Inverted Index Structure
The index is stored as a nested dictionary:
```python
{
    "word": {
        "page_url": {
            "frequency": 2,
            "positions": [4, 17]
        }
    }
}
```
This structure allows O(1) word lookup and efficient 
set intersection for multi-word queries.

### Crawling Strategy
- Crawls main paginated quote pages first
- Collects author URLs during quote page crawl to avoid 
  re-fetching pages
- Crawls author pages second
- Skips tag pages to avoid indexing duplicate content
- Observes 6 second politeness window between all requests

### Text Processing
- Words extracted using regex `[a-z]+` after lowercasing
- Punctuation and numbers automatically excluded
- **Note**: Apostrophes cause splits (e.g. "it's" → ["it", "s"]) — 
  a known limitation

---

## GenAI Usage Declaration

### Tool Used
**Claude (Anthropic)** — accessed via Claude.ai Projects feature using 
a custom system prompt configured to act as a coursework assistant 
rather than a solution provider.

### How GenAI Was Used

#### 1. Project Planning
Claude was asked to break down the coursework brief into manageable 
steps and explain key concepts (e.g. what an inverted index is) before 
any implementation began. This helped structure the development process 
incrementally.

#### 2. Guided Implementation Pipeline
For each component of the project, the following iterative pipeline 
was followed:

Claude provides function skeleton with docstrings and TODO comments
↓
I implement my own solution independently
↓
Claude reviews my implementation and gives feedback
↓
I apply fixes, make design decisions, and commit

This approach ensured I wrote and understood all code myself, using 
Claude as a reviewer rather than a code generator. Examples include:

- **fetch_page()** — I wrote the initial implementation including 
  raise_for_status() and exception handling. Claude identified a 
  redundant status code check and suggested adding a timeout parameter.
- **build_index()** — I attempted the implementation but incorrectly 
  initialised the index entry as a set() instead of a dict(). Claude 
  identified the bug and explained why dictionaries are more appropriate 
  for key-value assignment.
- **find_pages()** — I implemented a set-of-sets approach which would 
  have caused a TypeError at runtime. Claude explained why sets cannot 
  contain other sets and guided me toward an iterative intersection 
  approach instead.

#### 3. Documentation Reference
Rather than reading full library documentation, I asked Claude to 
generate project-specific cheat sheets for:
- **BeautifulSoup** — covering only the methods relevant to HTML 
  parsing in this project (find, find_all, get_text, get etc.)
- **pytest** — covering fixtures, mocking with unittest.mock, 
  capsys, and tmp_path relevant to testing this project
- **MagicMock** - covering how to make mock requests to a fake HTML
  page rather than wasting compute making real time requests to the 
  official website.

### What Claude Did NOT Do
- Claude did not write any complete functions from scratch
- All design decisions (crawl scope, data structures, text processing) 
  were discussed and decided collaboratively, not delegated to Claude
- Claude did not generate the test cases — I wrote these based on 
  the sample index fixture and my understanding of the expected behaviour

### Reflection
Using Claude in this structured way promoted active learning rather 
than passive code acceptance. The skeleton → attempt → review → fix 
pipeline meant every piece of code was written and understood by me 
before being committed. 

The most valuable aspect was having Claude act as an on-demand 
reviewer — catching bugs like the set/dict confusion in build_index() 
that would have been time-consuming to debug independently.

A limitation of this approach is that Claude occasionally suggested 
overly complex solutions (e.g. the initial find_pages skeleton) which 
required simplification. This highlighted that AI suggestions should 
always be critically evaluated rather than accepted wholesale.