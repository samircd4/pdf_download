import os
import requests
from urllib.parse import urlparse
import urllib

def download_pdfs(urls):
    # Define a custom download path
    download_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_path, exist_ok=True)

    for _ , url in enumerate(urls, start=1):
        try:
            # Extract the basename from the URL to name the file
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # Ensure the filename is properly formatted and safe
            filename = urllib.parse.unquote(filename)

            # Add ".pdf" extension if it's missing
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Define the full path where the PDF will be saved
            save_path = os.path.join(download_path, filename)

            # Send a GET request to download the PDF content
            print(f"Downloading PDF from: {url}")
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Download completed and saved as: {save_path}")
            else:
                print(f"Failed to download from {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
            with open('error.txt', 'a') as error_file:
                error_file.write(f"{url}\n")
        finally:
            print(f"{_}: Finished processing {url}")

# List of URLs you want to download from
with open('link.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]
    returned_urls = list(set(urls))  # Remove duplicates


# Call the function to start downloading the PDFs
download_pdfs(returned_urls)
