import PyPDF2
from pathlib import Path
import sys


def main():
    pages = {}

    for filename in Path().rglob('*/*.pdf'):
       # get pages number
        with open(filename, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            numpages = len(pdf.pages)
            # save pages count of exam
            parent = filename.parent.name
            if parent in pages:
                pages[parent] += numpages
            else:
                pages[parent] = numpages

    # total
    for folder, page_count in pages.items():
        print(folder, page_count)
    print(f"total {sum(pages.values())} pages of {len(pages)} folders.")

if __name__ == "__main__":
    main()
