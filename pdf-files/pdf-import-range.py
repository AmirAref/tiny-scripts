"""
this script is a tool to import a specific range of a pdf file to a new file, withoout losing outline and medtadata
"""


from PyPDF2 import PdfReader, PdfWriter


def main():
    source_file = "full-book.pdf"
    output_file = "physiscs-mechanics.pdf"

    # read source file
    reader = PdfReader(source_file)

    # merge specific range from source to putput
    output_pdf = PdfWriter()
    # pages : 37-484
    output_pdf.merge(position=0, fileobj=reader, pages=(36, 484), import_outline=True)
    # add metadata
    output_pdf.add_metadata(dict(reader.metadata))
    # save output
    output_pdf.write(output_file)


if __name__ == "__main__":
    main()
