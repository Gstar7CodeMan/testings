import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def login_and_extract_urls(login_url, username, password):
    with sync_playwright() as playwright:
        try:
            browser_type = playwright.chromium
            browser = browser_type.launch()
            page = browser.new_page()

            # Navigate to the login page
            page.goto(login_url)

            # Find the username and password input fields and enter the credentials
            page.fill('input[name="username"]', username)
            page.fill('input[name="pwd"]', password)

            # Submit the login form
            page.click('button[type="submit"]')

            # Wait for the login process to complete (you may need to add a delay or wait for specific elements to load)

            # Wait until the element with ID 'aof-ribbon-container' is loaded
            page.wait_for_selector('#aof-ribbon-container', timeout=5000)

            # Extract the current page content after successful login
            page_content = page.content()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')

            # Extract URLs and sub-URLs from the page
            base_url = page.url
            page_links = extract_page_links(base_url, soup)

            # Download and save the linked webpages with associated resources
            for link in page_links:
                download_webpage(link, base_url)

        except Exception as e:
            print(f"Error occurred during login and URL extraction: {str(e)}")

        finally:
            try:
                browser.close()
            except Exception as e:
                print(f"Error occurred while closing the browser: {str(e)}")

def extract_page_links(base_url, soup):
    links = soup.find_all('a')
    page_links = []
    for link in links:
        href = link.get('href')
        if href:
            absolute_url = urljoin(base_url, href)
            page_links.append(absolute_url)
    return page_links

def download_webpage(url, base_url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extract the filename from the URL
        filename = os.path.basename(urlparse(url).path)

        # Create a directory to store the downloaded files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(base_dir, 'downloaded_pages')
        os.makedirs(download_dir, exist_ok=True)

        # Save the HTML file
        html_file_path = os.path.join(download_dir, filename)
        with open(html_file_path, 'wb') as file:
            file.write(response.content)

        # Save associated resources (CSS, images, etc.)
        soup = BeautifulSoup(response.text, 'html.parser')
        resource_tags = soup.find_all(['link', 'img', 'script'])

        for tag in resource_tags:
            if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
                # Save CSS file
                css_url = urljoin(base_url, tag.get('href'))
                css_file_name = os.path.basename(urlparse(css_url).path)
                css_file_path = os.path.join(download_dir, css_file_name)
                download_resource(css_url, css_file_path)
            elif tag.name == 'img':
                # Save image file
                img_url = urljoin(base_url, tag.get('src'))
                img_file_name = os.path.basename(urlparse(img_url).path)
                img_file_path = os.path.join(download_dir, img_file_name)
                download_resource(img_url, img_file_path)
            elif tag.name == 'script':
                # Save script file
                script_url = urljoin(base_url, tag.get('src'))
                script_file_name = os.path.basename(urlparse(script_url).path)
                script_file_path = os.path.join(download_dir, script_file_name)
                download_resource(script_url, script_file_path)

        print(f"Webpage and associated resources saved in '{download_dir}'.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading webpage from URL '{url}': {str(e)}")

def download_resource(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading resource from URL '{url}': {str(e)}")

def main():
    login_url = 'https://example.com/login'
    username = 'your_username'
    password = 'your_password'

    login_and_extract_urls(login_url, username, password)

if __name__ == '__main__':
    main()
