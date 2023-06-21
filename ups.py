import mimetypes

def download_webpage(url, base_url):
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        if response.status == 200:
            # Extract the filename from the URL
            filename = os.path.basename(urlparse(url).path)
            
            # Check if the file is an HTML file
            content_type = response.headers.get('Content-Type')
            is_html = False
            if content_type:
                file_type, _ = mimetypes.guess_type(content_type)
                if file_type == 'text/html':
                    is_html = True

            # Append the correct extension based on the file type
            if is_html:
                filename += '.html'
            else:
                ext = mimetypes.guess_extension(content_type)
                if ext:
                    filename += ext

            # Create a directory to store the downloaded files
            base_dir = os.path.dirname(os.path.abspath(__file__))
            download_dir = os.path.join(base_dir, 'downloaded_pages')
            os.makedirs(download_dir, exist_ok=True)

            # Save the file
            file_path = os.path.join(download_dir, filename)
            with open(file_path, 'wb') as file:
                file.write(response.data)

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.data, 'html.parser')

            # Save associated resources (CSS, images, etc.)
            resource_tags = soup.find_all(['link', 'img', 'script'])

            for tag in resource_tags:
                if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
                    # Save CSS file
                    css_url = urljoin(base_url, tag.get('href'))
                    css_response = http.request('GET', css_url)
                    if css_response.status == 200:
                        css_filename = os.path.basename(urlparse(css_url).path)
                        css_file_path = os.path.join(download_dir, css_filename)
                        with open(css_file_path, 'wb') as css_file:
                            css_file.write(css_response.data)
                    else:
                        print(f"Error downloading CSS resource from URL '{css_url}': Status Code {css_response.status}")
                elif tag.name == 'img':
                    # Save image file
                    img_url = urljoin(base_url, tag.get('src'))
                    img_response = http.request('GET', img_url)
                    if img_response.status == 200:
                        img_filename = os.path.basename(urlparse(img_url).path)
                        img_file_path = os.path.join(download_dir, img_filename)
                        with open(img_file_path, 'wb') as img_file:
                            img_file.write(img_response.data)
                    else:
                        print(f"Error downloading image resource from URL '{img_url}': Status Code {img_response.status}")
                elif tag.name == 'script':
                    # Save script file
                    script_url = urljoin(base_url, tag.get('src'))
                    script_response = http.request('GET', script_url)
                    if script_response.status == 200:
                        script_filename = os.path.basename(urlparse(script_url).path)
                        script_file_path = os.path.join(download_dir, script_filename)
                        with open(script_file_path, 'wb') as script_file:
                            script_file.write(script_response.data)
                    else:
                        print(f"Error downloading script resource from URL '{script_url}': Status Code {script_response.status}")

            print(f"Webpage and associated resources saved in '{download_dir}'.")

        else:
            print(f"Error downloading webpage from URL '{url}': Status Code {response.status}")

    except Exception as e:
        print(f"Error occurred while downloading webpage from URL '{url}': {str(e)}")
