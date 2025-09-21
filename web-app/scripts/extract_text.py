#!/usr/bin/env python3
"""
Text extraction script for CV files using Tesseract OCR for all PDFs.
"""

import sys
from pathlib import Path
import subprocess
import tempfile
import os


def extract_text_tesseract(pdf_path: Path) -> str:
	"""Extract text from PDF using Tesseract OCR (for scanned PDFs)"""
	try:
		# Convert PDF to images using system tools, then Tesseract OCR
		with tempfile.TemporaryDirectory() as temp_dir:
			# Use poppler's pdftoppm to convert PDF to images
			cmd = f"pdftoppm -png -r 300 '{pdf_path}' '{temp_dir}/page'"
			result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
			
			if result.returncode != 0:
				raise Exception(f"PDF to image conversion failed: {result.stderr}")
			
			# Find generated image files
			image_files = sorted([f for f in os.listdir(temp_dir) if f.endswith('.png')])
			if not image_files:
				raise Exception("No images generated from PDF")
			
			# Extract text from each image using Tesseract
			text_chunks = []
			for image_file in image_files:
				image_path = os.path.join(temp_dir, image_file)
				# Use Tesseract directly via system command
				cmd = f"tesseract '{image_path}' stdout -l eng"
				result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
				
				if result.returncode == 0 and result.stdout.strip():
					text_chunks.append(result.stdout.strip())
				elif result.stderr:
					print(f"Tesseract warning for {image_file}: {result.stderr}", file=sys.stderr)
			
			return "\n\n".join(text_chunks).strip()
	except Exception as e:
		raise Exception(f"Tesseract OCR extraction failed: {str(e)}")


def extract_text(pdf_path: Path) -> str:
	"""Extract text from PDF using Tesseract OCR for all PDFs"""
	try:
		print("Processing PDF with Tesseract OCR...", file=sys.stderr)
		return extract_text_tesseract(pdf_path)
	except Exception as e:
		raise Exception(f"Tesseract OCR extraction failed: {str(e)}")


def main() -> None:
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print("Usage: python extract.py <input.pdf> [output.txt]")
		sys.exit(1)

	pdf_path = Path(sys.argv[1])
	if not pdf_path.exists():
		print(f"File not found: {pdf_path}")
		sys.exit(1)

	output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else None

	text = extract_text(pdf_path)

	if output_path:
		output_path.write_text(text, encoding="utf-8")
		print(f"Extracted text written to {output_path}")
	else:
		print(text)


if __name__ == "__main__":
	main()