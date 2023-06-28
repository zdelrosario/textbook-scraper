# textbook-scraper

This is the software toolchain used in the conference paper ["A Scoping Review of Engineering Textbooks to Quantify the Teaching of Uncertainty"](https://nemo.asee.org/public/conferences/327/papers/36798/view). This toolchain uses Python code to consolidate digitized textbook indexes into a single spreadsheet (the `masterlist.csv`).

## Scraping Workflow (Python)

[Download](https://github.com/zdelrosario/textbook-scraper/archive/refs/heads/main.zip) the contents of this repository (or clone it locally) and run the following steps:

1. (Install Python dependencies for textbook scraper) Using a python installation with a functional [pip](https://pypi.org/project/pip/) installation. Use the `requirements.txt` to install all python dependencies, i.e. with the command line invocation `pip install -r requirements.txt` from your terminal.
  - If you haven't used a *terminal* before, you may want to check out [this tutorial](https://towardsdatascience.com/a-quick-guide-to-using-command-line-terminal-96815b97b955)

2. (Prepare your source PDFs) Collect PDFs of the indexes you want to scrape. Make sure to truncate these PDFs so only the pages of the index are in each file. (You can use a PDF editor to do this.)
  - Name each PDF with the following format:

> `lastname_ocrN_isbn13.pdf`

For instance, Sheppard, Sheri D., Thalia Anagnos, and Sarah L. Billington. Engineering mechanics: Statics: Modeling and analyzing systems in equilibrium. Wiley Global Education, 2017. ISBN-13: 978-1119725138 would translate to:

> `sheppard_orcN_9781119725138.pdf`

*Note*: We use the `ocr` flag to denote PDFs that need Optical Character Recognition (OCR) to deal with scans that do not have digital text. This is part of an automated OCR workflow that we tested but could not get working reliably.

3. (Collect your source PDFs) Place all of your trimmed and properly-named PDFs in the `data_pdf` folder.

4. Run the scraping tool with the terminal invocation `python scrape_all.py`. This will either generate or overwrite the file `data_proc/masterlist.csv`. After running the `scape_all.py` utility, the `masterlist.csv` file will contain all lines from all indexes in a single table. For instance, this is the top of our table:

| Term | ISBN |
| 726 Index | 9780521883030 |
| Virtual movement | 9780521883030 |
| see also | 9780521883030 |

## Suggestions on analysis

We used a variety of R scripts to analyze the scraped index data; you may find some useful code in `analysis/analyze_terms.Rmd`.
