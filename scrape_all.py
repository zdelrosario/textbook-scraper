## Import block
import pandas as pd
import re
import PyPDF2
import os

## Scraping helper
def scrape_index(filename):
    """
    Append textbook index to existing database

    Args:
        filename: A string representing the file name of the index PDF. Should be in preexisting naming template [First Author]_ocr[Y|N]_[ISBN].pdf

    Returns:

    """

    # user_input = input('Have you pulled from git? (y/n): ')
    # if user_input.lower() == 'y':
    #     print("Proceed!")
    # elif user_input.lower() == 'n':
    #     print('Go pull from git!!')
    #     return
    # else:
    #     print('Type yes or no')


    ISBN = re.search("(\d+).pdf", filename).group(1)
    # ISBN = "".join(ISBN) #joins list to make string

    #measure for preventing duplicates
    temp = pd.read_csv("./data_proc/masterlist.csv") #reads in current masterlist

    if ISBN in temp: #checks for ISBN in masterlist
        print("ISBN already in masterlist.") #prints error and returns
        return

    if re.search("ocry", filename, re.IGNORECASE) is not None:
        print("File {} needs OCR; skipping...".format(filename))
        return

    filename = "./data_pdf/" + filename
    pdfFileObj = open(filename, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numpages = pdfReader.numPages
    df = []
    for i in range(numpages):
        pageObj = pdfReader.getPage(i)
        # extracting text from page
        df.append(pageObj.extractText())

    text = ""
    for i in range(len(df)):
        text = df[i] + text

    text = text.replace("\n", ",")
    text = text.split(",")

    filtered = []
    for term in text:
        if any(c.isalpha() for c in str(term)):
            filtered.append((term, ISBN))
    index = pd.DataFrame(filtered)
    index.to_csv('./data_proc/masterlist.csv', mode='a', index=False, header=False)

## Find and process all files
filenames = os.listdir('./data_pdf')
# Filter to PDFs only
filenames = filter(lambda s: s[-3:].lower() == "pdf", filenames)

# Ensure masterlist exists
if not os.path.exists("./data_proc/masterlist.csv"):
    pd.DataFrame({"Term": [], "ISBN": []}).to_csv("./data_proc/masterlist.csv", index=False)
    print("No masterlist.csv found; creating blank file")

# Process all files
print("Scraping all Index files:")
for filename in filenames:
    print("... scraping {}".format(filename))
    scrape_index(filename)
