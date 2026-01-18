from PyPDF2 import PdfReader

# Read the PDF
pdf_path = "20260105-UAS-Kriptografi.pdf"
reader = PdfReader(pdf_path)

# Extract text from all pages
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# Save to text file
with open("20260105-UAS-Kriptografi.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(f"PDF converted to text successfully!")
print(f"Total pages: {len(reader.pages)}")
