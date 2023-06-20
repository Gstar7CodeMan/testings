import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def login_and_extract_urls(login_url, username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Load the login page
        page.goto(login_url)

        # Find the username and password input fields and enter the credentials
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)

        # Submit the form
        page.press('input[name="password"]', 'Enter')

        # Wait for the login process to complete (you may need to add a delay or wait for specific elements to load)

        # Extract the current page source after successful login
        page_content = page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract URLs and sub-URLs from the page
        base_url = page.url
        page_links = extract_page_links(base_url, soup)

        # Download and save the linked webpages
        for link in page_links:
            download_webpage(link)

        # Close the browser
        context.close()
        browser.close()

def extract_page_links(base_url, soup):
    links = soup.find_all('a')
    page_links = []
    for link in links:
        href = link.get('href')
        if href:
            absolute_url = urljoin(base_url, href)
            page_links.append(absolute_url)
    return page_links

def download_webpage(url):
    response = requests.get(url)
    content = response.text
    filename = url.split('/')[-1]  # Extract the filename from the URL
    save_webpage(content, filename)

def save_webpage(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Webpage saved as '{filename}' successfully.")
    except IOError as e:
        print(f"Error saving webpage as '{filename}': {str(e)}")

def main():
    login_url = 'https://example.com/login'
    username = 'your_username'
    password = 'your_password'

    login_and_extract_urls(login_url, username, password)

if __name__ == '__main__':
    main()
