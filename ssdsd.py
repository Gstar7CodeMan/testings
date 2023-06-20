import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def login_and_extract_urls(login_url, username, password):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    try:
        # Load the login page
        driver.get(login_url)

        # Find the username and password input fields and enter the credentials
        username_field = driver.find_element_by_name('username')
        password_field = driver.find_element_by_name('password')
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the form by pressing Enter
        password_field.send_keys(Keys.RETURN)

        # Wait for the login process to complete (you may need to add a delay or wait for specific elements to load)

        # Extract the current page source after successful login
        page_source = driver.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract URLs and sub-URLs from the page
        base_url = driver.current_url
        page_links = extract_page_links(base_url, soup)

        # Download and save the linked webpages
        for link in page_links:
            download_webpage(link)

    finally:
        # Close the browser window
        driver.quit()

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
