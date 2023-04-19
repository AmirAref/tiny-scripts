from PyPDF2 import PdfMerger
from pathlib import Path
import sys

def main():
    # get folder name
    try:
        folder = sys.argv[1]
    except IndexError:
        return print("please give the folder path of files.\nfor current dir send the \".\"")

    # check folder 
    folder = Path(folder)
    if not folder.exists():
        return print("The folder isn't exists, please check the folder name agian.")
    


    # sort pdf files names
    files = [item for item in folder.rglob("*.pdf")]
    files.sort(key=lambda x:int(x.stem.split('-')[1]) )
    
    # merge files
    with PdfMerger() as merger:
        for pdf in files:
            merger.append(pdf)
            print(pdf.name)
        # write
        merger.write(f"{folder.stem}.pdf") # Output the merged PDF file

if __name__ == "__main__":
    main()
