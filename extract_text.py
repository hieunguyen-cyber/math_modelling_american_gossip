import sys
from pypdf import PdfReader

def extract_pdf(pdf_path, txt_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {pdf_path} to {txt_path}")

if __name__ == "__main__":
    extract_pdf("The spread of gossip in American schools.pdf", "epl.txt")
    extract_pdf("Spreading gossip in social networks.pdf", "pre.txt")
