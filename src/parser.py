from pathlib import Path
from pypdf import PdfReader

# Where the RUPSA SACCO knowledge-base files are stored
DATA_FOLDER = Path("data/pdfs")

# Where processed text will be saved
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
            print(
                f"Warning: No text found on page "
                f"{page_number} of {pdf_path.name}"
            )

    return "\n\n".join(pages_text)


def process_text_file(txt_path):
    """Read an existing TXT knowledge-base file."""
    return txt_path.read_text(encoding="utf-8")


def process_all_files():
    """Find and process PDF and TXT files inside data/pdfs."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    pdf_files = list(DATA_FOLDER.rglob("*.pdf"))
    txt_files = list(DATA_FOLDER.rglob("*.txt"))

    print(f"Found {len(pdf_files)} PDF files.")
    print(f"Found {len(txt_files)} TXT files.")

    processed_count = 0

    # Process PDF files
    for pdf_path in pdf_files:
        try:
            print(f"Processing PDF: {pdf_path}")

            text = extract_text_from_pdf(pdf_path)

            relative_path = pdf_path.relative_to(DATA_FOLDER)
            output_path = OUTPUT_FOLDER / relative_path.with_suffix(".txt")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding="utf-8")

            print(f"Saved: {output_path}")
            processed_count += 1

        except Exception as error:
            print(f"ERROR processing {pdf_path}: {error}")

    # Process TXT files
    for txt_path in txt_files:
        try:
            print(f"Processing TXT: {txt_path}")

            text = process_text_file(txt_path)

            relative_path = txt_path.relative_to(DATA_FOLDER)
            output_path = OUTPUT_FOLDER / relative_path

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding="utf-8")

            print(f"Saved: {output_path}")
            processed_count += 1

        except Exception as error:
            print(f"ERROR processing {txt_path}: {error}")

    print()
    print(f"Finished processing {processed_count} files.")


if __name__ == "__main__":
    process_all_files()