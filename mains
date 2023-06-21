from playwright.sync_api import sync_playwright
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def login_and_download_page(login_url, username, password, page_url, save_directory):
    with sync_playwright() as playwright:
        browser_type = playwright.chromium
        browser = browser_type.launch()
        page = browser.new_page()

        try:
            # Navigate to the login page
            page.goto(login_url)

            # Find the username and password input fields and enter the credentials
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)

            # Submit the login form
            page.click('button[type="submit"]')

            # Wait for navigation to complete
            page.wait_for_load_state("networkidle")

            # Check if login was successful by checking the URL or any element specific to logged-in state
            if page.url == login_url:
                print("Login failed. Please check your credentials.")
                return

            # Navigate to the target page after successful login
            page.goto(page_url)

            # Wait for the page to load
            page.wait_for_load_state("networkidle")

            # Get the page content
            page_content = page.content()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')

            # Find all link tags and get the associated CSS files
            css_files = soup.find_all('link', {'rel': 'stylesheet'})
            for css_file in css_files:
                css_url = urljoin(page.url, css_file['href'])
                css_response = requests.get(css_url)
                if css_response.status_code == 200:
                    # Save the CSS file
                    css_filename = os.path.basename(css_url)
                    css_filepath = os.path.join(save_directory, css_filename)
                    with open(css_filepath, 'wb') as file:
                        file.write(css_response.content)
                    print(f"CSS file '{css_filename}' downloaded successfully.")
                else:
                    print(f"Error downloading CSS file from URL '{css_url}'. Status Code: {css_response.status_code}")

            # Find all script tags and get the associated JavaScript files
            script_files = soup.find_all('script')
            for script_file in script_files:
                if script_file.get('src'):
                    script_url = urljoin(page.url, script_file['src'])
                    script_response = requests.get(script_url)
                    if script_response.status_code == 200:
                        # Save the JavaScript file
                        script_filename = os.path.basename(script_url)
                        script_filepath = os.path.join(save_directory, script_filename)
                        with open(script_filepath, 'wb') as file:
                            file.write(script_response.content)
                        print(f"JavaScript file '{script_filename}' downloaded successfully.")
                    else:
                        print(f"Error downloading JavaScript file from URL '{script_url}'. Status Code: {script_response.status_code}")

            # Save the page content to a file
            filename = os.path.join(save_directory, "downloaded_page.html")
            with open(filename, "wb") as file:
                file.write(page_content)

            print(f"Webpage downloaded and saved as '{filename}' successfully.")

        except Exception as e:
            print(f"An error occurred while logging in and downloading the webpage: {str(e)}")

        browser.close()


def main():
    login_url = 'https://example.com/login'
    username = 'your_username'
    password = 'your_password'
    page_url = 'https://example.com/page'
    save_directory = 'downloaded_pages'

    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    login_and_download_page(login_url, username, password, page_url, save_directory)


if __name__ == "__main__":
    main()
