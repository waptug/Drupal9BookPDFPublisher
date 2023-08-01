"""
Program Name: D9BookPDFPublisher
Developer: Michael Scott McGinn
Date: July 31, 2023
Version: V1.0
License: GPL3
Clone this repo from https://github.com/waptug/Drupal9BookPDFPublisher.git

This program fetches a main webpage from https://selwynpolit.github.io/d9book/ and all linked pages from the given URL, converts them to PDF, and merges them into a single PDF file.
Orginal idea for the D9Book project goes out to https://selwynpolit.github.io/d9book/ and this program simply extends the benefits of a live Drupal resource.

It uses several Python libraries to achieve this:

1. requests: A popular Python library for making HTTP requests. It abstracts the complexities of making requests behind a beautiful, simple API.
   Install it using pip: pip install requests

2. BeautifulSoup: A Python library for parsing HTML and XML documents. It is often used for web scraping.
   Install it using pip: pip install beautifulsoup4

3. pdfkit: A Python wrapper for wkhtmltopdf, which allows HTML to PDF conversion using the webkit rendering engine and qt.
   Install it using pip: pip install pdfkit
   Note: You also need to install wkhtmltopdf in your system: https://wkhtmltopdf.org/downloads.html
   
   To install wkhtmltopdf, you can follow these steps:

    1. Go to the wkhtmltopdf downloads page: https://wkhtmltopdf.org/downloads.html

    2. Download the appropriate version for your operating system.
        example: `wget https://wkhtmltopdf.org/0.12/0.12.6/wkhtmltox_0.12.6.1-2.jammy_amd64.deb`
    3. Install the downloaded package.

    4. Add the wkhtmltopdf executable to your system's PATH environment variable.

    After installing wkhtmltopdf, you should be able to use it with the pdfkit Python
    library to convert HTML to PDF.
    
    The command to add the wkhtmltopdf executable to the system's PATH environment variable depends on the operating system you are using. Here are the commands for some common operating systems:

    **Windows:**

    1. Open the Start menu and search for "Environment Variables".
    2. Click on "Edit the system environment variables".
    3. Click on the "Environment Variables" button.
    4. Under "System Variables", scroll down and find the "Path" variable.
    5. Click "Edit".
    6. Click "New" and add the path to the directory containing the wkhtmltopdf executable (e.g. `C:\Program Files\wkhtmltopdf\bin`).
    7. Click "OK" to close all the windows.

    **macOS:**

    1. Open Terminal.
    2. Run the following command: `sudo nano /etc/paths`.
    3. Enter your password if prompted.
    4. Add the path to the directory containing the wkhtmltopdf executable (e.g. `/usr/local/bin`).
    5. Press `Ctrl+X`, then `Y`, then `Enter` to save and exit.

    **Linux:**

    1. Open Terminal.
    2. Run the following command: `sudo nano /etc/environment`.
    3. Add the path to the directory containing the wkhtmltopdf executable (e.g. `/usr/local/bin`) to the end of the `PATH` variable.
    4. Press `Ctrl+X`, then `Y`, then `Enter` to save and exit.
    5. Run the following command to apply the changes: `source /etc/environment`.

    To install a .deb file in WSL2 Ubuntu, you can follow these steps:

    1. Open the terminal in WSL2 Ubuntu.

    2. Navigate to the directory where the .deb file is located using the `cd` command.

    3. Install the package using the `dpkg` command. For example, if the package is 
       named `wkhtmltox_0.12.6.1-2.jammy_amd64.deb`, you can install it using the following command:

    ```
    sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb
    ```

   This will install the package and its dependencies.

    4. If you encounter any errors related to missing dependencies, you can install
       them using the `apt-get` command. For example, if the error message says that a package named `dependency` is missing, you can install it using the following command:

    ```
    sudo apt-get install dependency
    ```

    Once the missing dependencies are installed, you can try installing the .deb 
    package again using the `dpkg` command.



4. os: A built-in Python module that provides functions to interact with the operating system. No installation is needed.

5. PyPDF2: A Python library to read/write and manipulate PDFs.
   Install it using pip: pip install PyPDF2

6. subprocess: A built-in Python module that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

7. urllib.parse: A built-in Python module for parsing URLs.

8. logging: A built-in Python module for logging application events.

The program is divided into the following steps:
step 1: Fetch the main webpage
step 2: Parse the main webpage
step 3: Find all links in the nav section
step 4: Download each linked page
step 5: Parse the downloaded webpage
step 6: Replace relative URLs with absolute URLs
step 7: Save the modified webpage
step 8: Convert the main webpage to PDF
step 9: Append the main PDF to the merger
step 10: Convert each downloaded webpage to PDF
step 11: Wrote the merged PDF to {os.path.join(output_dir, 'combined.pdf')}
"""

import requests
from bs4 import BeautifulSoup
import pdfkit
import os
from PyPDF2 import PdfMerger
import subprocess
from urllib.parse import urljoin
import logging

# Setup logging
logging.basicConfig(filename='logfile.txt', level=logging.INFO)

