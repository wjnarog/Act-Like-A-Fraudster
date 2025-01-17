## PDF Scraper
### Overview
This is a proof-of-concept model to scrape a series of webpages for file download links, and then download those files as a batch. It is intended to work for state/county record pages, using the Boulder County Land Survey Plat Records as an example.

Current model was completed in approx. 3 hours.

### Caveats
This model is dependent on link format to work properly. For the BoCo Land Survey Plat Records, downloads were hosted using the following format:
- Search Results
    - Hosting Page, with a URL of `https://services.boco.solutions/cpp_filenetclient/doclist?searchValue=HIST-MAP-XXXX`, where XXXX was a four-digit numerical identifier.
        - Download page, connected by a Javascript variable leading to the download, in the format `javascript:var w =window.open('ContentDisplay.aspx?DocId={430CB06B-6A34-4F38-8E1D-EBE391AC11E5}','Document','location=0, resizable=1')`.

Note that the Javascript variable is not the same as the file download link. The JS simply contains a DocId attribute that gets passed to the download link in the format `https://services.boco.solutions/cpp_filenetclient/ContentDisplay.aspx?DocId={XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}`, where the DocId within the curly brackets is a unique alphanumerical identifier tied to each PDF download.

### Libraries
- **Urllib** - to retrieve and download files
- **Requests** - to scrape content of pages
- **BeautifulSoup** - to parse HTML content of pages, after being scraped by Requests
- **Re** - to extract DocId from Javascript variable on download page

### Functionality
The scraper works as follows:
1. The Request/BeautifulSoup scraper iterates through a list of hostpage URLs and extracts the DocId.
2. The DocId is placed in a string matching the download link format, and these completed download URLs are placed in a second list.
3. PDF files are downloaded using Urllib and placed in their own directory.

### Files
- `pdf_scraper.ipynb` - Code to download the first 99 maps found on the Boulder County Land Survey Plat Records.
- `downloads` - A directory containing the 99 maps in PDF format.