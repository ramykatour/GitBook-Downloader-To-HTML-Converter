import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def save_webpage_as_html(url, output_filename):
    try:
        # Send a GET request to the URL to fetch the content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Save the web page content as an HTML file
        with open(output_filename, "w", encoding="utf-8") as html_file:
            html_file.write(response.text)

        print(f"Web page saved as {output_filename}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def convert_gitbook_to_html(base_url, output_directory):
    try:
        # Send a GET request to the base URL to fetch the content
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a')

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Iterate through the links
        for link in links:
            href = link.get('href')
            if href and href.startswith('/'):  # Check if the link is relative
                full_url = urljoin(base_url, href)  # Make it an absolute URL
                parsed_url = urlparse(full_url)
                output_filename = os.path.join(output_directory, parsed_url.path.lstrip('/').replace('/', '_') + '.html')

                # Download and save the linked page as an HTML file
                save_webpage_as_html(full_url, output_filename)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_gitbook_to_html.py <gitbook_url> <output_directory>")
        sys.exit(1)

    gitbook_url = sys.argv[1]
    output_directory = sys.argv[2]

    convert_gitbook_to_html(gitbook_url, output_directory)

if __name__ == "__main__":
    main()
