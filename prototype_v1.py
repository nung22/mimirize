# Import the libraries
import requests
from bs4 import BeautifulSoup
import sys # To get command line arguments if needed, or use input()

def fetch_and_extract_text(url):
    try:
        # 1. Fetch HTML content
        headers = {'User-Agent': 'MyFactCheckPrototype/1.0'} # Some sites block requests without a User-Agent
        response = requests.get(url, headers=headers, timeout=10) # Added timeout
        response.raise_for_status() # Raise an error for bad responses (4xx or 5xx)

        # 2. Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # 3. Extract Main Text (This is the hard part and varies greatly by website structure)
        # Strategy 1: Look for common tags like <article>, <main>, or divs with specific IDs/classes
        # (e.g., class="article-body", id="content"). This requires inspecting website source code.
        article_body = soup.find('article') # Try finding an <article> tag
        if not article_body:
            # Fallback: Try finding a common div structure (highly site-dependent)
            # This is just an example, you'd need to adapt based on common web structures
             possible_bodies = soup.find_all('div', class_=lambda x: x and ('content' in x or 'article' in x or 'body' in x))
             if possible_bodies:
               article_body = max(possible_bodies, key=len) # Guess the longest one is the main content
             else:
               article_body = soup.body # Last resort: get the whole body

        # Remove script and style elements
        if article_body:
            for script_or_style in article_body(['script', 'style']):
                script_or_style.decompose()
            text = article_body.get_text(separator='\n', strip=True)
        else:
             text = "Could not find main article body reliably."


        return text

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An error occurred during parsing: {e}"

# --- Main part of the script ---
if __name__ == "__main__":
    # Get URL from user input
    input_url = input("Please enter the URL of the article: ")

    if input_url:
        print(f"\nFetching text from: {input_url}\n")
        extracted_text = fetch_and_extract_text(input_url)
        print("--- Extracted Text ---")
        print(extracted_text)
        print("----------------------")
    else:
        print("No URL entered.")