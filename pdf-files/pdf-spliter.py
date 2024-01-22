from PyPDF2 import PdfReader, PdfWriter



def main():
    reader = PdfReader('./full-book.pdf')
    chapters = {
        1:(49, 56),
        2:(83,94),
        3:(106,113),
        4:(134,146),
        5:(171,185),
        6:(186, 188),
    }

    # extract the pages of each chapter
    for chapter, ch_range in chapters.items():
        # write a new pdf file
        chapter_pdf = PdfWriter()
        # add pages
        for p in range(ch_range[0] - 1, ch_range[1]):
            chapter_pdf.add_page(reader.pages[p])
        # export file 
        file_name = f"Chapter-{chapter}.pdf"
        chapter_pdf.write(file_name)
        print(file_name, f": {ch_range[1] - ch_range[0] + 1} pages writed !")



if __name__ == "__main__":
    main()

