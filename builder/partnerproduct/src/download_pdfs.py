import os
import time
import json
import requests
from urllib.parse import urlparse

def download_pdf(url, directory):
    bot_name = 'PDFDownloader/1.0'
    headers = {'User-Agent': bot_name}
    
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        # Get the filename from the URL
        filename = os.path.basename(urlparse(url).path)
        
        # Create the full path for saving the file
        filepath = os.path.join(directory, filename)
        
        # Open the file in write-binary mode
        with open(filepath, 'wb') as file:
            # Write the content to the file
            file.write(response.content)
        
        time.sleep(1)
        print(f"Downloaded: {filename}")
        print("------------------------------------------------")
        return True
    else:
        print(f"Failed to download: {url}")
        return False

def download_pdfs(urls, directory):
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    for url in urls:
        if url.lower().endswith('.pdf'):
            download_pdf(url, directory)
        else:
            print(f"Skipped: {url} (not a PDF)")

def main():

    pdf_directory = '../../../data' 
    
    # Load JSON data from file
    try:
        with open('faculty_of_science_links.json', 'r') as json_file:
            data = json.load(json_file)
        
        # Extract PDF URLs
        pdf_urls = data.get('pdfs', [])
        
        # Download PDFs
        print(f"Found {len(pdf_urls)} PDF files to download.")
        download_pdfs(pdf_urls, pdf_directory)
        print(f"Download process completed.")
    
    except FileNotFoundError:
        print("Error: JSON file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()