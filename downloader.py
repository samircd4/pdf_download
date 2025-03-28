import os
import asyncio
import aiohttp
from urllib.parse import unquote
from selectolax.parser import HTMLParser

# Semaphore to limit the number of concurrent downloads
MAX_CONCURRENT_DOWNLOADS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

async def download_file(file_url: str, save_path: str):
    # Skip files that have "anual" in the name
    if 'anual' in file_url.lower():
        return

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "0",
        "origin": "https://www.usace.army.mil",
        "priority": "u=1, i",
        "referer": "https://www.usace.army.mil/",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "sec-fetch-storage-access": "active",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    async with semaphore:
        try:
            # Use aiohttp to send an asynchronous GET request to the URL
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url, headers=headers) as response:
                    if response.status == 200:
                        content = await response.read()  # Asynchronously read the content
                        # Save the content to the file
                        with open(save_path, 'wb') as f:
                            f.write(content)
                        print(f"File downloaded successfully and saved as {save_path}")
                    else:
                        print(f"Failed to download file. Status code: {response.status}")
        except Exception as e:
            print(f"An error occurred: {e}")
            with open('error.txt', 'a') as file:
                file.write(f'{file_url}\n')
        except asyncio.TimeoutError:
            print('Request Timeout')
            with open('error.txt', 'a') as file:
                file.write(f'{file_url}\n')



async def read_text_file():
    with open('link.txt', 'r') as file:
        links = [link.strip() for link in file.readlines()]
    return links

# Main async function to download all files
async def main(folder_name):
    # Read links from the text file
    links = await read_text_file()

    # Create a directory for saving the files if it doesn't exist
    os.makedirs('auto_download', exist_ok=True)

    tasks = []
    for index, file_url in enumerate(links, start=1):
        # Get the file name and unquote the URL
        file_name = os.path.basename(unquote(file_url))
        print(f'Start downloading {index} {file_name}')

        # Ensure the file has the correct extension
        if not file_name.endswith(('.pdf', '.docx')):
            file_name += '.pdf'

        # Create the download task and add it to the list of tasks
        task = download_file(file_url, f'auto_download/{folder_name}/{file_name}')
        tasks.append(task)
        print(f'{index}/{len(links)}')

        # Limit the number of concurrent downloads by ensuring we don't exceed MAX_CONCURRENT_DOWNLOADS
        if len(tasks) >= MAX_CONCURRENT_DOWNLOADS:
            await asyncio.gather(*tasks)  # Wait for tasks to complete
            tasks = []  # Reset tasks list

    # Run the remaining tasks (if any)
    if tasks:
        await asyncio.gather(*tasks)



# Create a directory for saving the files if it doesn't exist
# folder_name = os.makedirs('web-108', exist_ok=True)



# Run the main function
asyncio.run(main('web-111'))
