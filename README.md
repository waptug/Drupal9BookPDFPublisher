# Drupal9BookPDFPublisher
Python program to convert the D9Book site into a PDF file

This python code will reach out to https://selwynpolit.github.io/d9book/
and pull in the site as html then locally convert each page into a PDF file.
Then it will combine each PDF page into a master file for easy sharing.
It will also generate a text log of the progress.

The cool thing I think about this is that each time the code is run it
will be a fresh copy of the site because it pulls from the live site.

So any new updates to the site will be published in the PDF.

And the links in the PDF all work get get back to the main site.

This site is an opensource project and all Drupal developers are welcome
to contribute to the main site to add code samples and documentation to it.

If you find my python code helpful please join my repository and add to it.

With a bit of tweeking my Python code would work on any site to create a 
PDF version of it.

### Requirements
Here is how I have my dev machine set up

WSL2
Ubuntu
DDEV
Python 3

A number of python librarys installed

1. requests: A popular Python library for making HTTP requests. It abstracts the complexities of making requests behind a beautiful, simple API.
   Install it using pip: pip install requests

2. BeautifulSoup: A Python library for parsing HTML and XML documents. It is often used for web scraping.
   Install it using pip: pip install beautifulsoup4

3. pdfkit: A Python wrapper for wkhtmltopdf, which allows HTML to PDF conversion using the webkit rendering engine and qt.
   Install it using pip: pip install pdfkit
   Note: You also need to install wkhtmltopdf in your ubuntu system: https://wkhtmltopdf.org/downloads.html

4. os: A built-in Python module that provides functions to interact with the operating system. No installation is needed.

5. PyPDF2: A Python library to read/write and manipulate PDFs.
   Install it using pip: pip install PyPDF2

6. subprocess: A built-in Python module that allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.

7. urllib.parse: A built-in Python module for parsing URLs.

8. logging: A built-in Python module for logging application events.

Michael Scott McGinn
July 31, 2023

