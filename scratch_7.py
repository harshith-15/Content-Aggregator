import requests
from bs4 import BeautifulSoup

def fetch_best_content_based_on_keyword(keyword, num_lines_per_website):
    # Pre-defined websites to scrape content from
    websites = {
        'wikipedia': f'https://en.wikipedia.org/wiki/{keyword}',
        'techcrunch': f'https://techcrunch.com/search/{keyword}'
        # Add more websites as needed
    }

    aggregated_content = []

    for site, url in websites.items():
        print(f'Fetching content for keyword "{keyword}" from {site}...')
        response = requests.get(url)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            # Example: Extract best content
            if site == 'wikipedia':
                paragraphs = soup.find('div', {'class': 'mw-parser-output'}).find_all('p')
                content = '\n'.join([p.text for p in paragraphs[:num_lines_per_website]])
                if not content:
                    content = "No content found on Wikipedia."
            elif site == 'techcrunch':
                # Modify this according to TechCrunch's HTML structure
                articles = soup.find_all('a', {'class': 'post-block__title__link'})
                content = '\n'.join([a.text for a in articles[:num_lines_per_website]])
                if not content:
                    content = "No relevant articles found on TechCrunch."

            aggregated_content.append(content)
        else:
            print(f'Failed to fetch content from {site}. Status code: {response.status_code}')

    # Sort content based on some criteria (e.g., length of content) to display the "best" content
    sorted_content = sorted(aggregated_content, key=len, reverse=True)

    # Combine the content into a single output without indicating the source
    combined_content = '\n\n'.join(sorted_content)

    return combined_content

# Take user input for keyword and number of lines per website
user_keyword = input('Enter a keyword: ')
num_lines_per_website = int(input('Enter the number of lines per website: '))

# Fetch and display the best content from the specified websites
print(f'\nBest content for keyword "{user_keyword}":\n')
best_content = fetch_best_content_based_on_keyword(user_keyword, num_lines_per_website)
print(best_content)
