import pdfplumber
import docx
import re


def extract_text(file):

    text = ""

    # PDF
    if file.name.endswith(".pdf"):

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    # DOCX
    elif file.name.endswith(".docx"):

        doc = docx.Document(file)

        for para in doc.paragraphs:
            text += para.text + "\n"

    # CLEAN TEXT
    text = re.sub(r'[ \t]+', ' ', text)

    return text
