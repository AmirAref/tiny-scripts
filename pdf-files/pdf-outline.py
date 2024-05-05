from dataclasses import dataclass
from enum import StrEnum, auto

from PyPDF2 import PageObject, PdfReader, PdfWriter
from PyPDF2.generic import PAGE_FIT, Fit


class Fits(StrEnum):
    PAGE = auto()
    TOP = auto()
    TOP2 = auto()
    CENTER = auto()
    BOTTOM = auto()
    BOTTOM2 = auto()


def get_fit(page: PageObject, fit: Fits = Fits.PAGE) -> Fit:
    page_height = float(page.mediabox.height)

    match fit:
        case Fits.TOP:
            return Fit.fit_horizontally(top=(page_height / 3 * 2))
        case Fits.TOP2:
            return Fit.fit_horizontally(top=(page_height / 4 * 3))
        case Fits.CENTER:
            return Fit.fit_horizontally(top=(page_height / 2))
        case Fits.BOTTOM:
            return Fit.fit_horizontally(top=(page_height / 3))
        case Fits.BOTTOM2:
            return Fit.fit_horizontally(top=(page_height / 4))
        case _:
            return PAGE_FIT


@dataclass
class OutlineItem:
    title: str
    page: int
    fit: Fits = Fits.PAGE


class BaseOutline:
    def __init__(self, outline: OutlineItem, children: list[OutlineItem] = []) -> None:
        self.outline = outline
        self.children = children


def add_pdf_outline(
    new_pdf: PdfWriter, outline: list[BaseOutline], first_page: int = -1
):
    before = None
    for item in outline:
        # add prent
        page_number = first_page + item.outline.page
        page_object = new_pdf.pages[page_number]
        parent = new_pdf.add_outline_item(
            title=item.outline.title,
            page_number=page_number,
            before=before,
            fit=get_fit(page=page_object, fit=item.outline.fit),
        )
        # set brefore
        if before is None:
            before = parent
        # add children
        for child in item.children:
            page_number = first_page + child.page
            page_object = new_pdf.pages[page_number]
            new_pdf.add_outline_item(
                title=child.title,
                page_number=page_number,
                parent=parent,
                fit=get_fit(page=page_object, fit=child.fit),
            )


document_outline_tree = [
    BaseOutline(
        outline=OutlineItem(title="outline 1", page=1),
        children=[
            OutlineItem(title="child 1 - fit", page=2),
            OutlineItem(title="child 2 - top", page=2, fit=Fits.TOP),
            OutlineItem(title="child 3 - top", page=2, fit=Fits.CENTER),
            OutlineItem(title="child 3 - top", page=2, fit=Fits.CENTER),
        ],
    ),
    BaseOutline(
        outline=OutlineItem(title="outline 2", page=3),
        children=[
            OutlineItem(title="child 1 - fit", page=4),
            OutlineItem(title="child 2 - top", page=4, fit=Fits.TOP),
            OutlineItem(title="child 3 - top", page=4, fit=Fits.CENTER),
            OutlineItem(title="child 3 - top", page=4, fit=Fits.CENTER),
        ],
    ),
]


if __name__ == "__main__":
    # read pdf
    author = "author name"
    document_title = "title of the docuemnt"
    pdf_file_path = "pdf_file_path.pdf"
    creator = "creator of document"
    pdf_file = PdfReader(stream=pdf_file_path)
    # create output pdf
    new_pdf = PdfWriter()
    # import old data
    start_page = -1
    # import the pdf to new pdf
    new_pdf.merge(position=None, fileobj=pdf_file)
    # add outlines objects
    add_pdf_outline(
        new_pdf=new_pdf,
        outline=document_outline_tree,
        first_page=start_page,
    )
    # add pdf metadata
    metadata = {
        # "/CreationDate": "D:20180613174011+05'30'",
        # "/ModDate": "D:20190119163727+01'00'",
        # "/Producer": "3-Heights(TM) PDF Optimization Shell 4.8.25.2 (http://www.pdf-tools.com)",
        "/Author": author,
        "/Title": document_title,
        "/Creator": creator,
    }
    new_pdf.add_metadata(infos=metadata)
    # save output
    new_pdf.write(f"{pdf_file_path.rstrip('.pdf')}_output.pdf")