# Create a new directory for the output files
logging.info("Creating a new directory for the output files.")
output_dir = "Rendered-PDF-2"
os.makedirs(output_dir, exist_ok=True)
logging.info(f"Success. Created a new directory for the output files: {output_dir}.")

# Fetch the main webpage
logging.info("Fetching the main webpage.")
main_url = 'https://selwynpolit.github.io/d9book/'
response = requests.get(main_url)
logging.info(f"Success. Fetched the main webpage: {main_url}.")

# Save the main index webpage to a local file using wget
logging.info("Saving the main index webpage to a local file using wget.")
main_filename = os.path.join(output_dir, 'D9BOOK.html')
result = subprocess.run(['wget', '-O', main_filename, main_url], capture_output=True, text=True)
if result.returncode != 0:
    logging.error(f"An error occurred while saving the main webpage: {result.stderr}")
else:
    logging.info(f"Success. Saved the main D9BOOK.html webpage to a local file: {main_filename}.")

# Parse the main webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links in the nav section
nav = soup.find('nav', {'id': 'site-nav'})  # Adjust this line based on the actual structure of the webpage
links = nav.find_all('a')

# Print all the links
logging.info("Found the following links:")
for link in links:
    logging.info(link.get('href'))

# Initialize a PDF merger
logging.info("Initializing a PDF merger.")
merger = PdfMerger()
logging.info("Success. Initialized a PDF merger.")

# Download each linked page
logging.info(f"Downloading {len(links)} webpages.")
for link in links:
    url = link.get('href')
    if url.startswith('/d9book/'):  # Relative link
        url = url.replace('/d9book/', '', 1)  # Remove the first occurrence of '/d9book/'
        url = main_url.rstrip('/') + '/' + url  # Concatenate main_url and the adjusted relative url
    
    logging.info(f"Created Access URL: {url}")  # Print the URL before accessing it
    
    try:
        # Fetch the linked webpage using wget
        logging.info(f"Fetching {url}.")
        filename = os.path.join(output_dir, os.path.basename(url) + '.html')
        result = subprocess.run(['wget', '-O', filename, url], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"An error occurred while fetching {url}: {result.stderr}")
        else:
            logging.info(f"Success. Downloaded {url}.")
            logging.info(f"=====================")

        # Parse the downloaded webpage and replace relative URLs with absolute URLs
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
        for tag in soup.findAll(True):
            if tag.has_attr('href'):
                tag['href'] = urljoin(url, tag['href'])
            if tag.has_attr('src'):
                tag['src'] = urljoin(url, tag['src'])

        # Save the modified webpage
        with open(filename, 'w') as f:
            f.write(str(soup))
    except Exception as e:
        logging.error(f"An error occurred while fetching {url}: {e}")

# Convert the main webpage to PDF
logging.info("Beginning conversion of main webpage to D9BOOK.pdf.")
main_pdf_filename = os.path.join(output_dir, 'D9BOOK.pdf')
logging.info(f"Converting {main_filename} to PDF.")
try:
    pdfkit.from_file(main_filename, main_pdf_filename)
    logging.info(f"Success Converted {main_pdf_filename} to PDF.")
except Exception as e:
    logging.error(f"An error occurred while converting {main_filename} to PDF: {e}")

# Add the main PDF to the merger
logging.info(f"Appending {main_pdf_filename} to the master PDF file.")
merger.append(main_pdf_filename)
logging.info(f"Appended {main_pdf_filename} to the master PDF file.")

# Convert each downloaded webpage to PDF
logging.info(f"Converting {len(links)} webpages to PDF.")
for link in links:
    url = link.get('href')
    if url.startswith('/d9book/'):  # Relative link
        url = url.replace('/d9book/', '', 1)  # Remove the first occurrence of '/d9book/'
        url = main_url.rstrip('/') + '/' + url  # Concatenate main_url and the adjusted relative url
    
    try:
        # Parse the downloaded webpage
        logging.info(f"Parsing {url} to convert to PDF.")
        filename = os.path.join(output_dir, os.path.basename(url) + '.html')
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Convert the local HTML file to PDF
        logging.info(f"Converting {url} to PDF.")
        pdf_filename = os.path.join(output_dir, os.path.basename(url) + '.pdf')
        pdfkit.from_file(filename, pdf_filename)
        logging.info(f"Success. Converted {url} to PDF.")
        
        # Add the PDF to the merger
        logging.info(f"Appending {pdf_filename} to the master PDF file.")
        merger.append(pdf_filename)
        logging.info(f"Success. Appended {pdf_filename} to the master PDF file.")
    except Exception as e:
        logging.error(f"An error occurred while converting {url} to PDF: {e}")

# Write the merged PDF to a file
logging.info(f"Writing the merged PDF to {os.path.join(output_dir, 'combined.pdf')}.")
merger.write(os.path.join(output_dir, "combined.pdf"))
merger.close()
logging.info(f"Success. Wrote the merged PDF to {os.path.join(output_dir, 'combined.pdf')}.")

print("Done.")
