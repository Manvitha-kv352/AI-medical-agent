from pypdf import PdfReader

pdf_path = r"C:\Users\MANVITH\OneDrive\Desktop\type 2 diabetes review.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text

print("\n===== FIRST 5000 CHARACTERS =====\n")
print(text[:5000])

print("\n\nTotal Characters:", len(text))