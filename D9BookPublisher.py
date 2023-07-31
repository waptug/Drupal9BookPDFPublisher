"""
Program Name: D9BookPDFPublisher
Developer: Michael Scott McGinn
Date: July 31, 2023
Version: V1.0
License: GPL3

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

4. os: A built-in Python module that provides functions to interact with the operating system. No installation is needed.

5. PyPDF2: A Python library to read/write and manipulate PDFs.
   Install it using pip: pip install PyPDF2

6. subprocess: A built-in Python module that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

7. urllib.parse: A built-in Python module for parsing URLs.

8. logging: A built-in Python module for logging application events.
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
