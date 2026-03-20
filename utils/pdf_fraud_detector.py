import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_extract


# Fallback extractor (pdfminer)
def extract_hidden_text_fallback(file):
    try:
        file.seek(0)
        return pdfminer_extract(file)
    except:
        return ""


def detect_hidden_text(uploaded_file):

    try:
        uploaded_file.seek(0)

        file_bytes = uploaded_file.read()

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        # RULE 1,2,3 → Span-based detection
        for page in doc:

            blocks = page.get_text("dict")["blocks"]

            for block in blocks:

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    for span in line["spans"]:

                        text = span["text"].strip()
                        size = span["size"]
                        color = span["color"]

                        if not text:
                            continue

                        if set(text) == {"_"}:
                            continue

                        # Rule 1: extremely tiny font
                        if size < 5:
                            return True, f"Hidden tiny font detected: '{text}'"

                        # 🔥 FIX 2: Only detect REAL white text (not black)
                        if size < 8 and color >= 16000000:
                            return True, f"Hidden white/invisible text detected: '{text}'"

                        # Rule 3: suspicious hidden keyword
                        if size < 8 and len(text) <= 15 and text.isalpha():
                            return True, f"Suspicious hidden keyword detected: '{text}'"

        # RULE 4 → Extractor mismatch detection (NEW)
        uploaded_file.seek(0)

        normal_text = ""
        try:
            doc_text = []
            for page in doc:
                doc_text.append(page.get_text())
            normal_text = " ".join(doc_text)
        except:
            pass

        hidden_text = extract_hidden_text_fallback(uploaded_file)

        if hidden_text and len(hidden_text) > len(normal_text) * 1.3:
            return True, "Possible hidden/invisible text detected (text mismatch)"

        # FINAL → No fraud
        return False, ""

    except Exception as e:
        return False, f"PDF detection error: {str(e)}"
