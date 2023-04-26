import PyPDF2
from pathlib import Path
import sys




def main():
    pages = {}

    try:
        path = Path(sys.argv[1])
        if not path.is_dir():
            raise ValueError
    except IndexError:
        path = Path()
    except ValueError:
        return print("please give a correct directory path (empty for current path")

    for filename in path.rglob('*.pdf'):
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
    
    for p in pages:
        print(p, pages[p])
    # total
    print()
    print("total pages of {} folders is {}".format(len(pages), sum(pages.values())))



if __name__ == "__main__":
    main()

