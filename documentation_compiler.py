import os
from PyPDF2 import PdfMerger
from pathlib import Path

# Path to the directory containing the PDFs
pdf_dir = Path(r"C:\Users\Aadi Jha\Downloads\manim-documentation")

# Get all PDF files and sort them by creation time
pdf_files = sorted(
    [f for f in pdf_dir.glob("*.pdf")],
    key=lambda x: x.stat().st_ctime
)

# Output file path
output_path = "merged_manim_docs.pdf"

# Merge PDFs
merger = PdfMerger()

for pdf in pdf_files:
    merger.append(str(pdf))

merger.write(str(output_path))
merger.close()

print(f"✅ Merged {len(pdf_files)} PDFs into {output_path}")
