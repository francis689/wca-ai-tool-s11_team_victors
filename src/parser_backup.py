from pathlib import Path
from pypdf import PdfReader


# Where the RUPSA SACCO PDFs are stored
PDF_FOLDER = Path("data/pdfs")

# Where extracted text will be saved
OUTPUT_FOLDER = Path("data/processed")


def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF."""
    reader = PdfReader(pdf_path)

    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages_text.append(text)
        else:
            print(f"Warning: No text found on page {page_number} of {pdf_path.name}")

    return "\n\n".join(pages_text)


def process_all_pdfs():
    """Find and process every PDF inside data/pdfs."""
    
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    pdf_files = list(PDF_FOLDER.rglob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    if not pdf_files:
        print("No PDF files found.")
        return

    processed_count = 0

    for pdf_path in pdf_files:
        try:
            print(f"Processing: {pdf_path}")

            text = extract_text_from_pdf(pdf_path)

            # Keep the same folder structure as data/pdfs
            relative_path = pdf_path.relative_to(PDF_FOLDER)

            output_path = OUTPUT_FOLDER / relative_path.with_suffix(".txt")

            output_path.parent.mkdir(parents=True, exist_ok=True)

            output_path.write_text(text, encoding="utf-8")

            print(f"Saved: {output_path}")

            processed_count += 1

        except Exception as error:
            print(f"ERROR processing {pdf_path}: {error}")

    print()
    print(f"Finished processing {processed_count} PDF files.")


if __name__ == "__main__":
    process_all_pdfs()